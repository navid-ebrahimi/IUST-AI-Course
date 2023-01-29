import pandas as pd
import numpy as np
import math

df = pd.read_csv('iris.data')

class Species:
  def __init__(self, name):
    self.name = name
    self.count = 0
    self.sepal_length_mean = 0
    self.sepal_width_mean = 0
    self.petal_length_mean = 0
    self.petal_width_mean = 0
    self.sepal_length_standard_division = 0
    self.sepal_width_standard_division = 0
    self.petal_length_standard_division = 0
    self.petal_width_standard_division = 0
    self.probability = 0
# mean of first 120 items 
df = pd.read_csv('iris.data')
df = df.sample(frac=1)
Iris_setosa = Species('Iris-setosa')
Iris_versicolor = Species('Iris-versicolor')
Iris_virginica = Species('Iris-virginica')
for i in range(120):
  if df.iloc[i][4] == 'Iris-setosa':
    Iris_setosa.sepal_length_mean += df.iloc[i][0]
    Iris_setosa.sepal_width_mean += df.iloc[i][1]
    Iris_setosa.petal_length_mean += df.iloc[i][2]
    Iris_setosa.petal_width_mean += df.iloc[i][3]
    Iris_setosa.count += 1
  elif df.iloc[i][4] == 'Iris-versicolor':
    Iris_versicolor.sepal_length_mean += df.iloc[i][0]
    Iris_versicolor.sepal_width_mean += df.iloc[i][1]
    Iris_versicolor.petal_length_mean += df.iloc[i][2]
    Iris_versicolor.petal_width_mean += df.iloc[i][3]
    Iris_versicolor.count += 1
  elif df.iloc[i][4] == 'Iris-virginica':
    Iris_virginica.sepal_length_mean += df.iloc[i][0]
    Iris_virginica.sepal_width_mean += df.iloc[i][1]
    Iris_virginica.petal_length_mean += df.iloc[i][2]
    Iris_virginica.petal_width_mean += df.iloc[i][3]
    Iris_virginica.count += 1
Iris_setosa.sepal_length_mean /= Iris_setosa.count
Iris_setosa.sepal_width_mean /= Iris_setosa.count
Iris_setosa.petal_length_mean /= Iris_setosa.count
Iris_setosa.petal_width_mean /= Iris_setosa.count
Iris_versicolor.sepal_length_mean /= Iris_versicolor.count
Iris_versicolor.sepal_width_mean /= Iris_versicolor.count
Iris_versicolor.petal_length_mean /= Iris_versicolor.count
Iris_versicolor.petal_width_mean /= Iris_versicolor.count
Iris_virginica.sepal_length_mean /= Iris_virginica.count
Iris_virginica.sepal_width_mean /= Iris_virginica.count
Iris_virginica.petal_length_mean /= Iris_virginica.count
Iris_virginica.petal_width_mean /= Iris_virginica.count
# standard division of first 120 items
for i in range(120):
  if df.iloc[i][4] == 'Iris-setosa':
    Iris_setosa.sepal_length_standard_division += (df.iloc[i][0] - Iris_setosa.sepal_length_mean) ** 2
    Iris_setosa.sepal_width_standard_division += (df.iloc[i][1] - Iris_setosa.sepal_width_mean) ** 2
    Iris_setosa.petal_length_standard_division += (df.iloc[i][2] - Iris_setosa.petal_length_mean) ** 2
    Iris_setosa.petal_width_standard_division += (df.iloc[i][3] - Iris_setosa.petal_width_mean) ** 2
  elif df.iloc[i][4] == 'Iris-versicolor':
    Iris_versicolor.sepal_length_standard_division += (df.iloc[i][0] - Iris_versicolor.sepal_length_mean) ** 2
    Iris_versicolor.sepal_width_standard_division += (df.iloc[i][1] - Iris_versicolor.sepal_width_mean) ** 2
    Iris_versicolor.petal_length_standard_division += (df.iloc[i][2] - Iris_versicolor.petal_length_mean) ** 2
    Iris_versicolor.petal_width_standard_division += (df.iloc[i][3] - Iris_versicolor.petal_width_mean) ** 2
  elif df.iloc[i][4] == 'Iris-virginica':
    Iris_virginica.sepal_length_standard_division += (df.iloc[i][0] - Iris_virginica.sepal_length_mean) ** 2
    Iris_virginica.sepal_width_standard_division += (df.iloc[i][1] - Iris_virginica.sepal_width_mean) ** 2
    Iris_virginica.petal_length_standard_division += (df.iloc[i][2] - Iris_virginica.petal_length_mean) ** 2
    Iris_virginica.petal_width_standard_division += (df.iloc[i][3] - Iris_virginica.petal_width_mean) ** 2
