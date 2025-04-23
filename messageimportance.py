import tensorflow as tensor
import pickle
import pandas as panda
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import os

CurrentDirectory = os.getcwd()


dataset = panda.read_csv(os.path.join(CurrentDirectory, "consultation_messages_batch.csv"))
dataset = dataset.drop_duplicates(subset=["Message"])
messages = dataset["Message"].tolist()
priorities = dataset["Priority"].tolist()


tokenizer = Tokenizer(num_words = 10000)
tokenizer.fit_on_texts(messages)
sequences = tokenizer.texts_to_sequences(messages)
maxlength = 100
X = pad_sequences(sequences, maxlen = maxlength)
label_encode = LabelEncoder()
y = label_encode.fit_transform(priorities)

#Training and Testing Sets (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()

# Embedding layer to convert words into dense vectors
model.add(Embedding(input_dim=10000, output_dim=128, input_length=maxlength))

# LSTM layer for sequential data (text)
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))

# Output layer (one neuron for each priority class)
model.add(Dense(4, activation='softmax'))  # 4 classes: 0, 1, 2, 3

# Step 8: Compile the model
model.compile(loss='sparse_categorical_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])

# Step 9: Train the model
history = model.fit(X_train, y_train, epochs=70, batch_size=16, validation_data=(X_test, y_test))

# Step 10: Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Accuracy: {accuracy:.4f}")

# Step 11: Plot accuracy and loss curves
plt.figure(figsize=(12, 4))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

model.save(os.path.join(CurrentDirectory,"AIModel1.keras"))
with open(os.path.join(CurrentDirectory,'Tokenizer1.pickle'), 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save label encoder
with open(os.path.join(CurrentDirectory,'LabelEncoder1.pickle'), 'wb') as handle:
    pickle.dump(label_encode, handle, protocol=pickle.HIGHEST_PROTOCOL)


#Eto itsura ng pag Train. Need ko to i automate once na maayos na program
