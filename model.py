import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df= pd.read_csv('kerala.csv')
dff = df.head(5)

# print(dff)
# print(df.info())

# print(df.shape)

# print(df.describe())

# print(df.corr())

df['FLOODS'].replace(['YES', 'NO'], [1,0], inplace=True)
print(df.head(5))

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

X= df.iloc[:,1:14]   #all features
Y= df.iloc[:,-1]   #target output (floods)

best_features= SelectKBest(score_func=chi2, k=3)
fit= best_features.fit(X,Y)

df_scores= pd.DataFrame(fit.scores_)
df_columns= pd.DataFrame(X.columns)

features_scores= pd.concat([df_columns, df_scores], axis=1)
features_scores.columns= ['Features', 'Score']
features_scores.sort_values(by = 'Score')

X= df[['SEP', 'JUN', 'JUL']]  #the top 3 features
Y= df[['FLOODS']]  #the target output

X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.4,random_state=100)

logreg= LogisticRegression()
logreg.fit(X_train,y_train)

y_pred=logreg.predict(X_test)
print (X_test) #test dataset
print (y_pred) #predicted values

from sklearn import metrics
from sklearn.metrics import classification_report
print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))
print('Recall: ',metrics.recall_score(y_test, y_pred, zero_division=1))
print("Precision:",metrics.precision_score(y_test, y_pred, zero_division=1))
print("CL Report:",metrics.classification_report(y_test, y_pred, zero_division=1))

y_pred_proba= logreg.predict_proba(X_test) [::,1]

false_positive_rate, true_positive_rate, _ = metrics.roc_curve(y_test, y_pred_proba)

auc= metrics.roc_auc_score(y_test, y_pred_proba)

plt.plot(false_positive_rate, true_positive_rate,label="AUC="+str(auc))
plt.title('ROC Curve')
plt.ylabel('True Positive Rate')
plt.xlabel('false Positive Rate')
plt.legend(loc=4)
plt.show()
#plt.save("roc.png")
