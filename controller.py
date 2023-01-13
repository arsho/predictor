import os
import json
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
        else:
            return None
    keys = search_results.keys()
    values = search_results.values()
    panels = []
    key_length = len(keys)
    for row in itertools.product(*values):
        panel = dict(zip(keys, row))
        unique_value_length = len(set(panel.values()))
        if unique_value_length == key_length and panel not in panels:
            panels.append(panel)
    return panels


def get_filtered_panels(panels, criterions):
    for criteria in criterions:
        panels = [panel for panel in panels if criteria in panel.items()]
    return panels


def get_initial_panels():
    folder = "data"
    data_file = "inventory_small.xlsx"
    data = read_data(os.path.join(folder, data_file))
    antibody_list_file = "antibody.xlsx"
    search_items = read_search_list(os.path.join(folder, antibody_list_file))
    print(f"Antibody list: {', '.join(search_items)}")
    print('-' * 24)
    # search_items = ["CD103", "CD11c", "CD138"]
    # # search_items = ["CD103", "CD138"]
    # # ["CD4", "CD8", "CD19", "CD38"]
    panels = get_search_results(data, search_items)
    return panels


if __name__ == "__main__":
    folder = "data"
    data_file = "inventory_small.xlsx"
    data = read_data(os.path.join(folder, data_file))
    antibody_list_file = "antibody.xlsx"
    search_items = read_search_list(os.path.join(folder, antibody_list_file))
    print(f"Antibody list: {', '.join(search_items)}")
    print('-' * 24)
    # search_items = ["CD103", "CD11c", "CD138"]
    # # search_items = ["CD103", "CD138"]
    # # ["CD4", "CD8", "CD19", "CD38"]
    panels = get_search_results(data, search_items)
    while True:
        user_msg = "Enter number of conditions (0 to exit): "
        number_of_criterias = int(input(user_msg))
        if number_of_criterias == 0:
            print("Program terminated\n")
            break
        criterions = []
        print("Enter condition in \"Antibody:Conjugate\" pattern "
              "(e.g. CD103:APC)")
        for i in range(number_of_criterias):
            condition = input(f"Enter condition #{i + 1}: ")
            antibody, conjugate = condition.split(":")
            criterions.append((antibody.strip(), conjugate.strip()))
        panels = get_filtered_panels(panels, criterions)
        print("")
