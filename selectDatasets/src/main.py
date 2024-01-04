# The following links were helpful
# - https://www.geeksforgeeks.org/read-json-file-using-python/
# - https://www.geeksforgeeks.org/randomly-select-n-elements-from-list-in-python/
# - https://stackoverflow.com/questions/123198/how-to-copy-files

import json
import os
import numpy as np
import shutil

def main():
    make_reproducible()
    prepare_final_directory()
    select_examples(subject='algebra', max_level_of_difficulty=4, n_problems_to_select=1000, train_test='train')
    select_examples(subject='algebra', max_level_of_difficulty=4, n_problems_to_select=100, train_test='test')
    check_for_duplicates()

def make_reproducible(SEED=64357):
    np.random.seed(SEED)

def prepare_final_directory():
    print('Final directory is being prepared.')
    if not os.path.isdir('./selectedProblems'):
        os.mkdir('./selectedProblems')
    if not os.path.isdir('./selectedProblems/train'):
        os.mkdir('./selectedProblems/train')
    if not os.path.isdir('./selectedProblems/test'):
        os.mkdir('./selectedProblems/test')
    print('Final directory was prepared.')
    print()

def select_examples(subject, max_level_of_difficulty, n_problems_to_select, train_test):
    calculate_dir_counts_for_levels(subject, train_test)
    candidates = determine_candidates_based_on_difficulty(subject, max_level_of_difficulty, train_test=train_test)
    select_randomly_among_candidates(candidates, n_problems_to_select, train_test=train_test)

def calculate_dir_counts_for_levels(subject, train_test):
    if train_test=='train':
        calculate_train_counts_for_levels(subject)
    else:
        calculate_test_counts_for_levels(subject)

def calculate_train_counts_for_levels(subject):
    print('Train folder ' + subject + ' counts for levels.')
    calculate_counts_for_levels('./MATH/train/', subject)

def calculate_test_counts_for_levels(subject):
    print('Test folder ' + subject + ' counts for levels.')
    calculate_counts_for_levels('./MATH/test/', subject)

def calculate_counts_for_levels(path, subject):
    files = os.listdir(path + subject) # './MATH/train/'
    count_levels = {i: 0 for i in range(1, 6)}
    for i in range(len(files)):
        f = open(path + subject + '/' + files[i])
        data = json.load(f)
        count_levels[int(data['level'][6:])] += 1
    print(count_levels)

def determine_candidates_based_on_difficulty(subject, max_level_of_difficulty, train_test='train'):
    candidates = []
    files = os.listdir('./MATH/' + train_test + '/' + subject)
    for i in range(len(files)):
        path = './MATH/' + train_test + '/' + subject + '/' + files[i]
        f = open(path)
        data = json.load(f)
        if int(data['level'][6:]) <= max_level_of_difficulty:
            candidates.append(path)
    return candidates

def select_randomly_among_candidates(candidates, n_problems_to_select, train_test='train'):
    selected_problems = sorted(np.random.choice(candidates, size=n_problems_to_select, replace=False).tolist())
    for i in range(len(selected_problems)):
        path = selected_problems[i]
        dirs = path.split('/')
        shutil.copyfile(selected_problems[i], './selectedProblems/' + train_test + '/' + dirs[-1])
    if train_test=='train':
        print('Selected train folder counts for levels.')
    else:
        print('Selected test folder counts for levels.')
    calculate_counts_for_levels('./selectedProblems/' + train_test + '/', '')

def check_for_duplicates():
    all_problem_dirs = get_all_problem_dirs()
    all_problem_statements = read_all_problem_statements(all_problem_dirs)
    compare_pairs(all_problem_statements)
    check_solution_lengths(all_problem_dirs)

def get_all_problem_dirs():
    all_problem_dirs = []
    train_problems = os.listdir('./selectedProblems/train')
    for i in range(len(train_problems)):
        all_problem_dirs.append('./selectedProblems/train/' + train_problems[i])
    test_problems = os.listdir('./selectedProblems/test')
    for i in range(len(test_problems)):
        all_problem_dirs.append('./selectedProblems/test/' + test_problems[i])
    return all_problem_dirs

def read_all_problem_statements(all_problem_dirs):
    all_problem_statements = []
    for i in range(len(all_problem_dirs)):
        f = open(all_problem_dirs[i])
        data = json.load(f)
        all_problem_statements.append(data['problem'])
    return all_problem_statements

def compare_pairs(all_problem_statements):
    has_duplicate = False
    for i in range(len(all_problem_statements)):
        for j in range(i+1, len(all_problem_statements)):
            if all_problem_statements[i] == all_problem_statements[j]:
                has_duplicate=True
    if has_duplicate:
        print('The chosen datasets CONTAINS some duplicates')
    else:
        print('The chosen datasets do NOT contain any duplicates')

def check_solution_lengths(all_problem_dirs):
    all_outputs = []
    for i in range(len(all_problem_dirs)):
        f = open(all_problem_dirs[i])
        data = json.load(f)
        all_outputs.append(data['solution'])
    lens = [len(s) for s in all_outputs]
    print('Shortest ones:', sorted(lens)[:5], 'Longest ones:', sorted(lens)[-5:])

if __name__ == '__main__':
    main()
