import java.io.*;     //For file reading/writing
import java.util.*;   // For data structures like HashMap and Scanner

//Stores patient data
class Patient {
    String name;
    int totalAppointments;
    int missedAppointments;
    
    //Constructor initializes patient name and counter
    Patient(String name) {
        this.name = name;
        this.totalAppointments = 0;
        this.missedAppointments = 0;
    }

    //Determines risk status based on appointments
    String getRiskStatus() {
        if (totalAppointments >= 3 && missedAppointments >= 2) {  //If patient has 3+ appointments and missed at least 2 -> high risk
            return "At Risk";
        }
        return "Low Risk";
    }
}

public class AppointmentRecord {
    
    //Stores all patients in a HashMap using their names as keys
    static HashMap<String, Patient> patientMap = new HashMap<>();

    public static void main(String[] args) {
        loadFile("cleaned_appointments.csv");  //Loads data from .csv file into patientMap

        Scanner sc = new Scanner(System.in);
        int choice;

        //Infinite loop for the menu system
        while(true) {
            
            //Displays menu options
            System.out.println("\nHealthcare Scheduling Menu – Java");
            System.out.println("1. View no-show history per patient");
            System.out.println("2. Flag high-risk patients");
            System.out.println("3. Export flagged list to flagged_patients.csv");
            System.out.println("4. Exit");
            System.out.print("Choose: ");

            //Reads user input
            choice = sc.nextInt();

            //Chooses an option based on user input
            switch (choice) {
                case 1:
                    viewHistory();  //Shows all patients sorted by missed appointments
                    break;
                case 2:
                    flagRisk();  //Flag high-risk patients
                    break;
                case 3:
                    exportFile("flagged_patients.csv");  //Saves results to "flagged_patients.csv"
                    break;
                case 4:
                    System.out.println("Exit");  //Exits program
                    return;
                default:
                    System.out.println("Invalid option");  //Handles invalid options
            }
        }
    }

    //Reads .csv file and builds Patient stats
    public static void loadFile(String fileName) {

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {

            String line = br.readLine(); // Skips header

            //Reads each line of the file
            while ((line = br.readLine()) != null) {

                String[] data = line.split(",");  //Splits .csv row into columns

                String patientName = data[1];  //Column for patient name
                int noShow = Integer.parseInt(data[5]); //Column for no show

                //Retrieves existing patient or creates a new one if not found
                Patient stats =
                        patientMap.getOrDefault(patientName, new Patient(patientName));

                //Counts total appointments
                stats.totalAppointments++;

                //If one appointment was missed, increase missedAppointments by 1
                if (noShow == 1) {
                    stats.missedAppointments++;
                }

                //Stores updated patient data back into map
                patientMap.put(patientName, stats);
            }

        } catch (Exception e) {
            //Handles file-reading errors
            System.out.println("Error reading file: " + e.getMessage());
        }
    }

    //Sorts patients by missed appointments (descending) using a bubble sort
    public static List<Patient> bubbleSort(List<Patient> list) {
        int n = list.size();
        boolean swapped;

        //Outer loop controls the number of passes
        for (int i = 0; i < n - 1; i++) {
            swapped = false;

            //Inner loop compares adjcent elements
            for (int j = 0; j < n - i - 1; j++) {
                //Swaps if current patient has fewer missed appointments than the next
                if (list.get(j).missedAppointments < list.get(j + 1).missedAppointments) {

                    Patient temp = list.get(j);
                    list.set(j, list.get(j + 1));
                    list.set(j + 1, temp);

                    swapped = true;
                }
            }

            //If no swaps occcurred, then the list is already sorted
            if (!swapped) break;
        }

        return list;
    }

    //Displays all patients and their appointment history
    public static void viewHistory() {
        System.out.println("\nNo-Show History:");

        //Converts map values to list for sorting purposes
        List<Patient> list = new ArrayList<>(patientMap.values());
        bubbleSort(list);

        //Prints each patients data
        for (Patient p : list) {
            System.out.println(p.name +
                    " | Total: " + p.totalAppointments +
                    " | Missed: " + p.missedAppointments);
        }
    }

    //Displays patients considered "At-Risk"
    public static void flagRisk() {
        System.out.println("\nHigh-Risk Patients:");

        //Converts map values to list for sorting purposes
        List<Patient> list = new ArrayList<>(patientMap.values());
        bubbleSort(list);

        //Print patients with high-risk status
        for (Patient p : list) {
            if (p.getRiskStatus().equals("At Risk")) {
                System.out.println(p.name + " → At Risk");
            }
        }
    }

    //Exports all patient data to a .csv file
    public static void exportFile(String fileName) {

        try (FileWriter fw = new FileWriter(fileName)) {

            //Writes .csv header
            fw.write("PatientName,TotalAppointments,MissedAppointments,RiskStatus\n");

            //Sorts patients before exporting
            List<Patient> list = new ArrayList<>(patientMap.values());
            bubbleSort(list);

            //Writes each patients data as a row in the .csv file
            for (Patient p : list) {
                fw.write(p.name + "," +
                        p.totalAppointments + "," +
                        p.missedAppointments + "," +
                        p.getRiskStatus() + "\n");
            }

            System.out.println("Export complete.");

        } catch (IOException e) {
            //Handles file-writing errors
            System.out.println("Write error: " + e.getMessage());
        }
    }
}