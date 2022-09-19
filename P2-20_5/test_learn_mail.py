#import seaborn as sns
#import matplotlib.pyplot as plt

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

mails = pd.read_csv('dataset.csv', sep=',')

mails.info()
mails.isnull().sum()

X = mails.drop(['class'], axis=1)
y = mails['class']

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.25 )
pX_train = X_train  #X_train preserving (before StandardScaler.fit_transform) for pickle file


##  Transform ##
sc1 = StandardScaler()
sc2 = MinMaxScaler()
sc = sc1

sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)

#print("\n\nX_train:\n",X_train, "\n\n")


#---- Randon Forest Classifire (sklearn.ensemble) -----# 
rfc = RandomForestClassifier(n_estimators = 300, bootstrap = True, criterion = 'gini')
rfc.fit(X_train,y_train)
rfc_output = rfc.predict(X_test)
#print(rfc_output[:30])

print(classification_report(y_test, rfc_output))
print(confusion_matrix(y_test, rfc_output))

#---- SVM Classifire (sklearn.svm) ----#
clf = SVC()
clf.fit(X_train,y_train)
clf_output = clf.predict(X_test)

print(classification_report(y_test, clf_output))
print(confusion_matrix(y_test, clf_output))

#---- Neural Networks (sklearn.neural_network) ----#
mlpc =  MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=500)
mlpc.fit(X_train,y_train)
mlpc_output = mlpc.predict(X_test)

print(classification_report(y_test, mlpc_output))
print(confusion_matrix(y_test, mlpc_output))

#-- Accuracy --#
print("\nRFC :", accuracy_score(y_test, rfc_output))
print("SVC :", accuracy_score(y_test, clf_output))
print("Neu :", accuracy_score(y_test, mlpc_output))

#---- Cross validation score ----#
print("\nCross validation scores\n------------------------")
scores = cross_val_score(rfc, X_train, y_train, cv=6 ) # 'cv' = cross validations 
print("RFC \n", "Mean:", scores.mean(), "\n S.Deviation:", scores.std(), "\n", scores)

#---- 'Grid Search' Cross validation score ----#
new_rfc = RandomForestClassifier()

grid_param = { 'n_estimators': [100, 300, 500, 800, 1000], 'criterion': ['gini', 'entropy'], 'bootstrap': [True, False] }
gd_sr = GridSearchCV(estimator=new_rfc, param_grid=grid_param, scoring='accuracy', cv=10, n_jobs = -1)

gd_sr.fit(X_train, y_train)
best_parameters = gd_sr.best_params_  
print("\nBest settings", best_parameters)


#----------------------------------------------------------------------------



