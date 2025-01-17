import csv
import random

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

negative = []
with open("./data/negative_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			negative.append(line)

positive = []
with open("./data/positive_labels.tsv", 'r', encoding='UTF8') as f:
	reader = csv.reader(f, delimiter='\t')
	for line in reader:
		if len(line) > 0:
			positive.append(line)

random.shuffle(negative)
random.shuffle(positive)

length = len(positive)
negative_data = negative[:length]

train_data = negative_data[:length//5*4]+positive[:length//5*4]
test_data = negative_data[length//5*4:]+positive[length//5*4:]

train_X = [s[1] for s in train_data]
train_y = [s[2] for s in train_data]
test_X = [s[1] for s in test_data]
test_y = [s[2] for s in test_data]

nb = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
              ])
sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
logreg = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(n_jobs=1, C=1e5)),
               ])

nb.fit(train_X, train_y)
sgd.fit(train_X, train_y)
logreg.fit(train_X, train_y)
pred_y_nb = nb.predict(test_X)
pred_y_sgd = sgd.predict(test_X)
pred_y_logreg = logreg.predict(test_X)

print('nb accuracy %s' % accuracy_score(pred_y_nb, test_y))
print('sgd accuracy %s' % accuracy_score(pred_y_sgd, test_y))
print('logreg accuracy %s' % accuracy_score(pred_y_logreg, test_y))