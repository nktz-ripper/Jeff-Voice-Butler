import tasklist_updater
import schedule
from constants import *
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import requests
import random
import pandas as pd
from pathlib import Path


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)
engine.setProperty('volume', 2)


butler ='jeff'

standby_countdown = 0
command=''
alarm_states = {}

def talk(text):
    engine.say(text)
    engine.runAndWait()

def standby(counter):
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Optional: Adjust for ambient noise
            voice = listener.listen(source, timeout=5)  # Set a timeout of 5 seconds
            command = listener.recognize_google(voice)
            command = command.lower()
            if butler in command:
                standby_reset(counter)
                talk('how can i help?')
                
    except:
        pass



def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)  # Optional: Adjust for ambient noise
            voice = listener.listen(source, timeout=30)  # Set a timeout of 30 seconds
            command = listener.recognize_google(voice)
            command = command.lower()
            if butler in command:
                command = command.replace(butler, '')
                print(command)
                return command
    except:
        #talk('balls')
        pass





def create_dataframe_from_csv(csv_file):
    df = pd.read_csv(csv_file, delimiter=';', skipinitialspace=True)
    df = df.dropna()  # Remove rows with missing values
    df = df.set_index('key')
    df = df['value'].apply(lambda x: x.strip())  # Remove leading/trailing spaces from values
    return df.to_dict()

def get_usd_brl_cotation():
    try:
        # Send a GET request to the API endpoint
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        if response.status_code == 200:
            data = response.json()
            brl_rate = data["rates"]["BRL"]
            return brl_rate
        else:
            print("Failed to retrieve USD/BRL cotation.")
    except requests.RequestException as e:
        print("Error occurred: {0}".format(e))

def get_btc_usd_cotation():
    try:
        # Send a GET request to the API endpoint
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        if response.status_code == 200:
            data = response.json()
            btc_rate = data["bitcoin"]["usd"]
            return btc_rate
        else:
            print("Failed to retrieve BTC/USD cotation.")
    except requests.RequestException as e:
        print("Error occurred: {0}".format(e))

def speak_cotation(cotation, currency):
    engine = pyttsx3.init()
    if currency == "USD/BRL":
        engine.say(f"The current dollar exchange rate is {cotation:.2f} for brazilian real")
    elif currency == "BTC/USD":
        engine.say(f"The current bitcoin exchange rate is {cotation:.2f} for u.s. dollar")
    engine.runAndWait()

def get_and_speak_cotation(currency):
    if currency == "USD/BRL":
        cotation = get_usd_brl_cotation()
    elif currency == "BTC/USD":
        cotation = get_btc_usd_cotation()
    else:
        print("Invalid currency.")
        return
    if cotation is not None:
        speak_cotation(cotation, currency)
    else:
        print(f"Failed to retrieve the {currency} cotation.")


