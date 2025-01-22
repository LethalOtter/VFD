import pandas as pd
import numpy as np
import scipy.interpolate as int
import propclean as pc
import airfoil_df as af
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# SET SPEED CALCULATIONS

# WING

# INITIALIZE
# Wing geometery DONE
# Airfoil DONE
# CG, CP

# ITERATIONS
# Choose airspeed
# Find CL neccesary for sufficient lift at chosen airspeed
# Find AOA neccesary for CL
# Find CD --> Drag
# Find CM --> Calculate the CM_flap needed to maintain stability (need weight location estimation first)
# Find new CL, CD
# Repeat until converges to find trim AOA and delta_flaps at airspeed

# PROPELLOR

# Interpolate within each RPM set to generate data points at constant flight speed DONE
# Use data points to generate function giving power and torque as a function of thrust DONE
# Use Drag as Thrust to determine power and torque and compare them to their limits
# If Drag is greater than thrust reduce airspeed by some step size and repeat calculations
# If Drag is less than thrust increase airspeed by some step size and repate calculations

# Repeat calculations untill convergence criteria is met!!!

# ADD ONS

# Adjusting cp location relative to cg, checking static margin for both We and MTOW
# Calculating cp location instead of estimating at C_1/4
# Adjusting flap size
# Adjusting airfoil
# Using low fidelity cfd methods from aerosandbox to optimize airfoil design
# Using low fidelity cfd methods from aerosandbox to wing placement
# Account for non axial aiflow effects on propellors
# Introduce efficiency factor estimation/relationship
# Record data sets for future use with ML estimation to reduce iterations


def load_data(file_path, loader_func, drop_columns=None):
    df = loader_func(file_path)
    if drop_columns:
        df.drop(columns=drop_columns, inplace=True)
        df.dropna(inplace=True)
    return df.apply(pd.to_numeric, errors="coerce")


def interpolate_column_value(df, querry_column, querry, resultant_column):
    f = int.interp1d(df[querry_column], df[resultant_column], fill_value="extrapolate")
    return f(querry)


def filter_dataframe_by_column_value(df, column_name, value):
    return df[df[column_name] == value]


def interpolate_row(df, querry_column, querry):
    min_val = df[querry_column].min()
    max_val = df[querry_column].max()

    if querry < min_val or max_val < querry:
        return None

    lower_row = df[df[querry_column] <= querry].iloc[-1]
    upper_row = df[df[querry_column] > querry].iloc[-1]

    weight = (querry - lower_row[querry_column]) / (
        upper_row[querry_column] - lower_row[querry_column]
    )

    return lower_row + weight * (upper_row - lower_row)


def constant_value_df(constant_parameter, constant_value):
    running = True
    interpolated_prop_df = pd.DataFrame(columns=prop_df.columns)
    rpm = 1000
    while running:
        filtered_prop_df = filter_dataframe_by_column_value(prop_df, "RPM", rpm)
        if filtered_prop_df.empty:
            break
        interpolated_prop_df = pd.concat(
            [
                interpolated_prop_df,
                interpolate_row(filtered_prop_df, constant_parameter, constant_value),
            ],
            ignore_index=True,
        )

        rpm += 1000
    return interpolated_prop_df


def find_power(df, V_tup, T_tup):
    V_constant_df = constant_value_df(V_tup[0], V_tup[1])
    print(V_constant_df)
    pwr = interpolate_column_value(V_constant_df, T_tup[0], T_tup[1] / 4, "Pwr")
    return pwr * 4


def calc_lift(rho, v, S, cl):
    return 0.5 * rho * v**2 * S * cl


def calc_Cl(rho, v, S, L):
    return L / (0.5 * rho * v**2 * S)


def calc_drag(rho, v, S, cd):
    return 0.5 * rho * v**2 * S * cd


def calc_moment(rho, v, S, c, cm):
    return 0.5 * rho * v**2 * S * c * cm


def aerodynamic_state(rho, V, S, W, airfoil_df):
    Cl_needed = calc_Cl(rho, V, S, W)
    interpolated_airfoil_df = interpolate_row(airfoil_df, "Cl", Cl_needed)

    if interpolated_airfoil_df.empty:
        print("Interpolation failed: No valid data found.")
        return pd.DataFrame(
            columns=airfoil_df.columns
        )  # Return an empty DataFrame or handle as needed

    return interpolated_airfoil_df


if __name__ == "__main__":
    # Tk().withdraw()
    # prop_dat_file_path = askopenfilename(filetypes=[("Dat file", "*.dat")])
    # airfoil_csv_file_path = askopenfilename(filetypes=[("Csv file", "*.csv")])

    prop_dat_file_path = "/Users/alecestrada/Downloads/PER3_20x10.dat"
    airfoil_csv_file_path = "/Users/alecestrada/Downloads/xf-naca0015-il-200000.csv"

    prop_df = load_data(prop_dat_file_path, pc.convert_dat_to_dataframe)
    airfoil_df = load_data(
        airfoil_csv_file_path, af.load_csv, drop_columns=["Polar key", "Airfoil", "Url"]
    )

    rho = 1.223  # kg/m^3
    wing_chord = 1.279 * 0.3048  # Meters  0.389
    wing_span = 4 * 0.3048  # Meters  1.2192
    wing_area = wing_chord * wing_span  # Meters^2  0.474
    weight = 18.5 * (0.3048 * 9.8)  # Newtons  55.26
    x_LE = -1 * (3 / 12 * 0.3048)  # Meters
    x_ac = x_LE - wing_chord * 0.25  # Meters
    SM = x_ac / wing_chord
    V_initial = "V", 100 * 0.44704  # m/s
    est_fuselage_drag = (
        0.298 * 0.5 * rho * V_initial[1] ** 2 * (wing_chord * 0.75) ** 2
    )  # Bullet approximation

    # P_hover = 500  # Watts
    # P_limit = P_hover * 2 * 0.8  # Watts

    V_stall = np.sqrt((2 * weight) / (rho * wing_area / 2 * airfoil_df["Cl"].max()))
    print(f"\nVstall = {V_stall / 0.44704} mph\n")

    interpolated_airfoil_data = aerodynamic_state(
        rho, V_initial[1], wing_area, weight, airfoil_df
    )

    Lift_drag = calc_drag(rho, V_initial[1], wing_area, interpolated_airfoil_data["Cd"])
    drag = "Thrust", Lift_drag + est_fuselage_drag
    print(f"\nDrag = {drag[1]}Newtons\n")

    pwr = find_power(prop_df, V_initial, drag)
    print(f"\nPower {pwr} Watts\n")
