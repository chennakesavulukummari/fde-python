# if
# if-else
# if-elif-else
# Nested if

# 1. Simple if Statement

# if condition:
#     # code to execute if condition is True
#     pass

age = 18
if age >= 18:
    print("You are eligible to vote.")

# 2. if-else Statement
age = 17
if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")

# 3. if-elif-else Statement

age = 20
if age < 13:
    print("You are a child.")
elif age < 20:
    print("You are a teenager.")
else:
    print("You are an adult.")


# Student marks
marks = 85

if marks >= 90:
    print("Grade A")
elif marks >= 75:
    print("Grade B")
elif marks >= 60:
    print("Grade C")
elif marks >= 35:
    print("Grade D")
else:
    print("Fail")

# ATM Withdrawal

balance = 10000
withdraw_amount = 5000

if balance > 0:
    if withdraw_amount <= balance:
        print("Withdrawal successful")
    else:
        print("Insufficient balance")
else:
    print("Account has no balance")

# Login Authentication

username = "admin"
password = "admin123"

if username == "admin" and password == "admin123":
    print("Login Successful")
else:
    print("Invalid Credentials")

# Cloud Server Status

server_status = "running"

if server_status == "running":
    print("Server is healthy")
elif server_status == "stopped":
    print("Server is stopped")
elif server_status == "terminated":
    print("Server is deleted")
else:
    print("Unknown server status")

# AWS Environment Deployment

environment = "production"

if environment == "dev":
    print("Deploying to Development")
elif environment == "preprod":
    print("Deploying to Preproduction")
elif environment == "production":
    print("Deploying to Production")
else:
    print("Invalid Environment")

# CPU Utilization Monitoring
cpu_usage = 85

if cpu_usage >= 90:
    print("CRITICAL: CPU usage is very high")
elif cpu_usage >= 75:
    print("WARNING: CPU usage is high")
else:
    print("CPU usage is normal")

# 6. Conditional Operators
a = 10
b = 20
==	Equal to	a == b : False
!=	Not equal	a != b : True
>	Greater than	a > b : False
<	Less than	a < b : True
>=	Greater than or equal to	a >= b : False
<=	Less than or equal to	a <= b : True   

and	Both conditions True	a > 10 and b > 20
or	Either condition True	a > 10 or b > 20
not	Reverses condition	not a == 10

# Important Concepts to Explain

indentation	Python uses spaces to define code blocks
Colon :	Required after if, elif, and else
Boolean	Conditions evaluate to True or False
Nested conditions	One condition inside another
Logical operators	Combine multiple conditions

# Python Loops (for, while, break, continue, pass)

# 1. What are loops?
# A loop is used to execute a block of code repeatedly until a specific condition is met or a sequence is exhausted.


