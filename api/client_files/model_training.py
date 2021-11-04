import random
import json
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from rq import get_current_job
from functools import partial

from utilities.constants import LANGUAGES, FOLDERS
from utilities.processing_utils import loadData, loadTrainingData
from utilities.utils import toLower, split_list
from utilities.processing_utils import process_and_annotate

from training.model_evaluation import evaluate_model
from utilities.processing_utils import save_model
from utilities.file_utils import load_csv
from classify.models import get_model

import utilities.logger as logger


def init_model(lang):
    if lang not in LANGUAGES:
        raise Exception(f"{lang} is not a supported language")

    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.blank(lang)

    if "textcat" not in nlp.pipe_names:
        textcat = nlp.create_pipe(
            "textcat", config={"exclusive_classes": False, "architecture": "ensemble"}
        )
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    # else:
    #     textcat = nlp.get_pipe("textcat")
    print("Created blank 'en' model")
    return nlp


def check_is_cancelled():
    job = get_current_job()  #  defined if if running from a rq
    is_cancelled = None if job is None else job.connection.get(
        job.key + b':should_stop')
    if is_cancelled is None:
        return False
    else:
        return True if int(is_cancelled.decode()) == 1 else False


def score_reporter(losses, iteration, scores):
    job = get_current_job()  #  defined if if running from a rq
    logger.info(f'current job: {job}, iteration: {iteration}')
    if job is not None:
        # pass back progress data
        job.meta["iteration"] = iteration
        job.meta["textcat_loss"] = losses['textcat']
        job.meta["textcat_p"] = scores["textcat_p"]
        job.meta["textcat_r"] = scores["textcat_r"]
        job.meta["textcat_f"] = scores["textcat_f"]
        job.save_meta()

    logger.info(
        "{0}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}".format(  # print a simple table
            iteration,
            losses["textcat"],
            scores["textcat_p"],
            scores["textcat_r"],
            scores["textcat_f"],
        )
    )


