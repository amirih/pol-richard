# Define the properties to be changed
import random
import subprocess


# Define the ranges or sets of values for each property
property_choices = {
    "numOfAgents": range(100, 1001, 100),  # 100 to 1000 in steps of 100
    "agentWalkingSpeed": [x * 0.1 for x in range(46, 100)],  # 1.4 to 2.3 in steps of 0.1
    "baseRentRate": range(300, 800, 50),  # 300 to 750 in steps of 50
    "maxNumOfFriends": range(20, 60, 4),  # 20 to 56 in steps of 4
    "numApartmentsPer1000": range(1000, 2001, 100),  # 1000 to 2000 in steps of 100
    "numWorkplacesPer1000": range(200, 401, 20),  # 200 to 400 in steps of 20
    "numRestaurantsPer1000": range(10, 31, 2),  # 10 to 30 in steps of 2
    "minimumHourlyRate": range(8, 18),  # 8 to 17
    "maximumHourlyRate": range(80, 181, 10),  # 80 to 180 in steps of 10
    "maxGroupMeetingSize": range(10, 30, 2),  # 10 to 28 in steps of 2
    "appetiteLowerBound": [x * 0.1 for x in range(2, 6)],  # 0.2 to 0.5 in steps of 0.1
    "appetiteUpperBound": [x * 0.1 for x in range(6, 10)],  # 0.6 to 0.9 in steps of 0.1
    "minimumSiteVisitLengthInMinutes": range(15, 26, 2),  # 15 to 25 in steps of 2
    "maximumSiteVisitLengthInMinutes": range(150, 241, 10),  # 150 to 240 in steps of 10
    "maxDaysToBeStarving": range(1, 6),  # 1 to 5 days
    "maxDaysToBeHomeless": range(1, 6)  # 1 to 5 days
}
combinations = []
for _ in range(1000):
    combination = {prop: random.choice(values) for prop, values in property_choices.items()}
    combination["numOfAgents"] = 182
    combination["maps"] = "beijing"
    combinations.append(combination)

def update_properties(file_path, new_props):
    # Read the existing properties
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Prepare the updated properties
    updated_lines = []
    for line in lines:
        for key, value in new_props.items():
            if line.startswith(key):
                line = f"{key} = {value}\n"
                break
        updated_lines.append(line)

    # Overwrite the original file with updated properties
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

import os
import shutil

def rename_and_move_log_dir(new_properties, result_folder="RESULT"):
    # Creating a name for the log directory from new_properties
    log_dir_name = "_".join([f"{key}_{value}" for key, value in new_properties.items()])
    
    # Check if the logs directory exists
    if os.path.exists("logs"):
        # Rename the logs directory
        os.rename("logs", log_dir_name)
        
        # Ensure the RESULT directory exists, create if it doesn't
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        # Move the renamed log directory to the RESULT folder
        shutil.move(log_dir_name, os.path.join(result_folder, log_dir_name))
        print(f"Moved and renamed 'logs' to '{os.path.join(result_folder, log_dir_name)}'")

# Path to your properties file
properties_file_path = './examples/beijing.properties'

# Java command template
java_command = (
    "java -Dlog4j2.configurationFactory=edu.gmu.mason.vanilla.log.CustomConfigurationFactory "
    "-Dlog.rootDirectory=logs -Dsimulation.test=all -jar ./target/vanilla-0.1-jar-with-dependencies.jar "
    "-configuration ./examples/beijing.properties -until 551426"
)

# Run the simulation for each combination
for new_properties in combinations:
    update_properties('examples/beijing.properties', new_properties)
    print(f"Running simulation with properties: {new_properties}")
    subprocess.run(java_command, shell=True)
    rename_and_move_log_dir(new_properties)
print("All simulations completed.")