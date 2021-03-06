# SVM and Random Forest
# Team Project

from sklearn_pandas import DataFrameMapper
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy.sparse import csr_matrix
import scikitplot as skplt
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def char_flag(l):
    if l <= 40:
        return 1
    elif l <= 60:
        return 2
    elif l <= 80:
        return 3
    elif l <= 120:
        return 4
    elif l <= 160:
        return 5
    else:
        return 6


def preprocessing_text():
    for d, ln in zip(messages_data, token_4):
        token_1.append(d)
        token_2.append(d.count('$'))
        x = re.sub('[^0-9 ]+', '', d.lower())
        token_3.append(len(x))
        token_5.append(char_flag(ln))
        if (re.sub(r'[^://@]', '', d.lower())) is not '':
            token_6.append(1)
        else:
            token_6.append(0)

    return np.array(
        [np.array([token_1[i], token_2[i], token_3[i], token_4[i], token_5[i], token_6[i]], dtype=object) for i in
         range(len(messages_data))])


def text_process(mess):
    no_punct = re.sub('[^A-Za-z ]+', '', mess.lower())
    return np.array([word for word in no_punct.split() if word not in stopwords.words('english')])


if __name__ == "__main__":
    messages = pd.read_csv("spam.csv", encoding='latin-1')
    messages = messages.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'])

    print(messages.head(5))
    messages_labels = messages['v1']
    messages['length'] = messages['v2'].apply(len)
    messages_data = messages['v2']

    token_1 = []
    token_2 = []
    token_3 = []
    token_4 = messages['length']
    token_5 = []
    token_6 = []
    
    count_vect = CountVectorizer()
    x_counts = count_vect.fit(messages_data)
    x_int = count_vect.transform(messages_data)   
    x_int = list(x_int)
    
    data = preprocessing_text()
    labels = ['message','f1','f2','f3','f4','f5']
    df = pd.DataFrame.from_records(data,columns=labels)
    mapper = DataFrameMapper([
    (['f1', 'f2','f3','f4','f5'], None),
    ('message',CountVectorizer(binary=True, ngram_range=(1, 2)))                          ])
    X=mapper.fit_transform(df)
    print("X "+str(X))
    print("X "+str(X.shape))
    trainset, testset, trainlabel, testlabel = train_test_split(X, messages_labels, test_size=0.33, random_state=42)


    SVM = svm.SVC()
    SVM.fit(trainset, trainlabel)
    predicted_values_svm = SVM.predict(testset)
    print(predicted_values_svm)
    acurracy_SVM = accuracy_score(testlabel, predicted_values_svm)
    print("acurracy_SVM " + str(acurracy_SVM))
    confusion_matrix_SVM = confusion_matrix(testlabel,predicted_values_svm,labels=["spam", "ham"])
    print(confusion_matrix_SVM)
    skplt.metrics.plot_confusion_matrix(testlabel,predicted_values_svm, normalize=True)
    plt.show()
