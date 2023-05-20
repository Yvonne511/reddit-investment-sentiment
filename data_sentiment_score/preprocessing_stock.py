import os
import json
import csv
import re


folder = "gme"


with open(os.path.join(folder, "price_raw.json")) as json_file:
    data = json.load(json_file)

pattern = r"...............9..."
pattern = r"...............9..."

with open(os.path.join(folder, "price.csv"), mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(['datetime', 'close-price'])
    for item in reversed(data):
        if re.match(pattern, item['datetime']):
            writer.writerow([item['datetime'][:16], item['close']])
