import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


##voting system between all classifiers, whichever category positive or negative
##gets most votes from all of the classifiers at the bottom, that's we are going to use
##improves accuracy and 'confidence' parameter
class VoteClassifier(ClassifierI):
    ##the method below will always run when we invoke the class
    ##whereas the rest of the methods won't run unless you call upon them
    ##pass a list of classifiers
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            ##get the vote for each classifier
            votes.append(v)
            ##return who got the most votes
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


##Pickle - saving algorithms and objects so you don't have to retrain it
##or reload the objects.

##loading the documents which we are extracting data from
documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()


##finding out which words are commonly positive or negative
word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


##find features within the example documents
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features



featuresets_f = open("pickled_algos/word_features5k.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

##second 10000 words
testing_set = featuresets[10000:]
##first 10000 words
training_set = featuresets[:10000]


##Pickle the Naive Bayes algorithm - the algorithm makes very strong
##independent decisions, a scalable algorithm which doens't take too much processing
##algorithm model : posterior = prior occurences x likelihood / evidence
open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()



open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


#open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
#LogisticRegression_classifier = pickle.load(open_file)
#open_file.close()


#open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
#LinearSVC_classifier = pickle.load(open_file)
#open_file.close()


#open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
#SGDC_classifier = pickle.load(open_file)
#open_file.close()



##list of classifiers we have used above
voted_classifier = VoteClassifier(
                                  classifier,
                                  
                                    MNB_classifier,
                                  BernoulliNB_classifier,
                            )



##return classification and confidence score
def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
