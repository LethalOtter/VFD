import pandas as pd
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Cleaning up DAT file and converting it into a pandas df


def gather_dat_header(dat_file_path):
    with open(dat_file_path, "r") as dat_file:
        for line in dat_file:
            if "PROP RPM" in line.strip():
                next(dat_file)
                header_variables = dat_file.readline().strip().split()
                header_variables.insert(0, "RPM")
                header_units = dat_file.readline().strip().split()
                header_units.insert(0, "-")
                return header_variables, header_units


def is_rpm_set(line, units):
    return line.strip().split() == units[1:]


def process_data_sets(dat_file, units):
    RPM_multiplier = 1
    data_set = False
    data = []
    for line in dat_file:
        # not flagged as a data set yet, but identifies that the following line begins a data set
        if not data_set and is_rpm_set(line, units):
            data_set = True
            continue
        # flagged as a data set, and current line is still in the data set
        if data_set and line.strip():
            row_data = line.strip().split()
            row_data.insert(0, RPM_multiplier * 1000)
            data.append(row_data)
        # still flagged as data set, but current line is not in the data set
        if data_set and not line.strip():
            data_set = False
            RPM_multiplier += 1
    return data


def make_unique(column_names):
    seen = {}
    for i, name in enumerate(column_names):
        if name in seen:
            seen[name] += 1
            column_names[i] = f"{name}.{seen[name]}"
        else:
            seen[name] = 0
    return column_names


def convert_dat_to_dataframe(dat_file_path):
    parameters, units = gather_dat_header(dat_file_path)
    with open(dat_file_path, "r") as dat_file:
        data = process_data_sets(dat_file, units)

    unique_parameters = make_unique(parameters)
    df = pd.DataFrame(data, columns=unique_parameters)
    df.drop(columns=["PWR", "Torque", "Thrust"], inplace=True)

    df = df.apply(pd.to_numeric, errors="coerce")
    return df


if __name__ == "__main__":
    Tk().withdraw()
    dat_file_path = askopenfilename(filetypes=[("Dat file", "*.dat")])
    df = convert_dat_to_dataframe(dat_file_path)
    print(df)
