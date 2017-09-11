import RPi.GPIO as GPIO
GPIO.setwarnings(False)
class Terrarium:
    temp = 0
    wilg = 0

    def __init__(self, numer_terra=None, nazwa=None, zadanaTemperatura=None,zadanaWilgotnosc=None, wahanieTemperatury=None, wahanieWilgotnosci=None, stanWiatraka=False, stanGrzalki=False, stanZraszacza=False):
        self.numer_terra = numer_terra
        self.nazwa = nazwa
        self.zadanaTemperatura = zadanaTemperatura
        self.zadanaWilgotnosc = zadanaWilgotnosc
        self.wahanieTemperatury = wahanieTemperatury
        self.wahanieWilgotnosci = wahanieWilgotnosci
        self.stanWiatraka = stanWiatraka
        self.stanGrzalki = stanGrzalki
        self.stanZraszacza = stanZraszacza

    def wypisz_temp(self):
        print (self.zadanaTemperatura, self.wahanieTemperatury)
    def wypisz_wilg(self):
        print (self.zadanaWilgotnosc, self.wahanieWilgotnosci)
    def wypisz_dane(self):
        print (self.numer_terra, self.nazwa)
    def zmianaStanuWiatraka(self, port):
        if self.stanWiatraka == True:
            self.stanWiatraka = False
            GPIO.output(port, GPIO.HIGH)
        else:
            self.stanWiatraka = True
            GPIO.output(port, GPIO.LOW)
    def zmianaStanuGrzalki(self, port):
        if self.stanGrzalki == True:
            self.stanGrzalki = False
            GPIO.output(port, GPIO.HIGH)
        else:
            self.stanGrzalki = True
            GPIO.output(port, GPIO.LOW)
    def zmianaStanuZraszacza(self, port):
        if self.stanZraszacza == True:
            self.stanZraszacza = False
            GPIO.output(port, GPIO.HIGH)
        else:
            self.stanZraszacza = True
            GPIO.output(port, GPIO.LOW)
    def ustawNumer_Terrarium(self):
        self.numer_terra = int(input("Podaj nr. terrarium: "))
    def ustawNazwe(self):
        self.nazwa = input("Podaj nazwę terrarium: ")
    def ustawTemperatura(self):
        self.zadanaTemperatura = int(input("Ustaw Temperature: "))         
        self.wahanieTemperatury = int(input("Ustaw maksymalne odchylenie: "))
    def ustawWilgotnosc(self):
        self.zadanaWilgotnosc = int(input("Ustaw Wilgotnosc: "))
        self.wahanieWilgotnosci = int(input("Ustaw maksymalne odchylenie: "))
    def wypiszStanyWyjsc(self):
        print (self.stanZraszacza, self.stanGrzalki, self.stanWiatraka)
    def wypiszStanyWejsc(self):
        print (self.temp, self.wilg)
    def odczytWilgotnosci(self, wilg): 
        self.wilg = wilg
    def odczytTemperatury(self, temp):
        self.temp = temp
    def regulacjaTemperatury(self, portGrzalki, portWiatraka):
        GPIO.setup(portGrzalki, GPIO.OUT)
        GPIO.setup(portWiatraka, GPIO.OUT) 
        if self.temp < self.zadanaTemperatura + self.wahanieTemperatury and self.temp > self.zadanaTemperatura - self.wahanieTemperatury:
            print ("Temperatura ok.")
        else:
            if self.temp < self.zadanaTemperatura - self.wahanieTemperatury:
                if self.stanGrzalki == True:
                    print ("Ciągle podgrzewam, daj mi trochę czasu")
                else:
                    self.zmianaStanuGrzalki(portGrzalki)
                    print ("Podgrzewam atmosferę")
            else:
                if self.temp >= self.zadanaTemperatura + self.wahanieTemperatury + 3:
                    if self.stanGrzalki == True:
                        if self.stanWiatraka == False:
                            self.zmianaStanuGrzalki(portGrzalki)
                            self.zmianaStanuWiatraka(portWiatraka)
                            print ("Grzałka off, włączam chłodzenie")
                        else:
                            self.zmianaStanuGrzalki(portGrzalki)
                            print ("Wyłączam grzanie, zostawiam chłodzenie")
                    else:
                        if self.stanWiatraka == False:
                            self.zmianaStanuWiatraka(portWiatraka)
                            print ("Włączam chłodzenie")
                        else:
                            print ("Ciągle chłodzę, daj mi trochę czasu") 
                else:
                    print ("Uwaga, temperatura rośnie!")
    def regulacjaWilgotnosci(self, portZraszacza, portWiatraka):
        GPIO.setup(portZraszacza, GPIO.OUT)
        GPIO.setup(portWiatraka, GPIO.OUT) 
        from time import sleep
        if self.wilg < self.zadanaWilgotnosc + self.wahanieWilgotnosci and self.wilg > self.zadanaWilgotnosc - self.wahanieWilgotnosci:
            print ("Wilgotność ok.")
        else:
            if self.wilg < self.zadanaWilgotnosc - self.wahanieWilgotnosci:
                if self.stanZraszacza == True:
                    print ("Nawadniam, nie przeszkadzaj mi.")
                else:
                    self.zmianaStanuZraszacza(portZraszacza)
                    time.sleep(30)
                    self.zmianaStanuZraszacza(portZraszacza)
                    print ("Włączam nawadnianie")
            else:
                if self.wilg >= self.zadanaWilgotnosc + self.wahanieWilgotnosci + 10:
                    if self.stanZraszacza == True:
                        if self.stanWiatraka == False:
                            self.zmianaStanuWiatraka(portWiatraka)
                            self.zmianaStanuZraszacza(portZraszacza)
                            print ("Wyłączam zraszanie, włączam wiatrak")
                        else:
                            self.zmianaStanuZraszacza(portZraszacza)
                            print ("Wyłączam nawadnianie")
                    else:
                        if self.stanWiatraka == False:
                            self.zmianaStanuWiatraka(portWiatraka)
                            print ("Włączam wiatrak")
                        else:
                            print ("Ciągle wietrzę, nie przeszkadzaj.")
                else:
                    print ("Uwaga, wilgotność rośnie!") 
