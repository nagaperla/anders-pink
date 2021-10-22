how to see installed package version?
pip show <PACKAGE_NAME>


How to uninstall all installed packages?
1. To list all packages: pip freeze > requirements.txt
2. To remove all packages at once: pip uninstall -r requirements.txt -y

virtualenv docs: https://sourabhbajaj.com/mac-setup/Python/virtualenv.html
1. source venv/bin/activate
2. deactivate

<!-- Sample pipeline: imdb -->
1. Initialize base_config.cfg file from spacy: https://spacy.io/usage/training#quickstart
2. Update *base_config.cfg* file with respective train.spacy/valid.spacy data files
3. Copy all values from *base_config.cfg* to *config.cfg*: python -m spacy fill-config ./config/base_config.cfg ./config/config.cfg
4. Then train the spacy model: python -m spacy train ./config/config.cfg --output ./output

Sample project:
https://www.youtube.com/watch?v=7PD48PFL9VQ
