import csv

def export_to_csv(data, filepath):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)

import json

def export_to_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)
