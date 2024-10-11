# -*- coding: utf-8 -*-
"""Project_MNIST.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QzFAukyi52y1fWR73ilgpFWLA6U0YD4x
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

"""# Data"""

train = pd.read_csv("/content/sample_data/mnist_train_small.csv")
test = pd.read_csv("/content/sample_data/mnist_test.csv")

train.head()

# 28*28 -> 784
len(train.index)

len(test.index)

test.head()

train.rename(columns={'6':"Label"},inplace=True)
test.rename(columns={'7':"Label"},inplace=True)

train.head()

test.isna().sum().sum()

"""# EDA"""

# Label Count
train["Label"].value_counts()

count_num = [x for x in train['Label'].value_counts().sort_index()]
count_num

plt.figure(figsize=(8,5))
sns.barplot(count_num)
plt.title("Train Label Count")
plt.show()

fig, ax = plt.subplots(figsize=(18,8))
for ind, row in train.iloc[:8, :].iterrows():
  plt.subplot(2,4,ind+1)
  plt.title(row[0])
  img = row.to_numpy()[1:].reshape(28,28)
  fig.suptitle('Train Images')
  plt.axis('off')
  plt.imshow(img,cmap='magma')

fig, ax = plt.subplots(figsize=(18,8))
for ind, row in test.iloc[:8, :].iterrows():
  plt.subplot(2,4,ind+1)
  plt.title(row[0])
  img = row.to_numpy()[1:].reshape(28,28)
  fig.suptitle('Test Images')
  plt.axis('off')
  plt.imshow(img,cmap='magma')

"""# Pre-processing"""

X = train.iloc[:, 1:].to_numpy()
y = train["Label"].to_numpy()

# test
X_test = test.iloc[:, 1:].to_numpy()
y_test = test["Label"].to_numpy()

for i in [X,y,X_test,y_test]:
  print(i.shape)

# Normalization
X = X/255.0
X_test = X_test/255.0

"""# ML Model"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

logreg = LogisticRegression()

logreg.fit(X,y)

y_pred_logreg = logreg.predict(X_test)

accuracy = accuracy_score(y_test,y_pred_logreg)
print("Accuracy: ", accuracy)

from sklearn.svm import SVC

svc = SVC()

svc.fit(X,y)

y_pred = svc.predict(X_test)

print("Accuracy: ", accuracy_score(y_pred,y_test))

# Random forest, KNN

"""# CNN"""

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

# One - hot encoding
print(y.shape)
print(y[0])

y_enc = to_categorical(y, num_classes=10)

print(y_enc.shape)
print(y_enc[0])

print(X.shape)
print(X_test.shape)

X = X.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

print(X.shape)
print(X_test.shape)

random_seed = 101
X_train, X_val, y_train_enc, y_val_enc = train_test_split(X,y_enc,test_size=0.3)

for i in [X_train, X_val, y_train_enc, y_val_enc ]:
  print(i.shape)

# Plot image
g = plt.imshow(X_train[0][:,:,0])
print(y_train_enc[0])

"""# Model Paarameters"""

INPUT_SHAPE = (28,28,1)
OUTPUT_SHAPE = 10
BATCH_SIZE = 128
EPOCHS = 10
VERBOSE = 1

# CNN Model

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3), activation='relu', input_shape=INPUT_SHAPE))
model.add(MaxPool2D((2,2)))

model.add(Conv2D(64,kernel_size=(3,3), activation='relu'))
model.add(MaxPool2D((2,2)))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(64,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(10,activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

history = model.fit(X_train,y_train_enc,
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    verbose=VERBOSE,
                    validation_split=0.3)

# Accuracy and loss
plt.figure(figsize=(14,5))
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'],label="Training Accuracy")
plt.plot(history.history['val_accuracy'],label="Validation Accuracy")
plt.legend(loc='lower right')
plt.title("Training and Validation Accuracy")

plt.subplot(1,2,2)
plt.plot(history.history['loss'],label="Training Loss")
plt.plot(history.history["val_loss"],label="Validation Loss")
plt.legend(loc="upper right")
plt.title("Training and Validation Loss")

plt.savefig("./loss.png")
plt.show()

# Evaluation on val data
model.evaluate(X_val,y_val_enc,verbose=1)

# predicted
y_pred_enc = model.predict(X_val)

# actual
y_act = [np.argmax(i) for i in y_val_enc]

# decoding predicted values
y_pred = [np.argmax(i) for i in y_pred_enc]

print(y_pred_enc[0])
print(y_pred[0])

print(classification_report(y_act,y_pred))

fig, ax = plt.subplots(figsize=(7,7))
sns.heatmap(confusion_matrix(y_act,y_pred), annot=True, cbar=False, fmt='1d', cmap='Blues', ax=ax)
ax.set_title("Confusion Matrix", loc='left')
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
plt.show()

# Predicting on test
y_pred_enc = model.predict(X_test)

y_pred = [np.argmax(i) for i in y_pred_enc]

print(y_pred_enc[0])
print(y_pred[0])

fig, ax = plt.subplots(figsize=(18,12))
for ind,row in enumerate(X_test[:15]):
  plt.subplot(3,5,ind+1)
  plt.title(y_pred[ind])
  img = row.reshape(28,28)
  fig.suptitle("Predicted Values")
  plt.axis('off')
  plt.imshow(img,cmap='viridis')

fig, ax = plt.subplots(figsize=(7,7))
sns.heatmap(confusion_matrix(y_test,y_pred), annot=True, cbar=False, fmt='1d', cmap='Blues', ax=ax)
ax.set_title("Confusion Matrix", loc='left')
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
plt.show()

print(classification_report(y_test,y_pred))

"""# Accuracy of 98%"""