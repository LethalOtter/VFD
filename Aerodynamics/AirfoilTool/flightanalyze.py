import pandas as pd
import numpy as np
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
            existing_df = pd.concat([existing_df, new_row_df], ignore_index=True)
            return existing_df

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

    # Check if the interpolation was successful
    if thrust_matched_interpolation.empty:
        print("Interpolation failed: No valid data found for thrust.")
        return None  # Handle as needed

    return thrust_matched_interpolation["PWR"][0] * 4


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
    print(f"{Cl_needed=}")
    interpolated_airfoil_df = pd.DataFrame(columns=airfoil_df.columns)
    interpolated_airfoil_df = interpolate_and_add_row(
        airfoil_df, "Cl", Cl_needed, interpolated_airfoil_df
    )

    if interpolated_airfoil_df.empty:
        print("Interpolation failed: No valid data found.")
        return pd.DataFrame(
            columns=airfoil_df.columns
        )  # Return an empty DataFrame or handle as needed

    return interpolated_airfoil_df


if __name__ == "__main__":
    Tk().withdraw()
    dat_file_path = askopenfilename(filetypes=[("Dat file", "*.dat")])
    csv_file_path = askopenfilename(filetypes=[("Csv file", "*.csv")])

    prop_df = pc.convert_dat_to_dataframe(dat_file_path)
    airfoil_df = af.load_csv(csv_file_path)
    airfoil_df.drop(columns=["Polar key", "Airfoil", "Url"], inplace=True)
    airfoil_df = airfoil_df.apply(pd.to_numeric, errors="coerce")

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
    print(f"Vstall = {V_stall} m/s")

    interpolated_airfoil_data = aerodynamic_state(
        rho, V_initial[1], wing_area, weight, airfoil_df
    )

    print(interpolated_airfoil_data)
    Lift_drag = calc_drag(
        rho, V_initial[1], wing_area, interpolated_airfoil_data["Cd"][0]
    )
    drag = "Thrust", Lift_drag + est_fuselage_drag
    print(f"Drag = {drag}")

    pwr = find_power(prop_df, V_initial, drag)
    print(f"{pwr} Watts")
