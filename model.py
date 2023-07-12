import sys
import json
import numpy as np

def build_transition_matrix(dataset):
    # Split the dataset into individual words
    words = []
    for sentence in dataset:
        words += sentence.split()

    # Count the frequency of each word in the dataset
    unique_words, counts = np.unique(words, return_counts=True)

    # Build a mapping of words to indices in the transition matrix
    word_to_idx = {word: idx for idx, word in enumerate(unique_words)}

    # Initialize the transition matrix
    num_words = len(unique_words)
    transition_matrix = np.zeros((num_words, num_words, num_words))

    # Iterate over each sentence in the dataset and update the transition matrix
    for sentence in dataset:
        sentence_words = sentence.split()

        # Skip sentences with fewer than three words
        if len(sentence_words) < 3:
            continue

        # Update the transition matrix
        for i in range(2, len(sentence_words)):
            word_1 = sentence_words[i-2]
            word_2 = sentence_words[i-1]
            word_3 = sentence_words[i]
            idx_1 = word_to_idx[word_1]
            idx_2 = word_to_idx[word_2]
            idx_3 = word_to_idx[word_3]
            transition_matrix[idx_1, idx_2, idx_3] += 1

    # Normalize the transition matrix
    row_sums = np.sum(transition_matrix, axis=(1,2), keepdims=True)
    transition_matrix = transition_matrix / row_sums

    return unique_words, transition_matrix

def print_transition_matrix(unique_words, transition_matrix):

    num_words = len(unique_words)

    words_max_len = 5

    for i in range(num_words):
        for j in range(num_words):
            for k in range(num_words):
                prob = transition_matrix[i, j, k]
                if prob > 0:
                    word_1 = unique_words[i].ljust(words_max_len)
                    word_2 = unique_words[j].ljust(words_max_len)
                    word_3 = unique_words[k].ljust(words_max_len)
                    print(f'P({word_3} | < {word_1}, {word_2} >) = {prob:.4f}')

# Example usage

dataset = [ 
            "The cat is on the mat",
            "The dog is under the table"
            ]

unique_words, transition_matrix = build_transition_matrix(dataset)
print_transition_matrix(unique_words, transition_matrix)
