import numpy as np
# Determine attitude angle given chord length, c_l, and prop diameter
def attitude_angle(chord_length, coeff_lift, prop_diameter):
    pitch = np.arctan((4 * chord_length * coeff_lift)/(np.pi * prop_diameter))
    return(round((pitch*180/np.pi),3))

# TEST CLARK Y AIRFOIL
for i in (0.1,0.2,0.3,0.4,0.5):
    print(f'c_l: {i}   pitch angle: {attitude_angle(2.05,i,1.25)} degrees')