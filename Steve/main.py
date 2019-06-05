import wolframalpha
import requests
import wikipedia
import spacy
from googlesearch import search
from datetime import datetime

wolframalphaclient = wolframalpha.Client('2JPLYG-XHH25L8W82')


def getweather(city):
    ipurl = 'https://ipinfo.io'
    ipinfo = requests.get(ipurl)
    ipdata = ipinfo.json()

    if city != '':
        city = city
    else:
        city = ipdata['city']

    authkey = '2a3b776ec8861e6fc9a3f05241694317'
    weatherurl = 'http://api.openweathermap.org/data/2.5/weather?appid=' + authkey + '&q=' + city
    weatherinfo = requests.get(weatherurl)
    weatherdata = weatherinfo.json()

    if weatherdata['cod'] != '404':
        main = weatherdata['main']
        wind = weatherdata['wind']
        visibilityinmetres = weatherdata['visibility']
        weather = weatherdata['weather'][0]

        tempinkelvin = main['temp']
        tempincelsius = tempinkelvin - 273.15
        pressureinhpa = main['pressure']
        pressureinatm = pressureinhpa / 1013.2501
        humidity = main['humidity']

        windspeedinmps = wind['speed']

        weatherdescription = weather['description']

        print('Today''s weather forecast in ', city, '', 'says...\n')
        print('Description: ', weatherdescription)
        print('Temperature (in Celsius): ', tempincelsius)
        print('Pressure (in atm): ', pressureinatm)
        print('Humidity: ', humidity)
        print('Wind Speed (in m/s): ', windspeedinmps)
        print('Visibility (in m): ', visibilityinmetres)
    else:
        print('Invalid City')


def removewiki(variable):
    if 'wiki' in variable or 'WIKI' in variable or 'Wiki' in variable:
        return variable[:-5]
    else:
        return variable


def search_wiki(keyword):
    searchresults = wikipedia.search(keyword)
    if not searchresults:
        print('No result from Wikipedia')
        return
    try:
        page = wikipedia.page(searchresults[0])
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])

    wikititle = str(page.title)
    wikisummary = wikipedia.summary(wikititle, sentences=2)
    wikiurl = (wikipedia.page(searchresults[0])).url
    print('Wikipedia says:\n', wikisummary)
    print('For more information please visit the link: ', wikiurl)


def google_search(question):
    searchresults = search(question, tld='co.in', num=10, stop=10, pause=2)
    print('This is what I found on Google.')
    for i in searchresults:
        print(i)


def find(question):
    if 'weather' in question:
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(question)
            city = ''
            for i in doc.ents:
                text = i.text
                label = i.label_
                if label == 'GPE':
                    city = text
                else:
                    city = ''
            getweather(city)

    elif 'wiki' in question or 'wikipedia' in question:
        question = removewiki(question)
        search_wiki(question)

    elif question.upper() == 'HOW ARE YOU':
        print('I am fine. Thank You for asking.')

    elif 'time' in question or 'TIME' in question:
        print(datetime.now().time())

    elif 'date' in question or 'DATE' in question:
        print(datetime.now().date())

    else:
        google_search(question)


while True:
    question = str(input('\nAsk me anything: '))

    if question.upper() == 'QUIT' or question.upper() == 'STOP':
        print('\nHope I was helpful. See you again. Adios!')
        quit()
    else:
        find(question)