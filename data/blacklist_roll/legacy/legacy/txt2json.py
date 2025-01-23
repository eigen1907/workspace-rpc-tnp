import argparse
import json

def convert_file(input_filename, output_filename):
    # Read the input data from the text file
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Process each line to extract the necessary information and format it
    formatted_list = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            formatted_list.append(parts[1])

    formatted_list.sort()

    # Write the result to a JSON file
    with open(output_filename, 'w') as file:
        json.dump(formatted_list, file, indent=4)

    print(f"Data has been successfully written to {output_filename}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert a text file to a JSON file.')
    parser.add_argument('-i', '--inputfile', type=str, required=True, help='The input text file')
    parser.add_argument('-o', '--outputfile', type=str, required=True, help='The output JSON file')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    convert_file(args.inputfile, args.outputfile)