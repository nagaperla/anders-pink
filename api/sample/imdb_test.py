import spacy
from ml_datasets import imdb

# Load the output model
nlp = spacy.load("./output/model-best")

# Imdb data to test
# train_data, valid_data = imdb()
# num_texts = 2500
# imdb_text = train_data[num_texts]
# imdb_doc = nlp(imdb_text[0])
# print("Text:", imdb_text)
# print("Scores:", imdb_doc.cats)

# Random data to test
random_text = "I love sweets"
random_doc = nlp(random_text)
print("Text:", random_text)
print("Scores:", random_doc.cats)
