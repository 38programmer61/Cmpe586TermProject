import pandas as pd

def main():
    labels = pd.read_csv('./labels.csv')
    # print(labels)
    # print(len(labels[labels['ChatgptScore'] == '1a']))
    labels = labels.replace('1a', '1')
    # print(len(labels[labels['ChatgptScore']=='1a']))

    chatgpt_final_score_with_partials = labels['ChatgptScore'].astype(int).sum() / 2.0
    untrained_llama2_final_score_with_partials = labels['UntrainedLlama2Score'].astype(int).sum() / 2.0
    llama2_trained_with_manual_labels_final_score_with_partials = labels['Llama2ManualScore'].astype(int).sum() / 2.0
    llama2_trained_with_chatgpt_labels_final_score_with_partials = labels['Llama2ChatgptScore'].astype(int).sum() / 2.0

    print('Scores with partials')
    print()
    print('ChatGPT:\t\t\t\t\t\t\t\t\t', chatgpt_final_score_with_partials)
    print('Untrained Llama 2:\t\t\t\t\t\t\t', untrained_llama2_final_score_with_partials)
    print('Llama 2 (fine-tuned with manual labels):\t', llama2_trained_with_manual_labels_final_score_with_partials)
    print('Llama 2 (fine-tuned with chatgpt labels):\t', llama2_trained_with_chatgpt_labels_final_score_with_partials)
    print()
    print('Scores without partials')
    print()

    chatgpt_final_score_without_partials = labels['ChatgptScore'].replace("1", "0").astype(int).sum() / 2.0
    untrained_llama2_final_score_without_partials = labels['UntrainedLlama2Score'].replace("1", "0").astype(int).sum() / 2.0
    llama2_trained_with_manual_labels_final_score_without_partials = labels['Llama2ManualScore'].replace("1", "0").astype(int).sum() / 2.0
    llama2_trained_with_chatgpt_labels_final_score_without_partials = labels['Llama2ChatgptScore'].replace("1", "0").astype(int).sum() / 2.0
    print('ChatGPT:\t\t\t\t\t\t\t\t\t', chatgpt_final_score_without_partials)
    print('Untrained Llama 2:\t\t\t\t\t\t\t', untrained_llama2_final_score_without_partials)
    print('Llama 2 (fine-tuned with manual labels):\t', llama2_trained_with_manual_labels_final_score_without_partials)
    print('Llama 2 (fine-tuned with chatgpt labels):\t', llama2_trained_with_chatgpt_labels_final_score_without_partials)
    print()

if __name__ == '__main__':
    main()
