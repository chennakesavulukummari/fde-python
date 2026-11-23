# reminder.py - SunRise Hospitals appointment reminder
# Variables
patient = input("Patient name: ").strip().title()
# Str
doctor = "Dr. Rao"
# int
hour = 10
# float
fee = 500.0
# bool
is_first_vist = True

# calling variables
print(f"Hello {patient}, your appointment with {doctor} is at {hour}:00 AM.")

print(f"Consultation fee: Rs. {fee:.2f}")

if is_first_vist:
    print("Please bring a Photo ID and past reports.")
