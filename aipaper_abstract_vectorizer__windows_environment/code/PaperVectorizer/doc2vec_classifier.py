import csv
import random
import sys

from gensim.models.doc2vec import Doc2Vec
from dataloader import tokenize_string

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

train_data = []
with open("./data/train_1.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      train_data.append(line)

random.shuffle(train_data)

test_data = []
with open("./data/test_1.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      test_data.append(line)

random.shuffle(test_data)

train_X = [s[1] for s in train_data]
train_y = [s[2] for s in train_data]
test_X = [s[1] for s in test_data]
test_y = [s[2] for s in test_data]

model = Doc2Vec.load(sys.argv[1])
train_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in train_X]
test_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in test_X]

sgd_doc2vec = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)
logreg_doc2vec = LogisticRegression(n_jobs=1, C=1e5)

sgd_doc2vec.fit(train_X_doc2vec, train_y)
logreg_doc2vec.fit(train_X_doc2vec, train_y)

pred_y_sgd_doc2vec = sgd_doc2vec.predict(test_X_doc2vec)
pred_y_logreg_doc2vec = logreg_doc2vec.predict(test_X_doc2vec)

test_data2 = []
with open("./data/fat_test.tsv", 'r', encoding='UTF8') as f:
  reader = csv.reader(f, delimiter='\t')
  for line in reader:
    if len(line) > 0:
      test_data2.append(line)

train_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in train_X]
test_X_doc2vec = [model.infer_vector(tokenize_string(s)) for s in test_X]

print('doc2vec model')
print('sgd accuracy %s' % accuracy_score(pred_y_sgd_doc2vec, test_y))
print('logreg accuracy %s\n' % accuracy_score(pred_y_logreg_doc2vec, test_y))

train_X_doc2vec = [model.infer_vector(tokenize_string(s[0])) for s in test_data2]
test_X_doc2vec = [model.infer_vector(tokenize_string(s[0])) for s in test_data2]
pred_y_sgd_doc2vec2 = sgd_doc2vec.predict(test_X_doc2vec)
pred_y_logreg_doc2vec2 = logreg_doc2vec.predict(test_X_doc2vec)

print('sgd accuracy2 %s' % accuracy_score(pred_y_sgd_doc2vec2, [s[1] for s in test_data2]))
print('logreg accuracy2 %s\n' % accuracy_score(pred_y_logreg_doc2vec2, [s[1] for s in test_data2]))

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

print('fsd')
print('nb accuracy %s' % accuracy_score(pred_y_nb, test_y))
print('sgd accuracy %s' % accuracy_score(pred_y_sgd, test_y))
print('logreg accuracy %s' % accuracy_score(pred_y_logreg, test_y))