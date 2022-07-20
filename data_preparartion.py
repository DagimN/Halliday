import numpy as np
from sklearn import preprocessing

input_data = np.array([[2.1, -1.9, 5.5],
                      [-1.5, 2.4, 3.5],
                      [0.5, -7.9, 5.6],
                      [5.9, 2.3, -5.8]])

data_binarized = preprocessing.Binarizer(threshold=0.5).transform(input_data)
print("\nBinarized data:\n", data_binarized)

print()
print("Mean = ", input_data.mean(axis=0))
print("Std Deviation = ", input_data.std(axis=0))

print()
data_scaled = preprocessing.scale(input_data)
print("Mean = ", data_scaled.mean(axis=0))
print("Std Deviation = ", data_scaled.std(axis=0))

print()
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 6))
data_scaled_minmax = data_scaler_minmax.fit_transform(input_data)
print("Min Max Scaled Data:\n", data_scaled_minmax)

print()
data_normalized_l1 = preprocessing.normalize(input_data, norm='l1');
print('\n L1 Normalized data: \n', data_normalized_l1)

input_labels = ['red', 'black', 'red', 'green', 'black', 'yellow', 'white']
encoder = preprocessing.LabelEncoder()
encoder.fit(input_labels)

test_labels = ['green', 'red', 'black']
encoded_values = encoder.transform(test_labels)
print("\nEncoded Values: ", encoded_values)

encoded_values = [3,0,4,1]
decoded_list = encoder.inverse_transform(encoded_values)
print("\nDecoded Values: ", list(decoded_list))

