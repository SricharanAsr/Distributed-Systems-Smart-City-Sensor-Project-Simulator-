import os
import json
import csv
from typing import List, Dict, Any


def export_cached_data_to_csv(cache_dir: str = "data_cache", output_file: str = "simulation_results.csv") -> bool:
    """
    Reads all JSON files in the cache directory and consolidates them into a single CSV.
    """
    if not os.path.exists(cache_dir):
        print(f"Error: Cache directory '{cache_dir}' does not exist.")
        return False

    all_data: List[Dict[str, Any]] = []
    
    # Load all json files
    for filename in os.listdir(cache_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(cache_dir, filename)
            try:
                with open(filepath, "r") as f:
                    all_data.append(json.load(f))
            except Exception as e:
                print(f"Warning: Failed to read {filename}: {e}")

    if not all_data:
        print("No data found to export.")
        return False

    # Extract all unique keys for header
    headers = set()
    for entry in all_data:
        headers.update(entry.keys())
    
    sorted_headers = sorted(list(headers))

    try:
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted_headers)
            writer.writeheader()
            for row in all_data:
                writer.writerow(row)
        
        print(f"Successfully exported {len(all_data)} records to {output_file}")
        return True
    except Exception as e:
        print(f"Error: Failed to write CSV: {e}")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate cached simulation data into CSV")
    parser.add_argument("--dir", default="data_cache", help="Directory containing JSON cache files")
    parser.add_argument("--out", default="simulation_results.csv", help="Output CSV filename")
    
    args = parser.parse_args()
    export_cached_data_to_csv(args.dir, args.out)
