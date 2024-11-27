import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd

scenario_numbers = [3,5,40, 50,100,500]
model_name = ['gemma-2b-it', 'vicuna-13b-v1.5']
flag_file = 'csv_read_flag.txt'
scenario_dimension_group_types = {
    'species': ["human", "pet"],
    'social value': ["lower", "higher"],
    'gender': ["female", "male"],
    'age': ["younger", "older"],
    'fitness': ["lower", "higher"],
    'utilitarian': ["less", "more"],
    'race' : ["black/indian", "white"],
    'sexualism' : ["black/indian", "white"]
}

scenario_mapping = {}


def check_merge_csv_flag():
    if os.path.exists(flag_file):
        with open(flag_file, 'r') as f:
            return f.read().strip() == 'True'
    return False

def set_merge_csv_flag(value):
    with open(flag_file, 'w') as f:
        f.write(str(value))

def merge_csv_files():
    current_df = pd.DataFrame()
    for model in model_name:
        for number in scenario_numbers:
            try:
                dataframe = pd.read_csv('shared_responses_{}_{}.csv'.format(model, number))
                current_df = dataframe if not current_df.empty else pd.concat([current_df, dataframe], ignore_index=True)
            except FileNotFoundError:
                # Handle the case where a file is not found
                print("File not found for model {} and scenario {}".format(model, number))
        if current_df is not None:
            current_df.to_csv('merged_file_{}.csv'.format(model), index=False)
    set_merge_csv_flag(True)

def merge_model_files(file1, file2):
    df_1 = pd.read_csv(file1)
    df_2 = pd.read_csv(file2)

    merged_df = pd.concat([df_1, df_2])
    num_rows = merged_df.shape[0]
    merged_df.to_csv('llm_model_scenarios.csv', index= False)



#merge_csv_files()
#merge_model_files("merged_file_vicuna-13b-v1.5.csv", "llm_model_scenarios.csv")


def count_rows_csv():
    df = pd.read_csv("llm_model_scenarios.csv")
    row_count = df.shape[0]
    return row_count
row_count = count_rows_csv()
print("Number of rows in the CSV file:", row_count)
#

def plot_bar_graph(case1_values, case2_values, scenarios):
    bar_width = 0.35

    r1 = range(len(scenarios))
    r2 = [x + bar_width for x in r1]

    plt.figure(figsize=(10, 6))
    colors = ['darkblue', 'red', 'plum']
    plt.bar(r1, case1_values, color='darkblue', width=bar_width, edgecolor='grey', label='Case 1')
    plt.bar(r2, case2_values, color='plum', width=bar_width, edgecolor='grey', label='Case 2')
    plt.xlabel('Scenario', fontweight='bold')
    plt.ylabel('Counts', fontweight='bold')
    plt.xticks([r + bar_width / 2 for r in range(len(scenarios))], scenarios)
    plt.legend()
    plt.title('Counts of Case 1 and Case 2 for Each Scenario')
    plt.show()


def analyse_llm_data():
    odd_rows_df = pd.read_csv("llm_model_scenarios.csv", skiprows=lambda x: x % 2 != 0)
    for dimension, groups in scenario_dimension_group_types.items():
        scenario_mapping[dimension] = {1: groups[0], 2: groups[1]}

    case1_counts = {key: 0 for key in scenario_mapping.keys()} 
    case2_counts = {key: 0 for key in scenario_mapping.keys()} 
    for index, row in odd_rows_df.iterrows():

        scenario_type = row['ScenarioType']
        scenario_type = scenario_type.lower()
        # Get the response for case 1 or case 2
        preference = 1 if 'Case 1' in row['Response'] else 2
        if preference == 1:
            case1_counts[scenario_type] += 1
        else:
            case2_counts[scenario_type] += 1

    # Get the scenarios and counts
    scenarios = list(case1_counts.keys())
    case1_values = list(case1_counts.values())
    case2_values = list(case2_counts.values())
    plot_bar_graph(case1_values, case2_values, scenarios)

#analyse_llm_data()


