import csv
import sys
import os

bu = sys.argv[3].upper()
localized_path = sys.argv[1]
info_path = sys.argv[2] + os.sep
filtered_path = sys.argv[2] + os.sep + 'FilteredCSV' + os.sep
silent = sys.argv[3] == 'on'
dry_run = sys.argv[4] == 'on'

if silent:
   sys.stdout=open(os.devnull, 'w')

files = [file for file in os.listdir(localized_path) if os.path.isfile(os.path.join(localized_path, file))]

if not os.path.exists(filtered_path):
    os.makedirs(filtered_path)

for file in files:
    localized = []
    values = {}
    with open(localized_path + file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = reader.next()
        
        for csv_key in header:
            if bu in csv_key:
                value_key  = 'value_' + csv_key.split('-')[-1].lower()
                values[value_key] = header.index(csv_key)

        if len(values) == 0:
            continue

        for row in reader:
            localized_object = {'key': row[0]}
            for (value_key, value_index) in values.items():
                value = row[value_index]
                if len(value) == 0:
                    continue
                localized_object[value_key] = row[value_index]

            # only key, no need to add
            if len(localized_object) > 1:
                localized.append(localized_object)

    if len(localized) == 0:
        continue

    with open(filtered_path + file, 'w') as csvfile:
        values_and_key = ['key']
        values_and_key.extend(values.keys())

        writer = csv.DictWriter(csvfile, values_and_key)
        writer.writeheader()
        writer.writerows(localized)

    with open(info_path + 'lang.info', 'w') as info_file:
        info_file.write(','.join(values.keys()))
