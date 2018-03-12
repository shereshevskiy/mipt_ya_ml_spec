__author__ = 'dmitry_sh'

import pickle as pkl
import os
import pymorphy2 # с русским языком, в отличие от nltk.stem.WordNetLemmatizer

abs_path = 'C:/Users/dsher/OneDrive/Documents/!_SkillsEvolution/ML/\
mipt_ya_ml_spec/practice/6_Final_project/sentiment_analysis/week7_final_project_APP'
# приходится использовать абсолютный путь, потому что в консоле на винде
# относительный путь не "прокатывает", как в ноутбуке или в отладчике на Spyder

path_to_data = ('data' )


class MobilereviewClassifier(object):
    def __init__(self):
        with open(os.path.join(abs_path, path_to_data, 'mobilereview_model.pkl'), 'rb') as model_pkl,\
             open(os.path.join(abs_path, path_to_data, 'mobilereview_vectorizer.pkl'), 'rb') as vectorizer_pkl:
            self.model = pkl.load(model_pkl)
            self.vectorizer = pkl.load(vectorizer_pkl)
        self.classes_dict = {0: "negative", 
                             1: "positive", 
                            -1: "prediction error"}


    @staticmethod
    def get_probability_words(probability):
        if probability < 0.55:
            return "neutral or uncertain"
        if probability < 0.7:
            return "probably"
        if probability > 0.95:
            return "certain"
        else:
            return ""

    def predict_text(self, text):
        
        # предобработка текста
        
        # замена некоторых символов и их сочетаний на пробелы
        def del_any_symbols(text):
            return (text.replace('\n', ' ').replace('\r', ' ').replace('<br />', ' ').replace('\t', ' ').replace('&quot;', ' ') 
               .replace('.', ' ').replace(',', ' ').replace('!', ' ! ').replace('?', ' ? ').replace(':', ' ').replace(';', ' '))
        # удаление пунктуации
        def del_punctuation(text):
            return ''.join(symbol for symbol in text if symbol not in '"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~')
        # лемматизация
        def lemmatizer(text):
            pymorph = pymorphy2.MorphAnalyzer()
            return' '.join([pymorph.parse(word)[0].normal_form for word in text.split(' ') if word not in ['']])
        # общий препроцессинг текста
        def text_preprocessing(text):
            return lemmatizer(del_punctuation(del_any_symbols(text)))
        
        try:
            vectorized = self.vectorizer.transform([text_preprocessing(text)])
            return self.model.predict(vectorized)[0],\
                   self.model.predict_proba(vectorized)[0].max()
        except:
            print ("prediction error")
            return -1, 0.8

#    def predict_list(self, list_of_texts):
#        try:
#            vectorized = self.vectorizer.transform(list_of_texts)
#            return self.model.predict(vectorized),\
#                   self.model.predict_proba(vectorized)
#        except:
#            print ('prediction error')
#            return None

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        class_prediction = prediction[0]
        prediction_probability = prediction[1]
        return self.get_probability_words(prediction_probability) + " " + self.classes_dict[class_prediction]