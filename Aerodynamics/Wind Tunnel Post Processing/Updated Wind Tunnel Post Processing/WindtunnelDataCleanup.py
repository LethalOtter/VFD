#Chatgpt is actually good at coding I guess

def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    
    filtered_lines = []
    for line in lines:
        columns = line.strip().split('\t')  # Split by tab to get rows
        if columns:  # Ensure the line is not empty
            last_column_values = columns[-1].split(',')  # Split the last column by comma
            if last_column_values[-1].strip() != '1.000':  # Check the last value in the last column
                filtered_lines.append(line)
    
    with open(output_filename, 'w') as outfile:
        outfile.writelines(filtered_lines)

# Example usage
input_file = "VFD\Des2Wind30mpsDataRun000.TXT"
output_file = "CleanedDes2Wind30mpsDataRun000.TXT"
process_file(input_file, output_file)