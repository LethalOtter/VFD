import pandas as pd
import propclean as pc
import matplotlib.pyplot as plt
import Aerodynamics
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# SET SPEED CALCULATIONS

# WING
# Choose airspeed
# Find CL neccesary for sufficient lift at chosen airspeed
# Find AOA neccesary for CL
# Find CD --> Drag
# Find CM --> Calculate the CM_flap needed to maintain stability
# Find new CL, CD
# Repeat until converges to find trim AOA and delta_flaps at airspeed

# PROPELLOR
# Interpolate within each RPM set to generate data points at constant flight speed DONE
# Use data points to generate function giving power and torque as a function of thrust DONE
# Use Drag as Thrust to determine power and torque and compare them to their limits
# If Drag is greater than thrust reduce airspeed by some step size and repeat calculations
# If Drag is less than thrust increase airspeed by some step size and repate calculations

# Repeat calculations untill convergence criteria is met


def filter_dataframe_by_column_value(df, column_name, value):
    return df[df[column_name] == value]


def interpolate_and_add_row(df, column_name, value, existing_df):
    min_val = df[column_name].min()
    max_val = df[column_name].max()

    if min_val <= value <= max_val:
        lower_bound = df[df[column_name] <= value]
        upper_bound = df[df[column_name] > value]

        if not lower_bound.empty and not upper_bound.empty:
            lower_row = lower_bound.iloc[-1]
            upper_row = upper_bound.iloc[0]
            new_row = lower_row + (upper_row - lower_row) * (
                (value - lower_row[column_name])
                / (upper_row[column_name] - lower_row[column_name])
            )
            new_row_df = pd.DataFrame([new_row])
            return pd.concat([existing_df, new_row_df], ignore_index=True)

    return existing_df


def constant_value_df(constant_parameter, constant_value):
    running = True
    interpolated_prop_df = pd.DataFrame(columns=prop_df.columns)
    rpm = 1000
    while running:
        filtered_prop_df = filter_dataframe_by_column_value(prop_df, "RPM", rpm)
        if filtered_prop_df.empty:
            break
        interpolated_prop_df = interpolate_and_add_row(
            filtered_prop_df, constant_parameter, constant_value, interpolated_prop_df
        )
        rpm += 1000
    return interpolated_prop_df


def find_power(df, V, T):
    V_constant_df = constant_value_df(V[0], V[1])
    thrust_matched_interpolation = pd.DataFrame(columns=df.columns)
    thrust_matched_interpolation = interpolate_and_add_row(
        V_constant_df, T[0], T[1] / 4, thrust_matched_interpolation
    )
    return thrust_matched_interpolation["PWR"][0] * 4


if __name__ == "__main__":
    Tk().withdraw()
    dat_file_path = askopenfilename(filetypes=[("Dat file", "*.dat")])
    prop_df = pc.convert_dat_to_dataframe(dat_file_path)

    V_initial = ("V", 30)
    T_initial = ("Thrust", 2 / 2.21 * 9.8)

    pwr = find_power(prop_df, V_initial, T_initial)
    print(f"{pwr} Watts")
