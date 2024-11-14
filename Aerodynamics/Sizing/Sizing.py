# %%
import numpy as np
import matplotlib.pyplot as plt


def new_S_scaled(S1, W1, W2):
    return S1 * (W2 / W1) ** (2 / 3)


def new_S(S1, W1, W2):
    return S1 * (W2 / W1)


MTOW = 25  # lb

c_rev1 = 13.3 / 12  # ft
b_rev1 = 40 / 12  # ft
S_rev1 = c_rev1 * b_rev1 * 2  # ft^2
AR_rev1 = 3
W_rev1 = 12.11  # lb

AR_rev_2 = 3
num_payload = 16
W_bottle = 0.5 + 0.04  # lb
W_payload = W_bottle * num_payload  # lb
W_rev2_min = MTOW - W_payload  # lb

W_rev2_max = MTOW

W_rev2_quarter = MTOW - ((W_payload) * (3 / 4))

S_rev2_min = new_S_scaled(S_rev1, W_rev1, W_rev2_min)
S_rev2_max = new_S_scaled(S_rev1, W_rev1, W_rev2_max)
S_rev2_quarter = new_S_scaled(S_rev1, W_rev1, W_rev2_quarter)

c_rev2_min = np.sqrt(S_rev2_min / 6)
b_rev2_min = c_rev2_min * AR_rev_2

c_rev2_max = np.sqrt(S_rev2_max / 6)
b_rev2_max = c_rev2_max * AR_rev_2

c_rev2_quarter = np.sqrt(S_rev2_quarter / 6)
b_rev2_quarter = c_rev2_quarter * AR_rev_2

# print(
#     f"For the minimum case, Rev2 would have a wing surface area of {S_rev2_min} ft^2,\na chord length of {c_rev2_min} ft, and a wingspan of {b_rev2_min} ft\n"
# )
# print(
#     f"For the maximum case, Rev2 would have a wing surface area of {S_rev2_max} ft^2,\na chord length of {c_rev2_max} ft, and a wingspan of {b_rev2_max} ft\n"
# )
# print(
#     f"For the quarter case, Rev2 would have a wing surface area of {S_rev2_quarter} ft^2,\na chord length of {c_rev2_quarter} ft, and a wingspan of {b_rev2_quarter} ft\n"
# )

# %%

weight_range = np.linspace(W_rev1 - 1, W_rev2_max + 1, 5)
surface_areas_scaled = [new_S_scaled(S_rev1, W_rev1, weight) for weight in weight_range]
surface_areas_unscaled = [new_S(S_rev1, W_rev1, weight) for weight in weight_range]

plt.figure(1)
plt.title("Rev2 Wing sizing based on proportional scaling")
plt.xlabel("Weight [lb]")
plt.ylabel("Wing area [$ft^{2}$]")
plt.plot(weight_range, surface_areas_unscaled, label="Unscaled", zorder=0)
plt.plot(weight_range, surface_areas_scaled, label="Scaled", linestyle="-.", zorder=0)
plt.plot()
plt.plot(
    [W_rev2_quarter, W_rev2_quarter],
    [surface_areas_unscaled[0], S_rev2_quarter],
    linestyle="dotted",
    color="grey",
)
plt.plot(
    [weight_range[0], W_rev2_quarter],
    [S_rev2_quarter, S_rev2_quarter],
    linestyle="dotted",
    color="grey",
)
plt.scatter(W_rev1, S_rev1, label="Rev1")
plt.scatter(W_rev2_min, S_rev2_min, label="Rev2 $W_{EMPTY}$")
plt.scatter(W_rev2_quarter, S_rev2_quarter, label="0.25%", color="r")
plt.scatter(W_rev2_max, S_rev2_max, label="Rev2 MTOW")
plt.text(
    20,
    8,
    f"Surface area = {S_rev2_quarter:.4} $ft^2$\nChord length = {c_rev2_quarter:.4} $ft$\nWing span = {b_rev2_quarter:.4} $ft$",
    bbox=dict(facecolor="grey", alpha=0.5),
)
plt.legend()

plt.show()
# %%