Iris_setosa.sepal_length_standard_division = (Iris_setosa.sepal_length_standard_division / Iris_setosa.count) ** 0.5
Iris_setosa.sepal_width_standard_division = (Iris_setosa.sepal_width_standard_division / Iris_setosa.count) ** 0.5
Iris_setosa.petal_length_standard_division = (Iris_setosa.petal_length_standard_division / Iris_setosa.count) ** 0.5
Iris_setosa.petal_width_standard_division = (Iris_setosa.petal_width_standard_division / Iris_setosa.count) ** 0.5
Iris_versicolor.sepal_length_standard_division = (Iris_versicolor.sepal_length_standard_division / Iris_versicolor.count) ** 0.5
Iris_versicolor.sepal_width_standard_division = (Iris_versicolor.sepal_width_standard_division / Iris_versicolor.count) ** 0.5
Iris_versicolor.petal_length_standard_division = (Iris_versicolor.petal_length_standard_division / Iris_versicolor.count) ** 0.5
Iris_versicolor.petal_width_standard_division = (Iris_versicolor.petal_width_standard_division / Iris_versicolor.count) ** 0.5
Iris_virginica.sepal_length_standard_division = (Iris_virginica.sepal_length_standard_division / Iris_virginica.count) ** 0.5
Iris_virginica.sepal_width_standard_division = (Iris_virginica.sepal_width_standard_division / Iris_virginica.count) ** 0.5
Iris_virginica.petal_length_standard_division = (Iris_virginica.petal_length_standard_division / Iris_virginica.count) ** 0.5
Iris_virginica.petal_width_standard_division = (Iris_virginica.petal_width_standard_division / Iris_virginica.count) ** 0.5
# probability of each species
Iris_setosa.probability = Iris_setosa.count / 120
Iris_versicolor.probability = Iris_versicolor.count / 120
Iris_virginica.probability = Iris_virginica.count / 120

# calculate the probability of each feature
def calculate_probability(feature, species, feature_name):
  if feature_name == 'sepal_length' and species == 'Iris-setosa':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_setosa.sepal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_setosa.sepal_length_mean)**2 / (Iris_setosa.sepal_length_standard_division) ** 2)
  elif feature_name == 'sepal_width' and species == 'Iris-setosa':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_setosa.sepal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_setosa.sepal_width_mean)**2 / (Iris_setosa.sepal_width_standard_division) ** 2)
  elif feature_name == 'petal_length' and species == 'Iris-setosa':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_setosa.petal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_setosa.petal_length_mean)**2 / (Iris_setosa.petal_length_standard_division) ** 2)
  elif feature_name == 'petal_width' and species == 'Iris-setosa':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_setosa.petal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_setosa.petal_width_mean)**2 / (Iris_setosa.petal_width_standard_division) ** 2)
  elif feature_name == 'sepal_length' and species == 'Iris-versicolor':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_versicolor.sepal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_versicolor.sepal_length_mean)**2 / (Iris_versicolor.sepal_length_standard_division) ** 2)
  elif feature_name == 'sepal_width' and species == 'Iris-versicolor':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_versicolor.sepal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_versicolor.sepal_width_mean)**2 / (Iris_versicolor.sepal_width_standard_division) ** 2)
  elif feature_name == 'petal_length' and species == 'Iris-versicolor':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_versicolor.petal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_versicolor.petal_length_mean)**2 / (Iris_versicolor.petal_length_standard_division) ** 2)
  elif feature_name == 'petal_width' and species == 'Iris-versicolor':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_versicolor.petal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_versicolor.petal_width_mean)**2 / (Iris_versicolor.petal_width_standard_division) ** 2)
  elif feature_name == 'sepal_length' and species == 'Iris-virginica':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_virginica.sepal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_virginica.sepal_length_mean)**2 / (Iris_virginica.sepal_length_standard_division) ** 2)
  elif feature_name == 'sepal_width' and species == 'Iris-virginica':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_virginica.sepal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_virginica.sepal_width_mean)**2 / (Iris_virginica.sepal_width_standard_division) ** 2)
  elif feature_name == 'petal_length' and species == 'Iris-virginica':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_virginica.petal_length_standard_division)) * math.exp(-0.5 * (feature - Iris_virginica.petal_length_mean)**2 / (Iris_virginica.petal_length_standard_division) ** 2)
  elif feature_name == 'petal_width' and species == 'Iris-virginica':
    return (1 / ((2 * math.pi) ** 0.5 * Iris_virginica.petal_width_standard_division)) * math.exp(-0.5 * (feature - Iris_virginica.petal_width_mean)**2 / (Iris_virginica.petal_width_standard_division) ** 2)



