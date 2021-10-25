import spacy
import pandas as pd

def data_modelling():
    training_data = pd.read_csv('./data/train_n50.csv')
    training_data.reset_index(drop = True, inplace = True)

    formatted_data = []
    category_ids_dict = {}

    for index, category in enumerate(training_data['category_ids']):
        category_ids_list = category.split(', ')
        category_ids_dict['category_id'] = convert_list_to_dictionary(category_ids_list)
        formatted_data.append((training_data['text'][index], category_ids_dict))
    return formatted_data

def convert_list_to_dictionary(category_ids_list):
    object = {}
    for idx, category_id in enumerate(category_ids_list):
        if category_id not in object:
            category_key = "category" + str(idx)
            object[category_key] = category_id
    return object

print(data_modelling())

def stop_words():
    pass

def train():
    # Output model directory
    output_directory = "model/"
    # Load language class
    nlp = spacy.lang("en")
    # Create a pipe
    category = nlp.create_pipe("textcat_multilabel")
    category.add_label("OFFENSIVE")
    # Add pipe
    nlp.add_pipe(category)
    nlp.to_disk(output_directory)
    pass

def __init__():
    pass

# embedding layer -
# nltk - frequency
# gensim - word embeddings - semantic meaning required
