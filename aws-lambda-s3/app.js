// ---------- CONFIG: change this ----------
const CONFIG = {
  // Function URL of the presign Lambda (see presign_lambda.py)
  PRESIGN_URL: "https://vmwqlzlgyglv75knaygi3hc6lq0toasl.lambda-url.us-east-1.on.aws/",
  MAX_SIZE_MB: 10,
};
// -----------------------------------------

const MAX_BYTES = CONFIG.MAX_SIZE_MB * 1024 * 1024;

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const emptyMsg = document.getElementById("emptyMsg");
const uploadBtn = document.getElementById("uploadBtn");
const clearBtn = document.getElementById("clearBtn");
const summary = document.getElementById("summary");

let items = [];
let nextId = 0;
let busy = false;

// ---------- helpers ----------
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function extensionOf(name) {
  const i = name.lastIndexOf(".");
  return i > -1 ? name.slice(i + 1, i + 5).toUpperCase() : "FILE";
}

// ---------- row rendering ----------
function buildRow(item) {
  const li = document.createElement("li");
  li.className = "file-row";

  const thumb = document.createElement("div");
  thumb.className = "thumb";
  if (item.file.type.startsWith("image/")) {
    item.previewUrl = URL.createObjectURL(item.file);
    const img = document.createElement("img");
    img.src = item.previewUrl;
    img.alt = `Preview of ${item.file.name}`;
    thumb.appendChild(img);
  } else {
    thumb.textContent = extensionOf(item.file.name);
  }

  const info = document.createElement("div");
  info.className = "info";

  const name = document.createElement("p");
  name.className = "name";
  name.textContent = item.file.name;
  name.title = item.file.name;

  const meta = document.createElement("p");
  meta.className = "meta";

  const bar = document.createElement("div");
  bar.className = "bar";
  const fill = document.createElement("span");
  bar.appendChild(fill);

  info.append(name, meta, bar);

  const remove = document.createElement("button");
  remove.className = "remove";
  remove.type = "button";
  remove.setAttribute("aria-label", `Remove ${item.file.name}`);
  remove.textContent = "\u00d7";
  remove.addEventListener("click", () => removeItem(item.id));

  li.append(thumb, info, remove);

  item.refs = { li, meta, fill, remove };
  return li;
}

function setStatus(item, status, message, percent) {
  item.status = status;
  const { meta, fill, remove } = item.refs;
  meta.textContent = message;
  meta.className = "meta" + (status === "done" ? " is-done" : status === "error" ? " is-error" : "");
  if (typeof percent === "number") fill.style.width = `${percent}%`;
  remove.disabled = status === "uploading";
}

function refreshControls() {
  const hasItems = items.length > 0;
  const hasReady = items.some((i) => i.status === "ready" || i.status === "error-retry");
  emptyMsg.hidden = hasItems;
  uploadBtn.disabled = busy || !hasReady;
  clearBtn.disabled = busy || !hasItems;
}

// ---------- list management ----------
function addFiles(files) {
  for (const file of files) {
    const item = { id: nextId++, file, status: "ready", previewUrl: null };
    fileList.appendChild(buildRow(item));
    if (file.size > MAX_BYTES) {
      setStatus(item, "error", `Too large (${formatSize(file.size)}). Limit is ${CONFIG.MAX_SIZE_MB} MB.`, 0);
    } else {
      setStatus(item, "ready", formatSize(file.size), 0);
    }
    items.push(item);
  }
  summary.textContent = "";
  refreshControls();
}

function removeItem(id) {
  const item = items.find((i) => i.id === id);
  if (!item) return;
  if (item.previewUrl) URL.revokeObjectURL(item.previewUrl);
  item.refs.li.remove();
  items = items.filter((i) => i.id !== id);
  refreshControls();
}

function clearAll() {
  items.forEach((i) => i.previewUrl && URL.revokeObjectURL(i.previewUrl));
  items = [];
  fileList.innerHTML = "";
  summary.textContent = "";
  refreshControls();
}

// ---------- upload ----------
function putWithProgress(url, file, contentType, onProgress) {
  // XMLHttpRequest is used because fetch() cannot report upload progress.
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", url);
    xhr.setRequestHeader("Content-Type", contentType);
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) onProgress(Math.round((e.loaded / e.total) * 100));
    };
    xhr.onload = () =>
      xhr.status >= 200 && xhr.status < 300
        ? resolve()
        : reject(new Error(`S3 rejected the upload (HTTP ${xhr.status})`));
    xhr.onerror = () => reject(new Error("Network error. Check the S3 CORS configuration."));
    xhr.send(file);
  });
}

async function uploadOne(item) {
  const contentType = item.file.type || "application/octet-stream";

  setStatus(item, "uploading", "Requesting upload URL\u2026", 0);

  const res = await fetch(CONFIG.PRESIGN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      fileName: item.file.name,
      contentType,
      size: item.file.size,
    }),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`Could not get upload URL (HTTP ${res.status}) ${detail}`.trim());
  }

  const { uploadUrl, key } = await res.json();

  await putWithProgress(uploadUrl, item.file, contentType, (pct) =>
    setStatus(item, "uploading", `Uploading\u2026 ${pct}%`, pct)
  );

  setStatus(item, "done", `Uploaded as ${key}`, 100);
}

async function uploadAll() {
  const queue = items.filter((i) => i.status === "ready" || i.status === "error-retry");
  if (queue.length === 0) return;

  busy = true;
  refreshControls();
  summary.textContent = "Uploading\u2026";

  let ok = 0;
  let failed = 0;

  for (const item of queue) {
    try {
      await uploadOne(item);
      ok++;
    } catch (err) {
      failed++;
      setStatus(item, "error-retry", err.message, 0);
      item.refs.meta.className = "meta is-error";
    }
  }

  busy = false;
  summary.textContent =
    failed === 0
      ? `${ok} file${ok === 1 ? "" : "s"} uploaded. The Lambda should fire within a few seconds.`
      : `${ok} uploaded, ${failed} failed. Fix the errors above and select Upload files to retry.`;
  refreshControls();
}

// ---------- events ----------
dropzone.addEventListener("click", () => fileInput.click());
dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    fileInput.click();
  }
});

fileInput.addEventListener("change", () => {
  addFiles(fileInput.files);
  fileInput.value = ""; // allow re-selecting the same file
});

["dragenter", "dragover"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add("is-over");
  })
);

["dragleave", "drop"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove("is-over");
  })
);

dropzone.addEventListener("drop", (e) => addFiles(e.dataTransfer.files));
uploadBtn.addEventListener("click", uploadAll);
clearBtn.addEventListener("click", clearAll);

refreshControls();