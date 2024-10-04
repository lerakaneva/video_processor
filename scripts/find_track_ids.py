import pandas as pd
import argparse
import os

def find_and_save_track_ids(csv_path_1, csv_path_2, common_output_path=None, diff_output_path_1=None, diff_output_path_2=None):
    """
    Find and save rows with common and different track IDs between two CSV files.

    Parameters:
    - csv_path_1 (str): Path to the first CSV file.
    - csv_path_2 (str): Path to the second CSV file.
    - common_output_path (str): Path to save the output CSV containing rows from the first file with track IDs common to both files.
    - diff_output_path_1 (str): Path to save the output CSV containing rows from the first file with track IDs not present in the second file.
    - diff_output_path_2 (str): Path to save the output CSV containing rows from the second file with track IDs not present in the first file.

    The function identifies track IDs present in both CSV files, as well as track IDs unique to each file,
    and saves the respective rows to separate output files if their paths are provided.
    """
    
    # Load the CSV files into pandas DataFrames
    df1 = pd.read_csv(csv_path_1)
    df2 = pd.read_csv(csv_path_2)

    # Ensure both DataFrames have a 'track_id' column
    if 'track_id' not in df1.columns or 'track_id' not in df2.columns:
        raise ValueError("Both CSV files must contain a 'track_id' column")

    # Find common track_ids
    common_track_ids = pd.merge(df1[['track_id']], df2[['track_id']], on='track_id')

    # Save rows with common track_ids from the first CSV if output path is provided
    if common_output_path and not common_track_ids.empty:
        common_ids_list = common_track_ids['track_id'].unique().tolist()
        print(f"Common track_ids found: {common_ids_list}")
        
        # Filter rows in df1 with common track_ids
        filtered_rows_common = df1[df1['track_id'].isin(common_ids_list)]
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(common_output_path), exist_ok=True)

        # Save the filtered rows to a common output file
        filtered_rows_common.to_csv(common_output_path, index=False)
        print(f"Rows with common track_ids have been saved to {common_output_path}")
    else:
        print("No common track_ids found or common output path not provided.")
    
    # Find track_ids that are in df1 but not in df2 if diff_output_path_1 is provided
    if diff_output_path_1:
        diff_track_ids_1 = df1[~df1['track_id'].isin(df2['track_id'])]
        if not diff_track_ids_1.empty:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(diff_output_path_1), exist_ok=True)
            
            diff_track_ids_1.to_csv(diff_output_path_1, index=False)
            print(f"Rows with track_ids only in the first file have been saved to {diff_output_path_1}")
        else:
            print("No track_ids unique to the first file were found.")

    # Find track_ids that are in df2 but not in df1 if diff_output_path_2 is provided
    if diff_output_path_2:
        diff_track_ids_2 = df2[~df2['track_id'].isin(df1['track_id'])]
        if not diff_track_ids_2.empty:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(diff_output_path_2), exist_ok=True)
            
            diff_track_ids_2.to_csv(diff_output_path_2, index=False)
            print(f"Rows with track_ids only in the second file have been saved to {diff_output_path_2}")
        else:
            print("No track_ids unique to the second file were found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and save track IDs between two CSV files.")
    parser.add_argument("--csv_path_1", help="Path to the first CSV file.")
    parser.add_argument("--csv_path_2", help="Path to the second CSV file.")
    parser.add_argument("--common_output_path", help="Path to save rows from the first file with track IDs common to both files.")
    parser.add_argument("--diff_output_path_1", help="Path to save rows from the first file with track IDs not present in the second file.")
    parser.add_argument("--diff_output_path_2", help="Path to save rows from the second file with track IDs not present in the first file.")
    args = parser.parse_args()

    find_and_save_track_ids(args.csv_path_1, args.csv_path_2, args.common_output_path, args.diff_output_path_1, args.diff_output_path_2)
