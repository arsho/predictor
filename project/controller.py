import os
from os.path import dirname, realpath
import itertools
import pandas as pd
from os.path import dirname, realpath


def read_data(datafile):
    data = pd.read_excel(datafile)
    mapper = {}
    for index, row in data.iterrows():
        antibody = row["Antibody"]
        conjugate = row["Conjugate"]
        if antibody in mapper:
            mapper[antibody].append(conjugate)
        else:
            mapper[antibody] = [conjugate]
    return mapper


def read_data_large(datafile):
    '''
    Lab#                       1.0
    Antibody                 CD102
    Conjugate                AF647
    Clone             3C4 (MIC2/4)
    Vendor               BioLegend
    Catalog Number          105612
    Users                      3.0
    Chanel                     ASK
    #C                        1ASK
    Backup                       1
    Lot#                   B227625
    RRID                       NaN
    '''
    data = pd.read_excel(datafile, sheet_name="Inventory")
    data.dropna(how='all', inplace=True)
    data.fillna("", inplace=True)
    return data.to_dict(orient='records')


def read_search_list(datafile):
    data = pd.read_excel(datafile, header=None)
    return data[0].tolist()


def get_search_results(data, search_items):
    search_results = {}
    for antibody in search_items:
        if antibody in data:
            search_results[antibody] = data[antibody]
    keys = search_results.keys()
    values = search_results.values()
    panels = []
    key_length = len(keys)
    not_found_antibody = list(set(search_items).difference(set(keys)))
    if key_length == 0:
        return panels, not_found_antibody
    for row in itertools.product(*values):
        panel = dict(zip(keys, row))
        unique_value_length = len(set(panel.values()))
        if unique_value_length == key_length and panel not in panels:
            panels.append(panel)
    return panels, not_found_antibody


def get_filtered_panels(panels, patterns):
    patterns = patterns.split(",")
    pairs = []
    not_found_patterns = []
    for pattern in patterns:
        if ":" in pattern:
            antibody, conjugate = pattern.split(":")
            pairs.append((antibody.strip(), conjugate.strip()))
    for pair in pairs:
        temp_panels = [panel for panel in panels if pair in panel.items()]
        if len(temp_panels) == 0:
            not_found_patterns.append(",".join(pair))
        else:
            panels = temp_panels
    return panels, not_found_patterns


def get_anitibody_data():
    folder = "data"
    data_file = "inventory.xlsx"
    data = read_data(
        os.path.join(dirname(realpath(__file__)), folder, data_file))
    return data


def get_row(data, lab_id):
    for record in data:
        if str(record["Lab#"]) == lab_id:
            return record
    return []


def get_full_data():
    folder = "data"
    data_file = "inventory_large.xlsx"
    data_path = os.path.join(dirname(realpath(__file__)), folder, data_file)
    return read_data_large(data_path)


def get_antibody_conjugate_mapper():
    folder = "data"
    data_file = "inventory_large.xlsx"
    data_path = os.path.join(dirname(realpath(__file__)), folder, data_file)
    data = read_data_large(data_path)
    antibody = []
    conjugate = []
    mapper = {}
    for row in data:
        current_antibody = row["Antibody"].strip()
        current_conjugate = row["Conjugate"].strip()
        if current_antibody != "" and current_conjugate != "":
            antibody.append(current_antibody)
            conjugate.append(current_conjugate)
            if current_antibody in mapper and current_conjugate != "" and current_conjugate != None:
                if current_conjugate not in mapper[current_antibody]:
                    mapper[current_antibody].append(current_conjugate)
            elif current_antibody != "" and current_antibody != None and current_conjugate != "" and current_conjugate != None:
                mapper[current_antibody] = [current_conjugate]
    return list(set(antibody)), list(set(conjugate)), mapper


def get_initial_panels(search_items):
    data = get_anitibody_data()
    panels = get_search_results(data, search_items)
    return panels


def get_initial_records(search_elements):
    data = get_full_data()
    filtered_data = []
    not_found_elements = []
    conjugate = {}
    for search_element in search_elements:
        found = False
        for row in data:
            if row["Antibody"] == search_element[0] and \
                    row["Conjugate"] == search_element[1]:
                if row["Conjugate"] in conjugate:
                    row["repeat"] = True
                else:
                    row["repeat"] = False
                    conjugate[row["Conjugate"]] = True
                found = True
                filtered_data.append(row)
        if not found:
            not_found_elements.append(search_element)
    return filtered_data, not_found_elements


if __name__ == "__main__":
    print("main")
