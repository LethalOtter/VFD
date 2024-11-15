import pandas as pd
import csv

# Borrowed and modified from Ore cuz he's super duper cool


def gather_dat_header(dat_file_path):
    with (open(dat_file_path, "r") as dat_file,):
        for line in dat_file:
            if "PROP RPM" in line.strip():
                next(dat_file)
                header_variables = dat_file.readline().strip().split()
                header_units = dat_file.readline().strip().split()
                return header_variables, header_units


def is_rpm_set(line, units):
    # units_str = " ".join(units)
    # new_line = " ".join(line.strip().split())
    return line.strip().split() == units


def process_data_sets(dat_file, csv_writer, units):
    data_set = False
    for line in dat_file:
        # not flagged as a data set yet, but identifies that the following line begins a data set
        if not data_set and is_rpm_set(line, units):
            data_set = True
            continue
        # flagged as a data set, and current line is still in the data set
        if data_set and line.strip():
            csv_writer.writerow(line.strip().split())
        # still flagged as data set, but current line is not in the data set
        if data_set and not line.strip():
            csv_writer.writerow("")
            data_set = False


def convert_dat_to_csv(dat_file_path, csv_file_path, parameters, units):
    with (
        open(dat_file_path, "r") as dat_file,
        open(csv_file_path, "w", newline="") as csv_file,
    ):
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(parameters)
        csv_writer.writerow(units)
        process_data_sets(dat_file, csv_writer, units)


dat_file_path = "Aerodynamics/Sizing/PER3_105x45.dat"
csv_file_path = "Aerodynamics/Sizing/PER3_105x45.csv"


parameters, units = gather_dat_header(dat_file_path)

convert_dat_to_csv(dat_file_path, csv_file_path, parameters, units)
