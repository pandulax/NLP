#import seaborn as sns
#import matplotlib.pyplot as plt
import  pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
#from sklearn import svm
#from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

#def execute_learn():
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
rfc = RandomForestClassifier(n_estimators = 500, random_state=None, bootstrap = False, criterion = 'entropy')
rfc.fit(X_train,y_train)
rfc_output = rfc.predict(X_test)

print(classification_report(y_test, rfc_output))
print(confusion_matrix(y_test, rfc_output))


#---- Extra Trees Classifier(sklearn.ensemble) -----# 
etc = ExtraTreesClassifier(n_estimators=500, random_state=None, bootstrap = False, criterion = 'entropy')
etc.fit(X_train,y_train)
etc_output = etc.predict(X_test)

print(classification_report(y_test, etc_output))
print(confusion_matrix(y_test, etc_output))


#---- SVM Classifire (sklearn.svm) ----#
clf = SVC()
clf.fit(X_train,y_train)
clf_output = clf.predict(X_test)

print(classification_report(y_test, clf_output))
print(confusion_matrix(y_test, clf_output))


#-- Accuracy --#
print("\n")
print("RFC :", accuracy_score(y_test, rfc_output))
print("ETC :", accuracy_score(y_test, etc_output))
print("SVC :", accuracy_score(y_test, clf_output))

#----------------------------------------------------------------------------

RFCstr = str(accuracy_score(y_test, rfc_output)*100)[:5]
ETCstr = str(accuracy_score(y_test, etc_output)*100)[:5]


#--- Writting to pickle ---#
model_rfc = rfc
model_etc = etc
scaler = sc

#Xtrain = X_train
#Ytrain = y_train
#params = { 'n_estimators' : 500, 'criterion' : 'entropy' }

from datetime import datetime
time_tag = datetime.now().strftime("%y%m%d_%H%M%S")

RFC_pklname = 'RFC_'+RFCstr+'_SC_'+time_tag
ETC_pklname = 'ETC_'+ETCstr+'_SC_'+time_tag

pickle.dump( [model_rfc, scaler], open( RFC_pklname+'.pkl' , 'wb') )

pickle.dump( [model_etc, scaler], open( ETC_pklname+'.pkl' , 'wb') )

#--------------------------#
