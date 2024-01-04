# The following tutorials were useful
# - https://www.geeksforgeeks.org/read-json-file-using-python/
# - https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# - https://www.freecodecamp.org/news/python-json-how-to-convert-a-string-to-json/

import os
import json
from openai import OpenAI

def main():
    # print(openai.__version__)
    make_chatgpt_response_directory()
    get_and_save_chatgpt_responses_for_directory(
        input_dir='./selectedProblems/train',
        output_dir='./problemsWithChatGPTResponses/train'
    )
    get_and_save_chatgpt_responses_for_directory(
        input_dir='./selectedProblems/test',
        output_dir='./problemsWithChatGPTResponses/test'
    )

def make_chatgpt_response_directory():
    print('New directory for storing problems with ChatGPT responses is being prepared.')
    if not os.path.isdir('./problemsWithChatGPTResponses'):
        os.mkdir('./problemsWithChatGPTResponses')
    if not os.path.isdir('./problemsWithChatGPTResponses/train'):
        os.mkdir('./problemsWithChatGPTResponses/train')
    if not os.path.isdir('./problemsWithChatGPTResponses/test'):
        os.mkdir('./problemsWithChatGPTResponses/test')
    print('New directory for storing problems with ChatGPT responses was prepared.')
    print()

def get_and_save_chatgpt_responses_for_directory(input_dir, output_dir):
    print('Started working with directory:', input_dir)
    problem_file_names = sorted(os.listdir(input_dir))
    for i in range(len(problem_file_names)):
        print('Started working with file:', problem_file_names[i])
        get_and_save_chatgpt_responses_for_a_problem(input_dir, problem_file_names[i], output_dir)
        print('Completed', i+1, '/', len(problem_file_names))
    print('Ended working with directory:', input_dir)
    print()

def get_and_save_chatgpt_responses_for_a_problem(input_dir, problem_file_name, output_dir):
    problem_data = read_problem_data(input_dir, problem_file_name)
    chatgpt_response_str, chatgpt_solution_str = get_chatgpt_response_using_api(problem_data['problem'])
    save_chatgpt_response(output_dir, problem_file_name, chatgpt_response_str)
    save_problem_with_chatgpt_response(output_dir, problem_file_name, problem_data, chatgpt_solution_str)

def read_problem_data(input_dir, problem_file_name):
    problem_file_path = os.path.join(input_dir, problem_file_name)
    f = open(problem_file_path)
    problem_data = json.load(f)
    return problem_data

def get_chatgpt_response_using_api(problem_statement):
    # ToDo use real api

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # client.api_key = 'A'

    RANDOM_SEED = 63753

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": problem_statement}
        ],
        seed=RANDOM_SEED
    )

    chatgpt_response_str = completion.model_dump_json()
    chatgpt_solution_str = completion.choices[0].message.content
    print(chatgpt_response_str)

    return chatgpt_response_str, chatgpt_solution_str

    # return '{"id":"chatcmpl-8JgEXfa1DKFxpHFI3Sv52DRfN1s8d","choices":[{"finish_reason":"stop","index":0,"message":{"content":"Since $3 \\\\ge -2,$ we use the second case to see that $f(3) = 5 - 2(3) = \\\\boxed{-1}.$","role":"assistant","function_call":null,"tool_calls":null}}],"created":1699701269,"model":"gpt-3.5-turbo-0613","object":"chat.completion","system_fingerprint":null,"usage":{"completion_tokens":37,"prompt_tokens":65,"total_tokens":102}}', "My solution"

def save_chatgpt_response(output_dir, problem_file_name, chatgpt_response_str):
    json_object = json.loads(chatgpt_response_str)
    json_object = json.dumps(json_object, indent=4)
    with open(os.path.join(output_dir, 'chat_' + problem_file_name), "w") as outfile:
        outfile.write(json_object)

def save_problem_with_chatgpt_response(output_dir, problem_file_name, problem_data, chatgpt_solution_str):
    problem_data['chatgpt_solution'] = chatgpt_solution_str
    json_object = json.dumps(problem_data, indent=4)
    with open(os.path.join(output_dir, problem_file_name), "w") as outfile:
        outfile.write(json_object)

if __name__ == '__main__':
    main()

