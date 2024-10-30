import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


custom_header = ["V", "J", "Pe", "Ct", "Cp", "PWR", "Torque", "Thrust", "PWR", "Torque",
                 "Thrust", "THR/PWR", "Mach", "Reyn", "FOM"]
units = ["(mph)", "(Adv_Ratio)", "-", "-", "-", "(Hp)", "(In-Lbf)", "(Lbf)", "(W)", "(N-m)",
         "(N)", "(g/W)", "-", "-", "-"]

def convert_dat_to_csv_with_custom_header(dat_file_path, csv_file_path):
    with open(dat_file_path, 'r') as dat_file, open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(custom_header)
        csv_writer.writerow(units)
        header_str = ' '.join(custom_header)# Skip line criteria
        units_str = ' '.join(units)
        # Scan Lines
        for line in dat_file:
            # Strip whitespace from the line and check if header and units are repeated
            if line.strip() == header_str or line.strip() == units_str:
                continue  # Header/Units skip check

            # Write the line to the CSV
            row = line.strip().split()
            csv_writer.writerow(row)

    print(f"Conversion complete. Data saved to {csv_file_path}")

def process_dat_file(dat_file_path, csv_file_path):
    convert_dat_to_csv_with_custom_header(dat_file_path, csv_file_path)
    # Load the new CSV into DataFrame
    df = pd.read_csv(csv_file_path, header=None)
    first_two_rows = df.iloc[1:2].copy()# Separate the first two rows
    # Remove any rows that match either the custom header or units
    remaining_rows = df.iloc[2:]
    filtered_rows = remaining_rows[~remaining_rows.apply(
        lambda row: ' '.join(map(str, row.values)) in [' '.join(custom_header), ' '.join(units)],
        axis=1
    )]

    # Concatenate the second row back with the filtered data
    df_cleaned = pd.concat([first_two_rows, filtered_rows], ignore_index=True)

    # Rename columns based on the custom header
    df_cleaned.columns = ["V(mph)", "J(Adv_Ratio)", "Pe", "Ct", "Cp", "PWR(Hp)", "Torque(In-Lbf)",
                          "Thrust(Lbf)", "PWR(W)", "Torque(N-m)", "Thrust(N)", "THR/PWR(g/W)",
                          "Mach", "Reyn", "FOM"]

    # Save the cleaned DataFrame
    cleaned_csv_path = csv_file_path  # Overwrite pre-cleaned iteration
    df_cleaned.to_csv(cleaned_csv_path, index=False)
    print(f"Cleaned data saved to {cleaned_csv_path}")

    df = pd.read_csv(cleaned_csv_path)
    # Identify RPM rows by locating rows where 'Ct' values are digits(Due to the fact that RPM values are in the same column as Ct values)
    rpm_rows = df[df['Ct'].apply(lambda x: str(x).isdigit())].index.tolist()
    # Segment data based on RPM rows
    #Extra functionality to visualize segments
    segment_dfs_raw = {}
    for i in range(len(rpm_rows)):
        start = rpm_rows[i] + 1
        if i + 1 < len(rpm_rows):
            end = rpm_rows[i + 1]
        else:
            end = len(df)
        segment_dfs_raw[f'segment_{i + 1}'] = df.iloc[start:end].copy()
    # Extract RPM values from 'Ct' column at rpm_rows
    rpm_values = []
    for idx in rpm_rows:
        rpm_value = int(df.loc[idx, 'Ct'])
        rpm_values.append(rpm_value)

    return df, segment_dfs_raw, rpm_values

def collect_data(segment_dfs_raw, rpm_values, variable_to_hold_constant, variable_value, selected_variable, label):
    # Initialize lists to collect RPM and selected variable values
    rpm_list = []
    selected_variable_values = []

    for i, (segment_name, segment_df) in enumerate(segment_dfs_raw.items()):
        # Convert all columns to numeric where possible
        segment_df = segment_df.apply(pd.to_numeric, errors='coerce')

        rpm_value = rpm_values[i]

        # Check if the variable to hold constant and the selected variable exist
        if variable_to_hold_constant not in segment_df.columns or selected_variable not in segment_df.columns:
            print(f"Variable '{variable_to_hold_constant}' or '{selected_variable}' not found in {segment_name}. Skipping this segment.")
            continue
        # Filter rows where the variable to hold constant is close to the specified value
        matching_rows = segment_df[(segment_df[variable_to_hold_constant] - variable_value).abs() < tolerance]

        # Interpolate if exact match is not found
        if not matching_rows.empty:
            # Exact match found
            selected_row = matching_rows.iloc[0]
        else:
            # No exact match, perform linear interpolation
            differences = segment_df[variable_to_hold_constant] - variable_value
            positive_diff = differences[differences > 0]
            negative_diff = differences[differences < 0]

            if not positive_diff.empty and not negative_diff.empty:
                idx_above = positive_diff.idxmin()
                idx_below = negative_diff.idxmax()
                # Extract rows for interpolation
                row_above = segment_df.loc[idx_above]
                row_below = segment_df.loc[idx_below]

                # Calculate interpolation factor
                factor = (variable_value - row_below[variable_to_hold_constant]) / (row_above[variable_to_hold_constant] - row_below[variable_to_hold_constant])

                # Interpolate the selected variable
                interpolated_value = row_below[selected_variable] + factor * (row_above[selected_variable] - row_below[selected_variable])
                selected_row = pd.Series(segment_df.columns, index=segment_df.columns)  # Create an empty Series
                selected_row[selected_variable] = interpolated_value
            else:
                # Interpolation cannot be performed
                print(f"Cannot interpolate for {segment_name} at RPM {rpm_value} ({variable_to_hold_constant} does not cross {variable_value}).")
                continue  # Skip to the next segment

        # Collect RPM and selected variable value
        rpm_list.append(rpm_value)
        selected_variable_values.append(selected_row[selected_variable])
        print(f"[{label}] At RPM {rpm_value}, interpolated {selected_variable} = {selected_row[selected_variable]}")

    # Create a DataFrame from the collected data
    plot_df = pd.DataFrame({'RPM': rpm_list, selected_variable: selected_variable_values})

    # Sort the DataFrame by RPM (optional)
    plot_df.sort_values('RPM', inplace=True)

    return plot_df

