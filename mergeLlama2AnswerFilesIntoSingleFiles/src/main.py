import json
import os

def main():
    DIRS = ['./llama2Answers/llama2Untrained', './llama2Answers/llama2TrainedWithManualSolutions',
            './llama2Answers/llama2TrainedWithChatgptSolutions']
    for dir in DIRS:
        # files = sorted(os.listdir(dir))
        files = sorted(os.listdir(dir), key=fix_multi_digit_num_sort)
        print(files)
        merged_list = []
        for file in files:
            f = open(os.path.join(dir, file), 'r')
            data = json.load(f)
            merged_list += data
        write_to_json_file(merged_list, os.path.join(dir, files[0][:-6] + 'merged'))

def fix_multi_digit_num_sort(el):
    return len(el), el

def write_to_json_file(dataset, name):
    json_object = json.dumps(dataset, indent=4)
    with open(name + ".json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    main()
