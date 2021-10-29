import os
import spacy
import pandas as pd

from spacy.tokens import Doc
from spacy.lang.en import English
from spacy.training import Example
from thinc.api import SGD

from dotenv import load_dotenv
load_dotenv()

# class SpacyTrainedModel:

# Uncomment this, if you want to use spaCy default modal
def load_spacy_stop_words():
    efficency_modal = spacy.load("en_core_web_sm")
    all_stop_words = efficency_modal.Defaults.stop_words
    return all_stop_words

def remove_stop_words(sentence):
    # List of manual stop words
    stop_words_list = ["not", "you", "i"]

    # List of spacy stop words
    # stop_words_list = load_spacy_stop_words()

    # Filtering stop words
    text_tokens = sentence.split(" ")
    text_tokens_after_filter = [word for word in text_tokens if not word in stop_words_list]
    return (" ").join(text_tokens_after_filter)

def convert_list_to_dictionary(category_ids_list):
    object = {}
    for idx, category_id in enumerate(category_ids_list):
        if category_id not in object:
            category_key = "category" + str(idx)
            object[category_key] = category_id
    return object

def model_input_data():
    training_data = pd.read_csv(os.getenv('PATH_TO_TRAINING_DATA'))
    training_data.reset_index(drop = True, inplace = True)

    formatted_data = []
    category_ids_dict = {}

    # Tuple format
    # for index, category in enumerate(training_data['category_ids']):
    #     category_ids_list = category.split(', ')
    #     category_ids_dict['category_id'] = convert_list_to_dictionary(category_ids_list)
    #     filtered_text = remove_stop_words(training_data['text'][index])
    #     formatted_data.append((filtered_text, category_ids_dict))

    # Dict format
    for index, category in enumerate(training_data['category_ids']):
        category_ids_list = category.split(', ')
        filtered_text = remove_stop_words(training_data['text'][index])
        formatted_data.append({"text": filtered_text, "categories": category_ids_list})

    return formatted_data

# Warn errors
def warn_error(proc_name, proc, docs, e):
    print(f"An error occured when applying component {proc_name}.")

def thinc_custom_optimizer():
    optimizer = SGD(
        learn_rate=0.001,
        L2=1e-6,
        grad_clip=1.0
    )
    return optimizer

def train_model():
    final_training_data = model_input_data()
    print('final_tra', final_training_data)
    batches = spacy.util.minibatch(final_training_data, size=1000)
    print('batches', batches)

    # Load language class
    nlp = English()
    nlp.set_error_handler(warn_error)

    # Create & Add pipe
    textcat_multilabel_pipe = nlp.create_pipe("textcat_multilabel")
    nlp.add_pipe(textcat_multilabel_pipe)
    textcat_multilabel_pipe.initialize(lambda: [], nlp=nlp)

    for batchIdx, batch in enumerate(batches):
        print('batch', batchIdx)
        example = Example.from_dict(Doc(vocab, words), {"text": "I'm a good body", "categories": ['1', '2', '3', '4']})
        nlp.update([example], sgd=thinc_custom_optimizer())

    # Write final output to model directory
    nlp.to_disk(os.getenv('PATH_TO_STORE_OUTPUT_MODEL'))
    pass

train_model()

def __init__(self, *kwargs):
    print('lllkdfj', self)
    pass

# r__spacy_trained_model = SpacyTrainedModel("en")
# print(r__spacy_trained_model.train_model())


# embedding layer -
# nltk - frequency
# gensim - word embeddings - semantic meaning required
