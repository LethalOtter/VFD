import numpy as np


# Determine attitude angle given chord length, c_l, and prop diameter
def attitude_angle(chord_length, coeff_lift, prop_diameter):
    """
    This function determines attitude angle of a biplane quadcopter in hover. Pitch angle is measured such that at zero pitch,
    the propellor's thrust vector is pointing straight up. Positive pitch indicates a forward pitch of the nose, while a
    negative pitch indicates a backward nose pitch.

    :param chord_length: Chord length of wing in feet
    :param coeff_lift: Nondimensional infinite coefficient of lift for one wing
    :param prop_diameter: Propellor diameter in feet
    :returns: Pitch angle in degrees
    """
    pitch = np.arctan((4 * chord_length * coeff_lift) / (np.pi * prop_diameter))
    return round((pitch * 180 / np.pi), 3)


# TEST CLARK Y AIRFOIL
for i in (0.1, 0.2, 0.3, 0.4, 0.5):
    print(f"c_l: {i}   pitch angle: {attitude_angle(2.05,i,1.25)} degrees")
