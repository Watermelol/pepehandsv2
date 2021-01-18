from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pickle



#Read csv
ds = pd.read_csv(r'Dividend Cash Data.csv')

#Labels are values we are predicting
labels = np.array(ds['D_C_S'])

#Features are our variables
#features = ds.drop(columns=['P_S', 'Name', 'Sector', 'Expert_S', 'A_S', 'D_C_S', 'L_S', 'Goodwill' ])
features = ds[['Cash_Ratio', 'CR', 'NTA', 'Y_NP', 'Debt', 'CTR', 'Cash']]

features.dropna()


print(features.head())

feature_list = list(features.columns)

features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#print('Training Features Shape:', train_features.shape)
#print('Training Labe ls Shape:', train_labels.shape)
#print('Testing Features Shape:', test_features.shape)
#print('Testing Labels Shape:', test_labels.shape)

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);

predictions = rf.predict(test_features)
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



# Pull out one tree from the forest
tree = rf.estimators_[5]
# Import tools needed for visualization
from sklearn.tree import export_graphviz
import pydot
# Pull out one tree from the forest
tree = rf.estimators_[5]
# Export the image to a dot file
export_graphviz(tree, out_file ='../tree.dot', feature_names = None, rounded = True, precision = 1)
# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('../tree.dot')
# Write graph to a png file
graph.write_png('tree.png')

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

pickle.dump(rf, open("../Cash_Score_Model.sav", "wb"))


