# The following resources were useful
# - https://www.geeksforgeeks.org/how-to-create-an-empty-dataframe-and-append-rows-columns-to-it-in-pandas/

import os
import json
import time

import pandas as pd

def main():
    prepared_output_dir(OUT_DIR='./allTestProblemsWithMergedAnswers')
    untrained_llama2_answers, llama2_trained_with_chatgpt_labels_answers, llama2_trained_with_manual_labels_answers = read_llama2_answers()
    merge_all_responses_to_test_set_problems(
        DIR='./problemsWithChatGPTResponses/test',
        OUT_DIR='./allTestProblemsWithMergedAnswers',
        untrained_llama2_answers=untrained_llama2_answers,
        llama2_trained_with_chatgpt_labels_answers=llama2_trained_with_chatgpt_labels_answers,
        llama2_trained_with_manual_labels_answers=llama2_trained_with_manual_labels_answers
    )
    prepare_csv_file(DIR='./allTestProblemsWithMergedAnswers')

def prepared_output_dir(OUT_DIR):
    if not os.path.isdir(OUT_DIR):
        os.mkdir(OUT_DIR)

def read_llama2_answers():
    f1 = open('./llama2Answers/llama2Untrained/test_examples_with_untrained_llama2_solutions_merged.json')
    untrained_llama2_answers = json.load(f1)

    f2 = open(
        './llama2Answers/llama2TrainedWithChatgptSolutions/test_examples_with_llama2_trained_on_chatgpt_solutions_merged.json')
    llama2_trained_with_chatgpt_labels_answers = json.load(f2)

    f3 = open(
        './llama2Answers/llama2TrainedWithManualSolutions/test_examples_with_llama2_trained_on_manual_solutions_merged.json')
    llama2_trained_with_manual_labels_answers = json.load(f3)

    return untrained_llama2_answers, llama2_trained_with_chatgpt_labels_answers, llama2_trained_with_manual_labels_answers

def merge_all_responses_to_test_set_problems(DIR, OUT_DIR, untrained_llama2_answers, llama2_trained_with_chatgpt_labels_answers, llama2_trained_with_manual_labels_answers):
    file_names = sorted(os.listdir(DIR))
    file_names = [file_name for file_name in file_names if not 'chat' in file_name]

    for i in range(len(file_names)):
        f = open(os.path.join(DIR, file_names[i]))
        problem_data = json.load(f)
        final_json = {
            "problem": problem_data['problem'],
            "level": problem_data['level'],
            "type": problem_data['type'],
            "untrained_llama2_solution": untrained_llama2_answers[i]["untrained_llama2_solution"],
            "llama2_trained_with_chatgpt_labels_solution": llama2_trained_with_chatgpt_labels_answers[i]["llama2_fine_tuned_on_chatgpt_solution"],
            "llama2_trained_with_manual_labels_solution": llama2_trained_with_manual_labels_answers[i]["llama2_fine_tuned_on_manual_solution"],
            "chatgpt_solution": problem_data['chatgpt_solution'],
            "manual_solution": problem_data['solution'],
            "latex": "\\textbf{Problem}: " + problem_data['problem'] + "\\newline\n\n\n\\textbf{Manual Solution}: " + problem_data['solution'] + "\\newline\n\n\n\\textbf{Chatgpt Solution}: " + problem_data['chatgpt_solution'] + "\\newline\n\n\n\\textbf{Untrained llama 2 Solution}: " + untrained_llama2_answers[i]["untrained_llama2_solution"] + "\\newline\n\n\n\\textbf{Llama 2 (fine-tuned with manual labels) Solution}: " + llama2_trained_with_manual_labels_answers[i]["llama2_fine_tuned_on_manual_solution"] + "\\newline\n\n\n\\textbf{Llama 2 (fine-tuned with chatgpt labels) Solution}: " + llama2_trained_with_chatgpt_labels_answers[i]["llama2_fine_tuned_on_chatgpt_solution"]
        }

        # print(file_names[i])
        # print(final_json["latex"])
        # next_one_command = input()

        json_object = json.dumps(final_json, indent=4)
        with open(os.path.join(OUT_DIR, file_names[i]), "w") as outfile:
            outfile.write(json_object)



def prepare_csv_file(DIR):
    file_names = sorted(os.listdir(DIR), key=file_explorer_order)
    df = pd.DataFrame(columns=['fileName', 'ChatgptScore', 'UntrainedLlama2Score', 'Llama2ManualScore', 'Llama2ChatgptScore'])
    for i in range(len(file_names)):
        df = df.append(
            {
                'fileName': file_names[i],
                'ChatgptScore': -1,
                'UntrainedLlama2Score': -1,
                'Llama2ManualScore': -1,
                'Llama2ChatgptScore': -1
            },
            ignore_index=True
        )
    df.to_csv('./labels.csv', index=False)

def file_explorer_order(el):
    return len(el), el

if __name__ == '__main__':
    main()