def __train_and_save(nlp, output_name, path, training_data, n_iter=5, split_ratio=0.8):

    annotated_data, cats = process_and_annotate(training_data, shuffle=True)

    for cat in cats:
        nlp.get_pipe("textcat").add_label(cat)

    data_training, data_evaluation = split_list(
        annotated_data, ratio=split_ratio)

    # get names of other pipes to disable them during training
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [
        pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    is_cancelled = False
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()

        batch_sizes = compounding(4.0, 32.0, 1.001)
        print("Training the model...")
        print("{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}".format(
            "ITER", "LOSS", "P", "R", "F"))
        for i in range(n_iter):
            if check_is_cancelled():
                is_cancelled = True
                break
            losses = {}
            # batch up the examples using spaCy's minibatch
            random.shuffle(data_training)
            batches = minibatch(data_training, size=batch_sizes)
            for batch in batches:
                texts = list([item["text"] for item in batch])
                annotations = list([item["annotations"] for item in batch])
                # training
                try:
                    nlp.update(texts, annotations, sgd=optimizer,
                               drop=0.2, losses=losses)
                except Exception:
                    print("error!")

            iteration_str = f"{i+1}/{n_iter}"

            evaluate_model(nlp, optimizer=optimizer,
                           data=data_evaluation, report_scores=partial(score_reporter, losses, iteration_str))

    if not is_cancelled:
        save_model(nlp, optimizer, output_name, path)


def get_cat_labels_for_file(file_name):
    td = load_training_datas([file_name])
    cat_labels_all = td[0][1:]
    return cat_labels_all


def get_training_data_from_files(file_names, split_ratio):
    # training_data = load_training_datas(file_names)
    data_training, data_evaluation = split_list(
        process_and_annotate(
            load_training_datas(file_names), shuffle=True), ratio=split_ratio)
    return (data_training, data_evaluation)


def create_cats(all_cats_dict, cats_list):
    merged = {**all_cats_dict, **
              {k: v for element in cats_list for k, v in element.items()}}
    return merged


def get_texts_and_annotations(data, cat_annotations_all):
    texts = list([item[0] for item in data])
    annotations = list(
        [{"cats": create_cats(cat_annotations_all, json.loads(item[1]))} for item in data])
    return (texts, annotations)


def __train_and_save_v2(nlp, output_name, training_data, n_iter=5, split_ratio=0.8, path=""):

    cat_labels_row = training_data[0]
    if cat_labels_row[0] != 'category_labels':
        raise Exception(
            'Bad training datas format - first row should contain category labels')

    cat_labels_all = [str(cat_label)
                      for cat_label in json.loads(cat_labels_row[1])]

    for cat in cat_labels_all:
        nlp.get_pipe("textcat").add_label(cat)

    cat_annotations_all = {cat: 0.0 for cat in cat_labels_all}

    data_training, data_evaluation = split_list(
        training_data[1:], ratio=split_ratio)

    data_evaluation = [{"text": item[0], "annotations": {"cats": create_cats(
        cat_annotations_all, json.loads(item[1]))}} for item in data_evaluation]

    # get names of other pipes to disable them during training
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [
        pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    is_cancelled = False
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()

        batch_sizes = compounding(4.0, 32.0, 1.001)
        print("Training the model...")
        print("{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}".format(
            "ITER", "LOSS", "P", "R", "F"))
        for i in range(n_iter):
            if check_is_cancelled():
                is_cancelled = True
                break
            losses = {}
            # batch up the examples using spaCy's minibatch
            random.shuffle(data_training)
            batches = minibatch(data_training, size=batch_sizes)
            for batch in batches:
                texts, annotations = get_texts_and_annotations(
                    batch, cat_annotations_all)
                # texts = list([item[0] for item in batch])
                # annotations = list(
                #     [{"cats": create_cats(cat_annotations_all, json.loads(item[1]))} for item in batch])

                try:
                    nlp.update(texts, annotations, sgd=optimizer,
                               drop=0.2, losses=losses)
                except Exception:
                    print("error!")

            iteration_str = f"{i+1}/{n_iter}"

            evaluate_model(nlp, optimizer=optimizer,
                           data=data_evaluation, report_scores=partial(score_reporter, losses, iteration_str))

    if not is_cancelled:
        save_model(nlp, optimizer, output_name, path)


def load_training_datas(data_file_names):
    logger.info('loading training datas...')
    try:
        training_datas = [load_csv(FOLDERS.TRAINING_DATA, file_name)
                          for file_name in data_file_names]
        all_cats = [td[0] for td in training_datas]
        cats_match = all(all_cats[0] == cat for cat in all_cats)
        if not cats_match:
            raise Exception('Cats do not match in training data')
        return [all_cats[0]] + [data_row for training_data in training_datas for data_row in training_data[1:]]
    except Exception as e:
        logger.exception(e)
        # training_data = [
        #     data_row for training_data in training_datas for data_row in training_data[1:]]
        # training_data = [all_cats[0]] + training_data


def train_model(data_file_names, save_as_name, path, model_to_update=None, lang="en", n_iter=5, split_ratio=0.8):
    try:
        if model_to_update is not None:
            # model_to_update = {model_name, categoriser_type}
            nlp = get_model(**model_to_update)
        else:
            nlp = init_model(lang)

        training_datas = load_training_datas(data_file_names)
        is_v2 = True if training_datas[0][0] == 'category_labels' else False
        logger.info(
            f"Starting training job, {'v2' if is_v2 else 'v1'} training data detected")
        if is_v2:
            __train_and_save_v2(nlp, output_name=save_as_name,
                                training_data=training_datas, n_iter=n_iter, split_ratio=split_ratio, path=path)
        else:
            __train_and_save(nlp, output_name=save_as_name,
                             training_data=training_datas, n_iter=n_iter, split_ratio=split_ratio, path=path)
    except Exception as e:
        logger.exception(e)
