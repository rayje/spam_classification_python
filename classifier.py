from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score
from pandas import DataFrame
import numpy as np
import os

NEWLINE = '\n'
SKIP_FILES = {'cmds'}
HAM = 'ham'
SPAM = 'spam'

SOURCES = [
    ('.data/spam', SPAM),
    ('.data/easy_ham', HAM),
    ('.data/hard_ham', HAM),
    ('.data/beck-s', HAM),
    ('.data/farmer-d', HAM),
    ('.data/kaminski-v', HAM),
    ('.data/kitchen-l', HAM),
    ('.data/lokay-m', HAM),
    ('.data/williams-w3', HAM),
    ('.data/BG', SPAM),
    ('.data/GP', SPAM),
    ('.data/SH', SPAM)
]

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    past_header, lines = False, []
                    with open(file_path, encoding="latin-1") as f:
                        for line in f:
                            if past_header:
                                lines.append(line)
                            elif line == NEWLINE:
                                past_header = True
                    content = NEWLINE.join(lines)
                    yield file_path, content

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text':text,'class':classification})
        index.append(file_name)

    return DataFrame(rows, index=index)

if __name__ == '__main__':
    print("Getting data")

    data = DataFrame({'text':[], 'class':[]})
    for path, classification in SOURCES:
        data = data.append(build_data_frame(path, classification))
    data = data.reindex(np.random.permutation(data.index))

    print(len(data))

    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])

    #print("Fitting data")

    #pipeline.fit(data['text'].values, data['class'].values)

    #print("Predicting")

    #examples = ['Free Viagra call today!', "I'm going to attend the Linux users group tomorrow."]

    #predictions = pipeline.predict(examples)

    #print(predictions)

    k_fold = KFold(n=len(data), n_folds=6)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])

    fold = 0
    for train_indicies, test_indicies in k_fold:
        fold += 1
        print('Fold:', fold)
        train_text = data.iloc[train_indicies]['text'].values
        train_y = data.iloc[train_indicies]['class'].values

        test_text = data.iloc[test_indicies]['text'].values
        test_y = data.iloc[test_indicies]['class'].values

        pipeline.fit(train_text, train_y)
        predictions = pipeline.predict(test_text)

        confusion += confusion_matrix(test_y, predictions)
        score = f1_score(test_y, predictions, pos_label=SPAM)
        scores.append(score)

    print('Total emails classified:', len(data))
    print('Score:', sum(scores)/len(scores))
    print('Confusion Matrix:')
    print(confusion)
