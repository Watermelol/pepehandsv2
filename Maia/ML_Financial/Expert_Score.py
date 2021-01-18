#Importing required packages
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle



#Reading the csv and creating a dataframe
ds = pd.read_csv(r'Overall Data.csv')

#Labels are values we are predicting
labels = np.array(ds['Expert_S'])

#Features are our variables being inputted to help calculate our labels
#For this, we are using all the variables inside the dataframe except the one listed below as they are unobtainable for unseen data
#features = ds.drop(columns=['P_S', 'Name', 'Sector', 'Expert_S', 'A_S', 'D_C_S', 'L_S', 'Goodwill' ])
features = ds[['P_S', 'A_S', 'D_C_S', 'L_S']]


#Dropping all null variables (Yet they are no null variables)
features.dropna()

#printing an examples of the feature variables
#print(features.head())

#Used for later use
feature_list = list(features.columns)

#Used to convert to a numpy array
features = np.array(features)

#Splitting of training and testing with training being 75% & testing 25%. Random state refers to a way we keep track
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#print('Training Features Shape:', train_features.shape)
#print('Training Labels Shape:', train_labels.shape)
#print('Testing Features Shape:', test_features.shape)
#print('Testing Labels Shape:', test_labels.shape)

# Instantiate model with 1000 decision trees
#Using regressor since our label is continuous and is based on multiple variables
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);

#Uses random forest predict method on test data
predictions = rf.predict(test_features)
#Rounding our prediction to 1 decimal places
predictions = [np.round(x,1) for x in predictions]


#Printing predictions for physical comparison
print(predictions)
#Printing actual for physical comparison
print(test_labels)

#Calculate absolute errors
errors = (predictions - test_labels)
#Printing errors for physical comparison
print(errors)


# Calculate mean absolute percentage error (MAPE)
mape = 100 * abs(errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')




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

pickle.dump(rf, open("../Expert_Score_Model.sav", "wb"))




