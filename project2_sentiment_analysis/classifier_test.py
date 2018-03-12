__author__ = 'dmitry_sh'
# coding: utf-8

from sentiment_classifier import SentimentClassifier

clf = SentimentClassifier()

pred = clf.get_prediction_message("Очень хороший телефон!!!")

print (pred)