def plot_xy_at_rpm(df, segment_dfs_raw, rpm_values):
    # Available columns for selection
    available_columns = df.columns.tolist()
    print("Available columns for plotting:")
    print(available_columns)

    # Prompt the user for input columns and RPM value
    x = input(f"Input X-axis variable from the above list: ")
    y = input(f"Input Y-axis variable from the above list: ")
    z = int(input(f"Input RPM value from available RPMs {rpm_values}: "))

    # Check if the selected columns exist
    if x not in available_columns or y not in available_columns:
        print("Selected variables not found in the data. Please check the variable names and try again.")
        return

    # Find the segment corresponding to the selected RPM
    try:
        rpm_index = rpm_values.index(z)
        segment_name = f'segment_{rpm_index + 1}'
        segment_df = segment_dfs_raw[segment_name]
    except ValueError:
        print(f"RPM {z} not found in the dataset.")
        return

    # Convert columns to numeric
    segment_df[x] = pd.to_numeric(segment_df[x], errors='coerce')
    segment_df[y] = pd.to_numeric(segment_df[y], errors='coerce')

    # Drop rows with NaN values in the selected columns
    segment_df.dropna(subset=[x, y], inplace=True)

    if segment_df.empty:
        print(f"No data available to plot for RPM {z} with the selected variables.")
        return

    # Extract data for plotting
    x_data = segment_df[x]
    y_data = segment_df[y]

    print(f"Data for X-axis ({x}):\n{x_data}")
    print(f"Data for Y-axis ({y}):\n{y_data}")

    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"Plot of {y} vs {x} at RPM {z}")
    plt.grid(True)
    plt.show()

# Main script

def main():
    # Define a tolerance for float comparison (global variable)
    global tolerance
    tolerance = 1e-5  # Adjust as needed for precision

    print("""\

                                       ._ o o
                                       \_`-)|_
                                    ,""       \ 
                                  ,"  ## |   ಠ ಠ. 
                                ," ##   ,-\__    `.
                              ,"       /     `--._;)
                            ,"     ## /
                          ,"   ##    /
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      Welcome to the Data Processing and Plotting Tool!       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    # Ask the user to choose a functionality
    print("\nChoose a functionality:")
    print("1. Hold a variable constant and plot another variable against RPM.")
    print("2. Plot any two variables against each other at a specified RPM.")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        # Functionality 1: Hold a variable constant and plot another variable against RPM.
        num_files = int(input("How many .dat files do you want to process (1 or 2)? "))

        dat_file_paths = []
        csv_file_paths = []

        for i in range(1, num_files + 1):
            dat_file_path = input(f"Paste .dat file location {i}: ")
            csv_file_path = input(f"Paste desired destination file path {i} (filepath/filename.csv): ")
            dat_file_paths.append(dat_file_path)
            csv_file_paths.append(csv_file_path)

        # Ask for variable to hold constant and its value
        variable_to_hold_constant = input("Enter the variable to hold constant (e.g., 'Cp', 'V(mph)', etc.): ")
        variable_value = float(input(f"Enter the value of {variable_to_hold_constant} to hold constant: "))

        # Ask for variable to plot against RPM
        selected_variable = input("Enter the variable you want to plot against RPM (e.g., 'Thrust(Lbf)', 'FOM', etc.): ")

        # Process each .dat file
        plot_dfs = []
        labels = []

        for i in range(num_files):
            label = f"DataSet {i+1}"
            print(f"\nProcessing {label}...")
            df, segment_dfs_raw, rpm_values = process_dat_file(dat_file_paths[i], csv_file_paths[i])
            plot_df = collect_data(segment_dfs_raw, rpm_values, variable_to_hold_constant, variable_value, selected_variable, label)
            plot_dfs.append(plot_df)
            labels.append(label)

        # Plot the selected variable against RPM for both datasets
        plt.figure(figsize=(10, 6))

        for plot_df, label in zip(plot_dfs, labels):
            if not plot_df.empty:
                plt.plot(plot_df['RPM'], plot_df[selected_variable], 'o-', markersize=4, label=label)
            else:
                print(f"No data available to plot for {label}.")

        plt.xlabel('RPM')
        plt.ylabel(selected_variable)
        plt.title(f"{selected_variable} vs RPM at {variable_to_hold_constant} = {variable_value}")
        plt.grid(True)
        plt.legend()
        plt.show()

    elif choice == '2':
        # Functionality 2: Plot any two variables against each other at a specified RPM.
        # Process a single .dat file
        dat_file_path = input("Paste .dat file location: ")
        csv_file_path = input("Paste desired destination file path (filepath/filename.csv): ")
        df, segment_dfs_raw, rpm_values = process_dat_file(dat_file_path, csv_file_path)

        # Call the function to plot X vs Y at a specified RPM
        plot_xy_at_rpm(df, segment_dfs_raw, rpm_values)

    else:
        print("Invalid choice. Please run the script again and select either 1 or 2.")

if __name__ == "__main__":
    main()

