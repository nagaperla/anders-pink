

def evaluate_model(nlp, optimizer, data, report_scores=None):
    textcat = nlp.get_pipe("textcat")
    with textcat.model.use_params(optimizer.averages):
        # evaluate on the dev data split off in load_data()
        if report_scores is not None:
            scores = calculate_scores(nlp.tokenizer, textcat, data)
            report_scores(scores)


def calculate_scores(tokenizer, textcat, dev_training_data):
    if len(dev_training_data) == 0:
        return {"textcat_p": 0, "textcat_r": 0, "textcat_f": 0}

    texts = [data["text"]
             for data in dev_training_data]
    annotations = [data["annotations"]
                   for data in dev_training_data]

    docs = (tokenizer(text) for text in texts)
    tp = 0.0  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 0.0  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = annotations[i]["cats"]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            # if label == badCat:
            #     continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.0
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.0
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}
