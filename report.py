import csv
import json 

# Creating a Function 
def load_appointments(path):
    good,bad = [],[]
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                row["fee"] = float(row["fee"])
                good.append(row)
            except ValueError:
                bad.append(row)
    return good, bad 

def summarize(appointments):
    summary = {}
    for a in appointments:
        dept = a["department"]
        summary.setdefault(dept, {"count": 0, "revenue": 0.0})
        summary[dept]["count"] += 1
        summary[dept]["revenue"] += a["fee"]
    return summary 

# Calling a Function
good, bad = load_appointments("appointments.csv")
report = summarize(good)

print(json.dumps(report, indent=2))

print(f"Skipped {len(bad)} bad row(s): {[b['patient'] for b in bad]}")

with open("report.json", "w") as f:
    json.dump(report,f, indent=2)