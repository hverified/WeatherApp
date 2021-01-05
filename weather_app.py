from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import requests

url = 'http://'+'api.openweathermap.org/data/2.5/weather?q={}&appid={}'

configFile = 'config.ini'
config = ConfigParser()
config.read(configFile)
api_key = config['api_key']['key']


def getWeather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()

        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin-273.15
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        finalData = (city, country, temp_celsius, icon, weather)
        return finalData
    else:
        return None


def search():
    city = cityText.get()
    weather = getWeather(city)
    if weather:
        imgPIL = Image.open("weather_icons/{}.png".format(weather[3]))
        imgTk = ImageTk.PhotoImage(imgPIL)
        time.sleep(2)
        locationLbl['text'] = '{}, {}'.format(weather[0], weather[1])
        image['image'] = imgTk
        tempLbl['text'] = '{:.2f}°C'.format(weather[2])
        weatherLbl['text'] = weather[4]
    else:
        messagebox.showerror(
            'Error', 'Cannot find city {}'.format(city))


app = Tk()
app.title("Weather App")
app.geometry('700x350')

cityText = StringVar()
cityEntry = Entry(app, textvariable=cityText)
cityEntry.pack()

searchBtn = Button(app, text='Search Weather', width=12, command=search)
searchBtn.pack()

locationLbl = Label(app, text='', font=('bold', 20))
locationLbl.pack()

image = Label(app, text='')
image.pack()

tempLbl = Label(app, text='')
tempLbl.pack()

weatherLbl = Label(app, text='')
weatherLbl.pack()


app.mainloop()
