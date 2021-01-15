from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from pprint import pprint



#Read csv
ds = pd.read_csv(r'Assets Data.csv')

#Labels are values we are predicting
labels = np.array(ds['A_S'])

#Features are our variables
features = ds.drop(columns=['P_S', 'Name', 'Sector', 'Expert_S', 'A_S', 'D_C_S', 'L_S', 'Goodwill', 'Q3_NP', 'Q4_NP', 'Q2_NP', 'Q1_NP', 'Q1_PBT', 'Q2_PBT', 'Q3_PBT', 'Q4_PBT', 'Y_NP', 'Q3_R', 'Q2_R', 'Q1_R', 'Q4_R', 'Y_R' ])


features.dropna()


print(features.head())

feature_list = list(features.columns)

features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#print('Training Features Shape:', train_features.shape)
#print('Training Labels Shape:', train_labels.shape)
#print('Testing Features Shape:', test_features.shape)
#print('Testing Labels Shape:', test_labels.shape)

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}









# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(random_state=42)
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Train the model on training data
rf_random.fit(train_features, train_labels)
rf_random.best_params_

predictions = rf_random.predict(test_features)
#tpredictions = rf.predict(train_features)

predictions = [np.round(x,1) for x in predictions]

print(predictions)
print(test_labels)


errors = (predictions - test_labels)
#terrors = abs(tpredictions - train_labels)
print(errors)


# Calculate mean absolute percentage error (MAPE)
mape = 100 * abs(errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')


#tmape = 100 * (terrors / train_labels)
#taccuracy = 100 - np.mean(tmape)
#print('test accuarcy: ', round(taccuracy, 2), '%.')



# Get numerical feature importances
importances = list(rf_random.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];




