__author__ = 'sybrandb'

import csv

def csv_dict_writer(p_path, p_fieldnames, p_data):
    """
    Writes a CSV file using DictWriter
    """
    with open(p_path, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=';', quoting= csv.QUOTE_NONNUMERIC, fieldnames=p_fieldnames)
        writer.writeheader()
        for row in p_data:
            writer.writerow(row)