def functions(command):
    try:
        response = None  # Initialize the response variable
        if 'play' in command:
            song = command.replace('play', '')
            response = 'playing ' + song
            pywhatkit.playonyt(song)
        elif 'what time' in command:
            hour = datetime.datetime.now().strftime('%I:%M %p')
            response = 'Current time is ' + hour
        elif 'what do you know about' in command:
            person = command.replace('what do you know about', '')
            info = wikipedia.summary(person, 1)
            if info != '':
                response = info
            else:
                response = f'I know nothing about {person}'
        elif 'joke' in command:
            response = pyjokes.get_joke()
        elif 'good morning' in command:
            day = datetime.datetime.now().strftime("%A %d of %B and its %I:%M %p")
            response = 'Good morning sir, today is ' + day
            get_and_speak_cotation("USD/BRL")
        elif 'what day' in command:
            day = datetime.datetime.now().strftime("%A, %d of %B")
            response = 'Today is ' + day
        elif 'dollar' in command:
            get_and_speak_cotation("USD/BRL")
        elif 'bitcoin' in command:
            get_and_speak_cotation("BTC/USD")
        elif 'tell me' in command:
            operation = command.split('me ')
            key = operation[1]
            if key != '':
                value = df_importantdata.get(key, None)
                if value is not None:
                    response = f'Sure! {key} is {value}'
                else:
                    response = f'Could not find the {key} data point'
            else: 
                response = 'Say that again, please'
        elif 'take a note' in command:
            operation = command.split('take a note ')
            text = str(operation[1])
            if text != '':
                try:
                    tasklist_updater.post_notes(text)
                    response = 'It is noted in Google Tasks'
                except:
                    response = 'Service inaccessible'
            else:
                response = 'Empty annotation, operation cancelled'
        elif 'is going to' in command:
            operation = command.split(' is going to ')
            if operation[1] is not None:
                response = f'Have a good time at {operation[1]}, {operation[0]}!'
        elif 'are going to' in command:
            operation = command.split(' are going to ')
            if operation[1] is not None:
                response = f'Please be safe at {operation[1]}, {operation[0]}!'
        elif 'is back' in command:
            response = f'Welcome back sir!'
        elif '+' in command:
            operation = command.split(' + ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber + secondnumber
            response = f'{firstnumber} plus {secondnumber} is equal to {result}'
        elif '-' in command:
            operation = command.split(' - ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber - secondnumber
            response = f'{firstnumber} minus {secondnumber} is equal to {result}'
        elif '*' in command:
            operation = command.split(' * ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber * secondnumber
            response = f'{firstnumber} times {secondnumber} is equal to {result}'
        elif '/' in command:
            operation = command.split(' / ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber / secondnumber
            response = f'{firstnumber} divided by {secondnumber} is equal to {result}'
        elif 'good night' in command:
            response = 'Good night! I will wake you up seven hours from now'
            time.sleep(25200)
            response += '\nGood morning! Time to wake up'
        elif 'motivation' in command:
            response = random.choice(list(motivation_quotes.values()))
        elif 'that right' in command:
            response = random.choice(list(thatsright.values()))
        return response  # Return the response from each function
    except Exception as e:
        print(e)
        return None  # Return None if an error occurs

def nap(command):
    if 'nap for' in command:
        getminutes = command.split('for ')
        getgetminutes = getminutes[1].split(' ')
        minutes = int(getgetminutes[0])
        talk(f'nighty nighty, i will wake you {minutes} minutes from now')
        time.sleep(60*minutes)
        talk('Hey, nap is over, time to wake up. wake up. wake up. wake up. wake up')
    else:
        pass


def chitchat(command):
    # Simple Conversation Script
    for key in chit_chat:
        if key in command:
            value = chit_chat[key]
            return str(value)

    return None  # Return None if no partial match is found

def check_alarm():
    now = datetime.datetime.now()
    weekday = now.strftime("%A")
    hour_24 = now.strftime("%H:%M")
    hour_ampm = now.strftime('%I:%M %p')
    now = now.strftime("%d/%m/%Y %H:%M %A")
    #print(now)

    if 'Saturday' or 'Sunday' in weekday:
        if ':00' in str(hour_24):
            calculate_hours = str(hour_24).split(':')
            calculate_hours = int(calculate_hours[0])
            if 6 <= calculate_hours <= 23 and not alarm_states.get(now, False):
                print(f'now, {hour_ampm}')
                alarm_states[now] = True
                talk(f'hey, it is, {hour_ampm}')
            else:
                pass
        else:
            pass
    else:
        if ':00' in str(hour_24):
            calculate_hours = str(hour_24).split(':')
            calculate_hours = int(calculate_hours[0])
            if 6 <= calculate_hours <= 8 and not alarm_states.get(now, False):
                alarm_states[now] = True
                talk(f'hey, it is, {hour_ampm}')
            elif 18 <= calculate_hours <= 23 and not alarm_states.get(now, False):
                alarm_states[now] = True
                talk(f'hey, it is, {hour_ampm}')
            else:
                pass
        else:
            pass
    for key in alarms:
        if key in now and not alarm_states.get(key, False):
            print(f'Alarm: {alarms[key]}')
            alarm_states[key] = True  # Set alarm state to True
            talk(f'Alarm triggered: {alarms[key]}')


def standby_add(counter):
    counter = counter + 1

def standby_reset(counter):
    counter = counter
    counter = 0



df_importantdata = create_dataframe_from_csv("scripts/important data.csv")
motivation_quotes = create_dataframe_from_csv("scripts/motivation quotes.csv")
thatsright = create_dataframe_from_csv("scripts/thats right.csv")
alarms = create_dataframe_from_csv("scripts/alarms.csv")
chit_chat = create_dataframe_from_csv("scripts/scripts.csv")

talk(f'hello, i am {butler}, your butler')
while True:
    check_alarm()
    command = take_command()
    if command is not None:
        nap(command)
        response = str(functions(command))
        if response != 'None':
            talk(response)
            pass
        else:
            response = str(chitchat(command))
            if response != 'None':
                talk(response)
            else:
                pass

    else:
        print('.')