# calculate the probability of each species

list_of_predictions_species = [0 for i in range(30)]
for i in range(120, 150):
  Iris_setosa_data = Iris_setosa.probability * calculate_probability(df.iloc[i][0], 'Iris-setosa', 'sepal_length') * calculate_probability(df.iloc[i][1], 'Iris-setosa', 'sepal_width') * calculate_probability(df.iloc[i][2], 'Iris-setosa', 'petal_length') * calculate_probability(df.iloc[i][3], 'Iris-setosa', 'petal_width')
  Iris_versicolor_data = Iris_versicolor.probability * calculate_probability(df.iloc[i][0], 'Iris-versicolor', 'sepal_length') * calculate_probability(df.iloc[i][1], 'Iris-versicolor', 'sepal_width') * calculate_probability(df.iloc[i][2], 'Iris-versicolor', 'petal_length') * calculate_probability(df.iloc[i][3], 'Iris-versicolor', 'petal_width')
  Iris_virginica_data = Iris_virginica.probability * calculate_probability(df.iloc[i][0], 'Iris-virginica', 'sepal_length') * calculate_probability(df.iloc[i][1], 'Iris-virginica', 'sepal_width') * calculate_probability(df.iloc[i][2], 'Iris-virginica', 'petal_length') * calculate_probability(df.iloc[i][3], 'Iris-virginica', 'petal_width')
  if Iris_setosa_data > Iris_versicolor_data and Iris_setosa_data > Iris_virginica_data:
    list_of_predictions_species[i - 120] = 0
  elif Iris_versicolor_data > Iris_setosa_data and Iris_versicolor_data > Iris_virginica_data:
    list_of_predictions_species[i - 120] = 1
  elif Iris_virginica_data > Iris_setosa_data and Iris_virginica_data > Iris_versicolor_data:
    list_of_predictions_species[i - 120] = 2

correct_predictions = 0
Iris_setosa_correct_predictions = 0
Iris_setosa_count = 0
Iris_versicolor_correct_predictions = 0
Iris_versicolor_count = 0
Iris_virginica_correct_predictions = 0
Iris_virginica_count = 0

for i in range(120, 150):
  if df.iloc[i][4] == 'Iris-setosa':
    Iris_setosa_count += 1
    if list_of_predictions_species[i - 120] == 0:
      Iris_setosa_correct_predictions += 1
      correct_predictions += 1
  elif df.iloc[i][4] == 'Iris-versicolor':
    Iris_versicolor_count += 1
    if list_of_predictions_species[i - 120] == 1:
      Iris_versicolor_correct_predictions += 1
      correct_predictions += 1
  elif df.iloc[i][4] == 'Iris-virginica':
    Iris_virginica_count += 1
    if list_of_predictions_species[i - 120] == 2:
      Iris_virginica_correct_predictions += 1
      correct_predictions += 1

print('Accuracy of the model is: ', correct_predictions / 30 * 100, '%')
print('Accuracy of the model for Iris-setosa is: ', Iris_setosa_correct_predictions / Iris_setosa_count * 100, '%')
print('Accuracy of the model for Iris-versicolor is: ', Iris_versicolor_correct_predictions / Iris_versicolor_count * 100, '%')
print('Accuracy of the model for Iris-virginica is: ', Iris_virginica_correct_predictions / Iris_virginica_count * 100, '%')



