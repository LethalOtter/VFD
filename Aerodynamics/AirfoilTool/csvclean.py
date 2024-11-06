from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd

Tk().withdraw()
file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
print(f"Selected file: {file_path}")

with open(file_path, 'r') as f:
    lines = f.readlines()

header_info = {}

for line in lines[:9]:
    if ',' in line:
        key, value = line.strip().split(',', 1)
        header_info[key] = value

if '\n' in lines:
    data_start_index = lines.index('\n') + 1
else:
    raise ValueError("No blank line found to separate header and data sections")

data_df = pd.read_csv(file_path, skiprows=data_start_index)

for key, value in header_info.items():
    data_df[key] = value

print(data_df.to_string())
