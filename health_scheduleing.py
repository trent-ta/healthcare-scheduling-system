import csv
from datetime import datetime

# load_appointments() allows you to read ad clean appointnent data
def load_appointments():
    # Store all cleaned appointment records
    appointments = []
    # Read "appointments_data.csv" file containng 40 appointment records
    with open ('appointments_data.csv', mode = 'r') as file:
        
        # Use DictReader to make each row is stored as a dictionary
        csvFile = csv.DictReader(file)
        
        # Loop through each appointment record
        for row in csvFile:

            # Convert AppointmentTime string into a datetime object
            appt = datetime.strptime(row['AppointmentTime'], '%H:%M')

            # Determine ArrivalStatus
            if row['NoShow'] == '1':
                status = 'Missed'

            # Check if paitent showed up (CheckInTime is not NA)
            elif row['CheckInTime'] != 'NA':
                checkin = datetime.strptime(row['CheckInTime'], '%H:%M')

                # Calculate the time difference in minutes (how late or early paitent arrived)
                difference = (checkin - appt).total_seconds() / 60

                # Determine ArrivalStatus based on the time difference
                if difference > 15:
                    status = 'Late'     
                else:
                    status = 'OnTime'
            else:
                status = 'Missed' 

            # Add a new column "ArrivalStatus" to the appointments records
            row['ArrivalStatus'] = status

            appointments.append(row)
    
    return appointments

# Option 1: View all records
def view_all_records(appointments):
    for row in appointments:
        print(row)

# Option 2: Enter a new appointment record
def enter_new_record(appointments):
    appointment_id = input("Enter AppointmentID (ex. 2001): ")
    patient_name = input("Enter PatientName: ")
    appointment_date = input("Enter AppointmentDate (ex. YYYY-MM-DD): ")
    appointment_time = input("Enter AppointmentTime (ex. HH:MM): ")
    check_in_time = input("Enter CheckInTime (ex. HH:MM or NA): " )
    no_show = input("Enter NoShow (ex. 0 or 1): ")
    
    appt = datetime.strptime(appointment_time, '%H:%M')
    if no_show == '1':
        status = 'Missed'

    elif check_in_time != 'NA':
        checkin = datetime.strptime(check_in_time, '%H:%M')
        difference = (checkin - appt).total_seconds() / 60

        if difference > 15:
            status = 'Late'
        else:
            status = 'OnTime'
        
    else:
        status = 'Missed'

    new_record = {
            'AppointmentID': appointment_id,
            'PatientName': patient_name,
            'AppointmentDate': appointment_date,
            'AppointmentTime': appointment_time,
            'CheckInTime': check_in_time,
            'NoShow': no_show,
            'ArrivalStatus': status
        }
    
    appointments.append(new_record)
    print("New Appointment has been added.")
        
# Option 3: View late arrivals and missed appointments
def view_late_and_missed(appointments):
    for row in appointments:
        if row['ArrivalStatus'] == 'Late' or row['ArrivalStatus'] == 'Missed':
            print(row)

# Option 4: View attendance summary by time of day
def view_attendance_summary(appointments):
    morning = 0
    afternoon = 0
    evening = 0

    for row in appointments:
        appt = datetime.strptime(row['AppointmentTime'], '%H:%M')
        hour = appt.hour

        if hour < 12:
            morning += 1
        elif hour < 17:
            afternoon += 1
        else:
            evening += 1
    
    print("\nAttendance Summary By Time of Day")
    print("Morning: ", morning)
    print("Afternoon: ", afternoon)
    print("Evening: ", evening)

# Option 5: Sort patients by number of missed appointments
def sort_patients_by_missed(appointments):
    missed_counts = {}
    
    # Count missed per patient
    for row in appointments:
        name = row['PatientName']

        if name not in missed_counts:
            missed_counts[name] = 0

        if row['NoShow'] == '1':
            missed_counts[name] += 1
    
    # Convert dictionary to a list
    missed_list = list(missed_counts.items())

    # Create a Bubble sort (descending order)
    for i in range(len(missed_list) - 1):
        for j in range(len(missed_list) - 1 - i):
            if missed_list[j][1] < missed_list[j + 1][1]:
                temp = missed_list[j]
                missed_list[j] = missed_list[j + 1]
                missed_list[j + 1] = temp
    
    print("\nPatients sorted by missed appointments:")
    for patient, count in missed_list:
        print(patient, ":", count)


# Option 6: Export cleaned data to cleaned_appointments.csv
def export_cleaned_appointments(appointments):
    # Export cleaned data to "cleaned_appointments.csv"
    with open('cleaned_appointments.csv', 'w', newline = '') as file:
            
        # Use dictionary keys as column headers
        fieldnames = appointments[0].keys()
        writer = csv.DictWriter(file, fieldnames = fieldnames)

        # Write header row (column names)
        writer.writeheader()
        # Write all cleaned appointments records into the file
        writer.writerows(appointments)

# Main Menu
def main():
    appointments = load_appointments()

    while True:
        print("\n----------Healthcare Scheduling Menu----------")
        print("1. View all appointment records")
        print("2. Enter a new appointment record")
        print("3. View late arrivals and missed appointments")  
        print("4. View attendance summary by time of day")
        print("5. Sort patients by number of missed appointments")
        print("6. Export cleaned data to cleaned_appointments.csv")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_all_records(appointments)
        elif choice == '2':
            enter_new_record(appointments)
        elif choice == '3':
            view_late_and_missed(appointments)
        elif choice == '4':
            view_attendance_summary(appointments)
        elif choice == '5':
            sort_patients_by_missed(appointments)
        elif choice == '6':
            export_cleaned_appointments(appointments)
        elif choice == '7':
            print("Exiting Program.")
            break
        else:
            print("Invalid choice, please try agian.")

main()


