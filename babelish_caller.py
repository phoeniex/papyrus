import subprocess
import sys
import os
import csv

def call_babelish(lang_config):
    command = 'babelish ' + platform_string + ' --filename=' + csv_path + ' --keys_column=0 --langs=' + lang_config + ' --output_dir=' + output_path
    subprocess.call(command, shell=True)

csv_original_path = sys.argv[1] + os.sep + 'merged.csv'
csv_path = sys.argv[1] + os.sep + 'merged_removed.csv'
info_path = sys.argv[1] + os.sep + 'lang.info'
output_path = sys.argv[2]
platform = sys.argv[3].lower()
platform_string = 'csv2strings' if platform == 'ios' else 'csv2android'

lang_list = []
with open(info_path) as info_file:
    lang_list = info_file.readline().split(',')

# Remove 'key' (header of each file) from merged csv file
localized = []
with open(csv_original_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    localized.append(reader.next())

    for row in reader:
        if row[0] != 'key':
            localized.append(row)

with open(csv_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(localized)

for lang in lang_list:
    lang_config = lang + ':' + lang.split('_')[-1]
    call_babelish(lang_config)

# Call to set base language, always use first language
call_babelish(lang_list[0] + ':Base')