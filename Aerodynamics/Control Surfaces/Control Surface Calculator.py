import numpy as np
import matplotlib.pyplot as plt


def thicknessFromLE(x, t):
    """Calculate airfoil thickness at a given position from the leading edge.

    This function computes the thickness of an airfoil at a specified
    distance from the trailing edge, based on the NACA 4-digit airfoil
    equation.

    Args:
        x (float): Distance from the trailing edge as a fraction of the chord length.
        t (float): Maximum thickness of the airfoil as a fraction of the chord length.

    Returns:
        float: The thickness of the airfoil at the specified position.
    """
    A = 0.2969
    B = 0.1260
    C = 0.3516
    D = 0.2843
    E = 0.1015
    return t / 0.1 * (A * np.sqrt(x) - B * x - C * x**2 + D * x**3 - E * x**4)


def surfaceAngleFromLE(x, t):
    """Calculate airfoil surface angle at a given position from the leading edge.

    This function computes the surface angle of an airfoil at a specified
    distance from the leading edge, based on the NACA 4-digit airfoil
    equation.

    Args:
        x (float): Distance from the leading edge as a fraction of the chord length.
        t (float): Maximum thickness of the airfoil as a fraction of the chord length.

    Returns:
        float: The surface angle of the airfoil at the specified position.
    """
    A = 0.1485
    B = 0.126
    C = 0.7032
    D = 0.8529
    E = 0.4060
    return t / 0.1 * (A * x ^ (-0.5) - B - C * x + D * x**2 - E * x**3)


maxThicknessPercent = 0.15  # From NACA 0015 max thickness is 15% of chord length
chord = 16  # in
aileronChord = 2.5  # in
aileronDistND = 1 - (aileronChord / chord)
aileronBaseThicknessND = thicknessFromLE(aileronDistND, maxThicknessPercent)
aileronBaseThickness = aileronBaseThicknessND * chord

print(f"\nThe thickness of the aeileron at its base is {aileronBaseThickness} inches\n")

dist = np.linspace(0, 16, 32)


# plt.plot(dist, chord * thicknessFromLE(dist / chord, maxThicknessPercent))
# plt.axvline(x=16-2.5)
# plt.axhline(y=0.85)
# plt.show()
