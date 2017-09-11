import RPi.GPIO as GPIO
import Adafruit_DHT
import pickle
from TerraInit import pinyGrzalek, pinyCzujnikow, pinyWiatrakow, pinyZraszaczy
from TerraCore import Terrarium
GPIO.setmode(GPIO.BCM)

czytaj = open('Terraria.txt', 'rb')
ilosc_terrariow = pickle.load(czytaj)
listaTerrariow = []
for n in range(ilosc_terrariow):
    listaTerrariow.append(n)

portyGrzalek = dict(zip(listaTerrariow, pinyGrzalek))
portyCzujnikow = dict(zip(listaTerrariow, pinyCzujnikow))
portyWiatrakow = dict(zip(listaTerrariow, pinyWiatrakow))
portyZraszaczy = dict(zip(listaTerrariow, pinyZraszaczy))

for i in listaTerrariow:
    if portyCzujnikow.get(i) == None:
        break
    else:
        wilg, temp = Adafruit_DHT.read_retry(11, portyCzujnikow.get(i))
        terrarium = pickle.load(czytaj)
        terrarium.odczytWilgotnosci(zwilg)
        terrarium.odczytTemperatury(ztemp)
        print(wilg, temp)
        if portyWiatrakow.get(i) == None:
            break
        elif portyGrzalek.get(i) == None:
            if portyZraszaczy.get(i) == None:
                break
            else:
                terrarium.regulacjaWilgotnosci(portyZraszaczy.get(i), portyWiatrakow.get(i))
        elif portyZraszaczy.get(i) == None:
            if portyGrzalek.get(i) == None:
                break
            else:
                terrarium.regulacjaTemperatury(portyGrzalek.get(i), portyWiatrakow.get(i))
        else:
            terrarium.regulacjaTemperatury(portyGrzalek.get(i), portyWiatrakow.get(i))
            terrarium.regulacjaWilgotnosci(portyZraszaczy.get(i), portyWiatrakow.get(i))
