# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:37:58 2016

@author: Abdullah
"""
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
import xlsxwriter

data2 = pd.read_table('trainingData.txt', encoding='latin-1')
print(data2.head())
print(data2.tail())
print(data2.shape)

X = data2.ix[:,1]
#print (type(X))
print (X.shape)
#print (X.head)

y = data2.ix[:,0]
#print (type(y))
print (y.shape)
#print (y.head)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
print (X_train.shape)
print (X_test.shape)

# Preprocess into matrix of token counts
count_vect = CountVectorizer(ngram_range=(1, 2), decode_error='ignore', max_df=0.5)
X_train_counts = count_vect.fit_transform(X_train)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Train the models
clf = MultinomialNB()

clf.fit(X_train_tfidf, y_train)

X_test_counts = count_vect.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

# Predict the labels
y_pred = clf.predict(X_test_tfidf)

# Now actual test
data1 = pd.read_csv('AllYouTubeComments.csv', encoding='latin-1')
print(data1.head())
print(data1.tail())
print(data1.shape)

# Get the actual youtube comments test input and preprocess
X_test = data1.ix[:,1]

X_test_counts = count_vect.transform(X_test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

# Predict the labels
y_pred = clf.predict(X_test_tfidf)

workbook = xlsxwriter.Workbook('AllCommentsSentiment.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
worksheet.write(row, col, "Author")
worksheet.write(row, col+1, "Comment")
worksheet.write(row, col+2, "Date")
worksheet.write(row, col+3, "Time")
worksheet.write(row, col+4, "Type")
worksheet.write(row, col+5, "Sentiment")
#print (vect[4])

row = 1
col = 0
i = 0
for sentiment in (y_pred):
    vect = data1.ix[i,:]
    worksheet.write(row, col, vect[0])
    worksheet.write(row, col+1, vect[1])
    worksheet.write(row, col+2, vect[2])
    worksheet.write(row, col+3, vect[3])
    worksheet.write(row, col+4, vect[4])
    worksheet.write(row, col+5, sentiment)
    row += 1
    col = 0
    i +=1
    
workbook.close()

    






