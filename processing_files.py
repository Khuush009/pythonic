import pandas as pd 
import os 

def process_files(source_folder, destination_folder):
    """
    Reads data from multiple files in a folder, calculates salary statistics, and creates a new CSV file.

    Args:
        source_folder: Path to the folder containing the input files.
        destination_folder: Path to the folder where the output CSV file will be saved.
    """

    all_salaries = []
    all_data=[]
    # Check if the folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Folder '{source_folder}' does not exist.")
        return
    
    for filename in os.listdir(source_folder):
        if filename.endswith(".dat"):
            filepath = os.path.join(source_folder, filename)
            # Read data from the file based on its format (adjust reading logic accordingly)
            try:
                with open(filepath, "r") as file:
                    df = pd.read_csv(file, delimiter='\t')
            except pd.errors.ParserError as e:
                print(f"Error parsing '{filename}': {e}")
                continue
            float_sal_values = df['basic_salary'].apply(pd.to_numeric, errors='coerce').tolist()
            all_salaries.extend(float_sal_values)
            all_data.append(df)

    if not all_salaries:
        print("No salary data found in the files.")
        return

    # Calculate statistics
    average_salary = df['basic_salary'].mean()
    second_highest_salary = df['basic_salary'].nlargest(2).iloc[-1] if not df.empty else None

    # Create a list containing footer information
    footer_data = [f"Average Salary: {average_salary:.2f}", f"Second Highest Salary: {second_highest_salary:.2f}"] if second_highest_salary else [f"Average Salary: {average_salary:.2f}"]

    # Convert footer list to DataFrame
    footer_df = pd.DataFrame([footer_data])

    df['gross_salary'] = df['basic_salary'] + df['allowances']
    
    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat([df, footer_df], ignore_index=True)

    output_filename = "result.csv"  # Customize filename
    output_filepath = os.path.join(destination_folder, output_filename)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_filepath, index=False)

    print(f"Data from .dat files combined and saved to '{output_filename}'.")
            
if __name__ == "__main__":
    source_folder = "input/"  # Replace with your source folder path
    destination_folder = "output/"  # Replace with your destination folder path
    process_files(source_folder, destination_folder)

    print("CSV file created successfully!")