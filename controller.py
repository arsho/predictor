import os
import itertools
import pandas as pd


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
    for row in itertools.product(*values):
        panel = dict(zip(keys, row))
        unique_value_length = len(set(panel.values()))
        if unique_value_length == key_length and panel not in panels:
            panels.append(panel)
    not_found_antibody = list(set(search_items).difference(set(keys)))
    return panels, not_found_antibody


def get_filtered_panels(panels, patterns):
    patterns = patterns.split(",")
    pairs = []
    not_found_patterns = []
    for pattern in patterns:
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
    # data_file = "inventory_small.xlsx"
    data_file = "inventory.xlsx"
    data = read_data(os.path.join(folder, data_file))
    return data


def get_initial_panels(search_items):
    data = get_anitibody_data()
    # CD103,CD11c,CD138
    panels = get_search_results(data, search_items)
    return panels
