import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import requests
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)
engine.setProperty('volume', 2)




butler ='jeff'

def talk(text):
    engine.say(text)
    engine.runAndWait()



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

command=''


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



        
motivation_quotes = [
    'stand up straight with your shoulders back',
    'fear the bitterness that you would be',
    'ask yourself: what should you be doing right now',
    'picture your life a couple of years from now. Then picture the steps you must take to get there. You will get there',
    'get good scrub',
    'clean your room before you go change the world',
    'have you been exercicing regularly?',
    'just get to it',
    'you have a mission, and that is to show them who is the boss',
    'you are a force to be reckoned with',
    'do it for the kids man. your kids',
    'you put yourself in your position, no matter how bad. it is your responsability to go to a better one. just think a little more through before tough',
    'if you are high in neuroticism you can incorporate the shadow by recognizing the negative emotion and redirecting it to: one, fear the failure scenario. two, strive for the success scenario',
    'take a deep breath and get to phase 10',
    'remember that too much extraversion makes you stupid, so capitalize on your misery',
    'if you are feeling creative, write',
    'in the back of your mind there is a post-it written: get back to Maringá and conquer that dragon',
    'its on you man, only you can do it',
    'you never know when a close friend or family member will need the best version of you',
    'you are now building a raft out of someday island',
    'tomorrow always comes, and you dont wanna find out that years gone by with you living the same day, over and over again'

]



def run_alexa():
    try: 
        command = take_command()
        print(command)
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'what time' in command:
            hour = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + hour)
        elif 'what do you know about' in command:
            person = command.replace('what do you know about', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'hello' in command:
            talk('hello sir')
        elif 'hi' in command:
            talk('how can i help you sir?')
        elif 'hey' in command:
            talk('hey man')
        elif 'what can you do' in command:
            talk('i can play music and tell you what time is it. But... You know... Balls')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'good morning' in command:
            day = datetime.datetime.now().strftime("%A %d of %B and its %I:%M %p")
            talk('good morning sir, today is is ' + day)
            get_and_speak_cotation("USD/BRL")
        elif 'what day' in command:
            day = datetime.datetime.now().strftime("%A, %d of %B")
            talk('today is is ' + day)
        elif 'thank you' in command:
            talk('thank you sir')
        elif 'thanks' in command:
            talk('glad to help')
        elif 'stand by' in command:
            talk('say my name and i will wake')
            standby()
            if butler in command:
                pass
        elif 'have you seen my' in command:
            talk('in my pants!')
        elif 'funny' in command:
            talk('balls')
        elif 'have you ever been to' in command:
            talk('oh, yes. I love it there!')
        elif 'what part of' and 'have you been' in command:
            talk('the south-eastern part, with the shops, and the lamps, and the cars...')
        elif 'dollar' in command:
            get_and_speak_cotation("USD/BRL")
        elif 'bitcoin' in command:
            get_and_speak_cotation("BTC/USD")
        elif '+' in command:
            operation = command.split(' + ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber + secondnumber
            talk(f'{firstnumber} plus {secondnumber} is equal to {result}')
        elif '-' in command:
            operation = command.split(' - ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber - secondnumber
            talk(f'{firstnumber} minus {secondnumber} is equal to {result}')
        elif '*' in command:
            operation = command.split(' * ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber * secondnumber
            talk(f'{firstnumber} times {secondnumber} is equal to {result}')
        elif '/' in command:
            operation = command.split(' / ')
            firstnumber = int(operation[0])
            secondnumber = int(operation[1])
            result = firstnumber / secondnumber
            talk(f'{firstnumber} divided by {secondnumber} is equal to {result}')
        elif 'good night' in command:
            talk('good night man, i will wake you seven hours from now')
            time.sleep(25200)
            talk('good morning, time to wake up')
        elif 'nap for' in command:
            getminutes = command.split('for ')
            getgetminutes = getminutes[1].split(' ')
            minutes = int(getgetminutes[0])
            talk(f'nighty nighty, i will wake you {minutes} minutes from now')
            time.sleep(60*minutes)
            talk('Hey, nap is over, time to wake up. wake up. wake up. wake up. wake up')
        elif 'motivation' in command:
            talk(random.choice(motivation_quotes))

    except:
        #talk('Come again for jeff.')
        pass


def standby():
    time.sleep(30)
    with sr.Microphone() as source:
        print('Jeff in on Stand-By')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        print(command)
        return command


talk(f'hello, i am {butler}, your butler')
while True:
    try:
        run_alexa()
    except:
        #talk('balls')
        standby()
        if 'jeff' in command:
            talk('hi, this is jeff')
            run_alexa() 
        
