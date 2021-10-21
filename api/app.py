import spacy
# Ref: https://spacy.io/usage/saving-loading#entry-points-languages
from spacy.lang.en import English

spacy.prefer_gpu()
# To calculate efficiency
# python -m spacy download en_core_web_sm
# nlp = spacy.load("en_core_web_sm")

# To calculate accuracy
# Run the following cmd before executing this
# python -m spacy download en_core_web_trf
# nlp = spacy.load("en_core_web_trf")

nlp = English()
nlp.add_pipe("snek")

doc = nlp("What Cosby’s Release Means For Victims Of Workplace Sexual Harassment The technicalities behind Cosby's release are hardly any consolation to anyone who’s been a victim of sexual misconduct and is thinking about taking legal action in response..")
print(doc)
print([ (w, w.text, w.pos_) for w in doc])
print([ (w.text, w.pos_) for w in doc])

# cls = spacy.util.get_lang_class(lang)
# nlp2 = cls()
# for name in pipeline:
#     nlp2.add_pipe(name)
# nlp2.from_disk(data_path)
