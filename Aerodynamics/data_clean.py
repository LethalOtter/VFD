import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define custom headers and units globally
custom_header = [
    "V",
    "J",
    "Pe",
    "Ct",
    "Cp",
    "PWR",
    "Torque",
    "Thrust",
    "PWR",
    "Torque",
    "Thrust",
    "THR/PWR",
    "Mach",
    "Reyn",
    "FOM",
]
units = [
    "(mph)",
    "(Adv_Ratio)",
    "-",
    "-",
    "-",
    "(Hp)",
    "(In-Lbf)",
    "(Lbf)",
    "(W)",
    "(N-m)",
    "(N)",
    "(g/W)",
    "-",
    "-",
    "-",
]


def convert_dat_to_csv_with_custom_header(dat_file_path, csv_file_path):
    with open(dat_file_path, "r") as dat_file, open(
        csv_file_path, "w", newline=""
    ) as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(custom_header)
        csv_writer.writerow(units)

        # Define criteria for lines to skip
        header_str = " ".join(custom_header)
        units_str = " ".join(units)

        # Read Lines
        for line in dat_file:
            # Strip whitespace from the line and check if header and units are repeated
            if line.strip() == header_str or line.strip() == units_str:
                continue  # Skip this line if it matches either the header or units

            # write the line to the CSV
            row = line.strip().split()
            csv_writer.writerow(row)

    print(f"Conversion complete. Data saved to {csv_file_path}")


dat_file_path = input("Paste .dat file location : ")
csv_file_path = input("Paste desired destination file path(filepath/filename.csv) : ")
convert_dat_to_csv_with_custom_header(dat_file_path, csv_file_path)

# Load the new CSV into a DataFrame
df = pd.read_csv(csv_file_path, header=None)

# Separate the first two rows
first_two_rows = df.iloc[1:2].copy()

# Remove any rows that match either the custom header or units by converting each row to a string
# It will end up being read as a null space and be removed
remaining_rows = df.iloc[2:]
filtered_rows = remaining_rows[
    ~remaining_rows.apply(
        lambda row: " ".join(map(str, row.values))
        in [" ".join(custom_header), " ".join(units)],
        axis=1,
    )
]

# Concatenate the second rows back with the filtered data
df_cleaned = pd.concat([first_two_rows, filtered_rows], ignore_index=True)

# Rename columns based on the custom header
df_cleaned.columns = [
    "V(mph)",
    "J(Adv_Ratio)",
    "Pe",
    "Ct",
    "Cp",
    "PWR(Hp)",
    "Torque(In-Lbf)",
    "Thrust(Lbf)",
    "PWR(W)",
    "Torque(N-m)",
    "Thrust(N)",
    "THR/PWR(g/W)",
    "Mach",
    "Reyn",
    "FOM",
]
# null check
# df_cleaned.dropna(axis=1, how='all', inplace=True)

# Save the cleaned DataFrame to a new CSV file
cleaned_csv_path = csv_file_path  # Adjust the path as needed
df_cleaned.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned data saved to {cleaned_csv_path}")
# x=input('Input X axis \n["V(mph)", "J(Adv_Ratio)", "Pe", "Ct", "Cp", "PWR(Hp)", "Torque(In-Lbf)", "Thrust(Lbf)", "PWR(W)", "Torque(N-m)", "Thrust(N)", "THR/PWR(g/W)", "Mach", "Reyn", "FOM"] : ')
# y=input('Input Y axis \n["V(mph)", "J(Adv_Ratio)", "Pe", "Ct", "Cp", "PWR(Hp)", "Torque(In-Lbf)", "Thrust(Lbf)", "PWR(W)", "Torque(N-m)", "Thrust(N)", "THR/PWR(g/W)", "Mach", "Reyn", "FOM"] : ')
# z=input('Input Z axis \n[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000] : ')

df = pd.read_csv(cleaned_csv_path)
# Ct = df.iloc[:, 3]  # Assuming the RPM values are in the 3rd column (Ct)
# df['RPM'] = Ct  # Create an 'RPM' column in df for filtering convenience
column_map = {
    "V(mph)": "V(mph)",
    "J(Adv_Ratio)": "J(Adv_Ratio)",
    "Pe": "Pe",
    "Ct": "Ct",
    "Cp": "Cp",
    "PWR(Hp)": "PWR(Hp)",
    "Torque(In-Lbf)": "Torque(In-Lbf)",
    "Thrust(Lbf)": "Thrust(Lbf)",
    "PWR(W)": "PWR(W)",
    "Torque(N-m)": "Torque(N-m)",
    "Thrust(N)": "Thrust(N)",
    "THR/PWR(g/W)": "THR/PWR(g/W)",
    "Mach": "Mach",
    "Reyn": "Reyn",
    "FOM": "FOM",
}
# Prompt the user for input columns and RPM value
x = input(
    'Input X axis \n["V(mph)", "J(Adv_Ratio)", "Pe", "Ct", "Cp", "PWR(Hp)", "Torque(In-Lbf)", "Thrust(Lbf)", "PWR(W)", "Torque(N-m)", "Thrust(N)", "THR/PWR(g/W)", "Mach", "Reyn", "FOM"] : '
)
y = input(
    'Input Y axis \n["V(mph)", "J(Adv_Ratio)", "Pe", "Ct", "Cp", "PWR(Hp)", "Torque(In-Lbf)", "Thrust(Lbf)", "PWR(W)", "Torque(N-m)", "Thrust(N)", "THR/PWR(g/W)", "Mach", "Reyn", "FOM"] : '
)
z = int(input("Input RPM value\n[1000, 2000, 3000, ...] : "))

rpm_rows = df[df["Ct"].apply(lambda x: str(x).isdigit())].index

start_idx = None
for idx in rpm_rows:
    rpm_value = int(df.loc[idx, "Ct"])  # Integer
    if rpm_value == z:
        start_idx = idx + 1
        break

# RPM Check
if start_idx is not None:
    next_rpm_index = (
        rpm_rows[rpm_rows > start_idx].min()
        if any(rpm_rows > start_idx)
        else df.shape[0]
    )  # Find the next RPM index to determine the end of the current RPM section
    rpm_data = df.iloc[start_idx:next_rpm_index].reset_index(
        drop=True
    )  # Slice the data for the current RPM range
    x_data = pd.to_numeric(rpm_data[column_map[x]], errors="coerce")
    y_data = pd.to_numeric(rpm_data[column_map[y]], errors="coerce")
    print(f"Data for X-axis ({x}):\n{x_data}")
    print(f"Data for Y-axis ({y}):\n{y_data}")

    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, marker="o", linestyle="-", color="b")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f"Plot of {y} vs {x} at RPM {z}")

    plt.grid(True)
    plt.xlim(
        [x_data.min() - 0.1 * abs(x_data.min()), x_data.max() + 0.1 * abs(x_data.max())]
    )  # To adjust plot grid size based on range
    plt.ylim(
        [y_data.min() - 0.1 * abs(y_data.min()), y_data.max() + 0.1 * abs(y_data.max())]
    )

    # Show the plot
    plt.show()
else:
    print(f"RPM {z} not found in the dataset.")
