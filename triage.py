# triage.py - Sort SunRise Help Desk tickets into triage categories

# Create a List Variable to hold the tickets
tickets = [
    {"id": 101, "issue": "chest pain", "age": 67},
    {"id": 102, "issue": "shortness of breath", "age": 72},
    {"id": 103, "issue": "abdominal pain", "age": 55},
    {"id": 104, "issue": "headache", "age": 30},
    {"id": 105, "issue": "billing query", "age": 45},
    {"id": 106, "issue": "fever", "age": 25},  
    {"id": 107, "issue": "report download", "age": 80}, 
]

urget_words = ["chest pain", "shortness of breath", "abdominal pain"]
# urget = []
# normal = []
urget, normal = [], []

# Loop through the tickets and sort them into urgent and normal lists
for ticket in tickets:
    if ticket["issue"] in urget_words:
        urget.append(ticket)
    else:
        normal.append(ticket)

print(f"Urgent Tickets: {len(urget)} Normal Tickets: {len(normal)}")
for ticket in urget:
    print(f"Urgent Ticket ID: {ticket['id']} Issue: {ticket['issue']} Age: {ticket['age']}")

for ticket in normal:
    print(f"Normal Ticket ID: {ticket['id']} Issue: {ticket['issue']} Age: {ticket['age']}")
