import RPi.GPIO as GPIO
import MySQLdb as mdb
import TerraFunc as TF
from w1thermsensor import W1ThermSensor
from TerraInit import pinyGrzalek, pinyCzujnikow, pinyWiatrakow, pinyZraszaczy

GPIO.setmode(GPIO.BCM)

ilosc_terrariow = TF.liczTerraria()

zakresNumerow = range(1, ilosc_terrariow+1)
portyGrzalek = dict(zip(zakresNumerow, pinyGrzalek))
portyCzujnikow = dict(zip(zakresNumerow, pinyCzujnikow))
portyWiatrakow = dict(zip(zakresNumerow, pinyWiatrakow))
portyZraszaczy = dict(zip(zakresNumerow, pinyZraszaczy))

odczytyCzujnikow = {} # Słownik z odczytami temperatury dla każdego terrarium
for sensor in W1ThermSensor.get_available_sensors():
    odczytyCzujnikow[sensor.id] = sensor.get_temperature()

for t in range(ilosc_terrariow):
    if portyCzujnikow.get(t) is None:  # Wyłuskanie portu ze słownika na podstawie numeru terrarium
        break  # jeśli terrarium nie ma czujnika to przerywa pętlę
    else:
        temperatura = odczytyCzujnikow.get(portyCzujnikow.get(t))  # odczytywanie temperatury z danego czujnika

        if portyWiatrakow.get(t) is None:
            break
        elif portyGrzalek.get(t) is None:
            if portyZraszaczy.get(t) is None:
                break
            else:  # nie mamy grzałki, ale mamy wiatrak i zraszacz - regulujemy wilgotność
                GPIO.setup(portyZraszaczy.get(t), GPIO.OUT)
                GPIO.setup(portyWiatrakow.get(t), GPIO.OUT)
                # TF.regulacjaWilgotnosci(t, wilgotnosc, portyZraszaczy.get(t), portyWiatrakow.get(t))
        elif portyZraszaczy.get(t) is None:
            if portyGrzalek.get(t) is None:
                break
            else:  # nie mamy zraszacza, ale mamy grzałkę i wiatrak - regulujemy temperaturę
                GPIO.setup(portyGrzalek.get(t), GPIO.OUT)
                GPIO.setup(portyWiatrakow.get(t), GPIO.OUT)
                stanGrzalki = TF.regulacjaTemperatury(t, temperatura, portyGrzalek.get(t), portyWiatrakow.get(t))
                TF.zapiszPomiar(t, temperatura, stanGrzalki)
        else:  # mamy cały sprzęt, regulujemy wilgotność i temperaturę
            GPIO.setup(portyZraszaczy.get(t), GPIO.OUT)
            GPIO.setup(portyWiatrakow.get(t), GPIO.OUT)
            GPIO.setup(portyGrzalek.get(t), GPIO.OUT)
            stanGrzalki = TF.regulacjaTemperatury(t, temperatura, portyGrzalek.get(t), portyWiatrakow.get(t))
            TF.zapiszPomiar(t, temperatura, stanGrzalki)
            # TF.regulacjaWilgotnosci(t, wilgotnosc, portyZraszaczy.get(t), portyWiatrakow.get(t))
