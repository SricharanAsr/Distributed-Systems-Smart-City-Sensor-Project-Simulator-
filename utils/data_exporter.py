import csv

def export_to_csv(data, filepath):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)

import json

def export_to_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

"""
The data exporter provides isolated mechanisms to bypass API transmission and write directly to disk.
"""
