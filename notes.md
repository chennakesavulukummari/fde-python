FDE Day 1 – Windows Host Machine Setup

Objective: Prepare a Windows laptop/desktop as an FDE engineering workstation using Python, Git, AWS CLI v2, Google Chrome and Visual Studio Code.

We will use Windows Package Manager (winget) to install the utilities automatically instead of downloading and installing each application manually.

Utility	                    Purpose
Python 3	                Programming and automation
Git	                        Source code management
AWS CLI v2	                AWS cloud management
Google Chrome	            Browser and testing
Visual Studio Code	        Python development
VS Code Python Extension	Python development support

2. Step 1 – Verify Windows and winget
Ask students to open:

Start → Search → Windows PowerShell → Run as Administrator

Check Windows version:

winver

Check winget availability:

winget --version

3. Step 2 – Install all utilities using winget
Run the following commands one by one in PowerShell:

1. Install Python

winget install --id Python.Python.3.13 --exact --source winget

2. Install Git

winget install --id Git.Git --exact --source winget

3. Install AWS CLI version 2

winget install --id Amazon.AWSCLI --exact --source winget

4. Install Google Chrome

winget install --id Google.Chrome --exact --source winget

5. Install Visual Studio Code

winget install --id Microsoft.VisualStudioCode --exact --source winget

6. Install Python extensions in VS Code

Close and reopen PowerShell after the VS Code installation, then run:

code --install-extension ms-python.python

code --install-extension ms-python.vscode-pylance


```


```
