# Import necessary libraries
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from datetime import datetime, time, timedelta
import pandas as pd
import csv as csv
import pickle
import os
import sys



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    

# Use the CSV path
csv_path = os.path.join(os.path.abspath("."), "data/schedule.csv")
sched = pd.DataFrame(columns=["message", "priority", "schedule", "datecreated"])
if os.path.exists(csv_path):
    sched = pd.read_csv(csv_path)
    print("Loaded existing schedule.csv")
else:
    sched.to_csv(csv_path, index=False)
    print("schedule.csv not found. Created an empty CSV.")


# Load the saved model
model = load_model(os.path.join(os.path.abspath("."), 'AIModel.keras'))  # Replace with your model file path

# Load the saved tokenizer
with open(os.path.join(os.path.abspath("."), 'Tokenizer.pickle'), 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the saved label encoder
with open(os.path.join(os.path.abspath("."), 'LabelEncoder.pickle'), 'rb') as handle:
    label_encoder = pickle.load(handle)



# Function to predict the priority of a message
def predict_priority(message):
    # Step 1: Tokenize and pad the new message
    new_sequence = tokenizer.texts_to_sequences([message])
    new_padded_sequence = pad_sequences(new_sequence, maxlen=50)  # Adjust maxlen based on training

    # Step 2: Predict the class for the new message
    prediction = model.predict(new_padded_sequence)

    # Step 3: Decode the prediction (inverse transform to get the class label)
    predicted_class = label_encoder.inverse_transform(prediction.argmax(axis=1))

    return predicted_class[0]

def check_valid_date(current_date):
    if current_date.weekday() == 5:  # Saturday
        return current_date + timedelta(days=2)
    elif current_date.weekday() == 6:  # Sunday
        return current_date + timedelta(days=1)
    return current_date

def check_valid_time(current_time):
    hour = current_time.hour
    if hour < 10:
        return current_time.replace(hour=10, minute=0)
    elif 10 <= hour < 12:
        return current_time
    else:
        # Move to next weekday at 10 AM
        next_day = current_time + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return next_day.replace(hour=10, minute=0)

def appendsched(message, priority):
    now = datetime.now()
    valid_date = check_valid_date(now)
    valid_time = check_valid_time(valid_date)

    # Corrected date format for `now` and `valid_time`
    formatted_valid_time = valid_time.strftime("%B-%d-%Y %I:%M %p")  # ex. "April-14-2025 10:00 AM"
    formatted_now = (now.strftime("%m-%d-%Y") + ":" + now.strftime("%H-%M-%S")) # ex. "04-12-2025"

    with open(csv_path, 'a+', newline="") as newobj:
        writer = csv.writer(newobj)
        writer.writerow([message, priority, formatted_valid_time, formatted_now])


def reqsched():
    # Predict and print the result
    while True:
        
        user_message = input("Enter a message (Type Exit to Close Program, Type Other to return to menu.): ")
        if(user_message.lower() == 'other'):
            return
        else:
            predicted_priority = predict_priority(user_message)
            print(f"Message: {user_message}\nPredicted Priority: {predicted_priority}\n")
            appendsched(user_message, predicted_priority)
        
            
    
    

def checksched():
    sched = pd.read_csv(csv_path)
    if sched.empty:
        print("No Schedules Loaded.")
        return
    
    else:
        for index, row in sched.iterrows():
            print("Print Schedule Keywords.")
            print("\tMessage: " , row['message'])
            print("\tPriority: " , row['priority'])
            print("\tSchedule: " , row['schedule'])
            print("\tDate Created: " , row['datecreated'])
            if len(sched) - 1:
                print("=============")
        user_message = input("Press any key to exit.")
        return

# Main loop to accept custom messages from the user
while True:
    print("Entering Menu: ")
    print("==================")
    print("1. Request a Schedule.")
    print("2. Check Current Schedules.")
    user_message = input("")
    if int(user_message) == 1:
        reqsched()
    elif int(user_message) == 2:
        checksched()
    # Exit the loop if the user types 'exit'
    elif user_message.lower() == 'exit':
        print("Exiting the program.")
        break
    elif user_message.lower() == 'other':
        print("Entering ")
    


    
    
