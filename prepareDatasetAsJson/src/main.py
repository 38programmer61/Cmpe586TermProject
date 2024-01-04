# The following tutorials were useful
# - https://www.geeksforgeeks.org/read-json-file-using-python/
# - https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# - https://www.geeksforgeeks.org/convert-json-to-csv-in-python/

import json
import os
import pandas as pd

def main():
    build_dataset_as_json(DIR='./problemsWithChatGPTResponses/train', n_problems=100, is_manual_solution=True)
    build_dataset_as_json(DIR='./problemsWithChatGPTResponses/train', n_problems=100, is_manual_solution=False)
    build_dataset_as_json(DIR='./problemsWithChatGPTResponses/train', n_problems=1000, is_manual_solution=True)
    build_dataset_as_json(DIR='./problemsWithChatGPTResponses/train', n_problems=1000, is_manual_solution=False)
    build_test_set_as_json(DIR='./problemsWithChatGPTResponses/test', n_problems=100)

def build_dataset_as_json(DIR, n_problems, is_manual_solution):
    dataset = []
    file_names = os.listdir(DIR)
    file_names = [file_name for file_name in file_names if not 'chat' in file_name]
    for i in range(n_problems):
        f = open(os.path.join(DIR, file_names[i]))
        problem_data = json.load(f)
        problem_json = get_json_for_problem(problem_data, is_manual_solution)
        dataset.append(problem_json)
    write_to_json_file(dataset, name=get_name(n_problems, is_manual_solution))
    write_to_csv_file(dataset, name=get_name(n_problems, is_manual_solution))

def build_test_set_as_json(DIR, n_problems):
    test_set = []
    file_names = sorted(os.listdir(DIR))
    file_names = [file_name for file_name in file_names if not 'chat' in file_name]
    print(file_names)
    for i in range(n_problems):
        f = open(os.path.join(DIR, file_names[i]))
        problem_data = json.load(f)
        problem_json = {
            "instruction": problem_data['problem'],
            "input": ""
        }
        test_set.append(problem_json)
    write_to_json_file(test_set, name='test_set')
    # write_to_csv_file(test_set, name='test_set')

def get_json_for_problem(problem_data, is_manual_solution):
    if is_manual_solution:
        problem_json = {
            "instruction": problem_data['problem'],
            "input": "",
            "output": problem_data['solution']
        }
    else:
        problem_json = {
            "instruction": problem_data['problem'],
            "input": "",
            "output": problem_data['chatgpt_solution']
        }
    return problem_json

def get_name(n_problems, is_manual_solution):
    if is_manual_solution:
        name = 'manual_' + str(n_problems)
    else:
        name = 'chatgpt_' + str(n_problems)
    return name

def write_to_json_file(dataset, name):
    json_object = json.dumps(dataset, indent=4)
    with open(name + ".json", "w") as outfile:
        outfile.write(json_object)

def write_to_csv_file(dataset, name):
    df = pd.DataFrame(dataset)
    df['text'] = ('Below is an instruction that describes a task. Write a response that appropriately completes the request. ' +
                  '### Instruction: ' + df['instruction'] + ' ### Response: ' + df['output'])
    df.to_csv(name + '.csv', index=False)


if __name__ == '__main__':
    main()
