import RPi.GPIO as GPIO
import MySQLdb as mdb
from TerraInit import host, user, password, database
GPIO.setwarnings(False)

def liczTerraria():
    try:
        dbConnection = mdb.connect(host, user, password, database)
        with dbConnection:
            dbCursor = dbConnection.cursor()
            dbCursor.execute("SELECT COUNT(*) FROM zwierzeta")
            ilosc_terrariow = dbCursor.fetchone()[0]
    except mdb.Error as e:
        print("Error %d: %s".format(e.args[0], e.args[1]))
    finally:
        if dbConnection:
            dbConnection.close()
    return ilosc_terrariow

def zapiszPomiar(i, temperatura, stanGrzalki):
    try:
        dbConnection = mdb.connect(host, user, password, database)
        with dbConnection:
            dbCursor = dbConnection.cursor()
            dbCursor.execute("INSERT INTO pomiary (id, pomiar, stan_grzalki) VALUES ({0}, {1}, {2})".format(i,
                                                                                                            temperatura,
                                                                                                            stanGrzalki))
    except mdb.Error as e:
        print("Error %d: %s".format(e.args[0], e.args[1]))
    finally:
        if dbConnection:
            dbConnection.close()
def czytajUstawieniaTemperatury(t):
    try:
        dbConnection = mdb.connect(host, user, password, database)
        with dbConnection:
            dbCursor = dbConnection.cursor()
            dbCursor.execute("SELECT temperatura, wahanie FROM zwierzeta WHERE id="+t)
            ustawieniaTemperatury = dbCursor.fetchone()
    except mdb.Error as e:
        print("Error %d: %s".format(e.args[0], e.args[1]))
    finally:
        if dbConnection:
            dbConnection.close()
    return ustawieniaTemperatury

# def czytajUstawieniaWilgotnosci(t):
#     try:
#         dbConnection = mdb.connect(host, user, password, database)
#         with dbConnection:
#             dbCursor = dbConnection.cursor()
#             dbCursor.execute("SELECT wilgotnosc, wahanie FROM zwierzeta WHERE id="+t)
#             ustawieniaWilgotnosci = dbCursor.fetchone()
#     except mdb.Error as e:
#         print("Error %d: %s".format(e.args[0], e.args[1]))
#     finally:
#         if dbConnection:
#             dbConnection.close()
#     return ustawieniaWilgotnosci

def zmianaStanuWiatraka(port, stanWiatraka):
    if stanWiatraka:
        GPIO.output(port, GPIO.HIGH)
    else:
        GPIO.output(port, GPIO.LOW)


def zmianaStanuGrzalki(port, stanGrzalki):
    if stanGrzalki:
        GPIO.output(port, GPIO.HIGH)
    else:
        GPIO.output(port, GPIO.LOW)


# def zmianaStanuZraszacza(port, stanZraszacza):
#     if stanZraszacza:
#         GPIO.output(port, GPIO.HIGH) # Zmieniamy na False
#     else:
#         GPIO.output(port, GPIO.LOW) # Zmieniamy na True

def regulacjaTemperatury(t, temperatura, portGrzalki, portWiatraka):
    stanGrzalki = GPIO.output(portGrzalki, not GPIO.input(portGrzalki))  # sprawdza obecny stan grzałki
    stanWiatraka = GPIO.output(portWiatraka, not GPIO.input(portWiatraka))
    zadanaTemperatura, wahanieTemperatury = czytajUstawieniaTemperatury(t)
    if zadanaTemperatura + wahanieTemperatury > temperatura > zadanaTemperatura - wahanieTemperatury:
        print("Temperatura ok.")
    else:
        if temperatura < zadanaTemperatura - wahanieTemperatury:
            if stanGrzalki:
                print("Ciągle podgrzewam, daj mi trochę czasu")
            else:
                zmianaStanuGrzalki(portGrzalki)
                print("Podgrzewam atmosferę")
        else:
            if temperatura >= zadanaTemperatura + wahanieTemperatury + 3:
                if stanGrzalki:
                    if stanWiatraka is False:
                        zmianaStanuGrzalki(portGrzalki, stanGrzalki)
                        zmianaStanuWiatraka(portWiatraka)
                        print("Grzałka off, włączam chłodzenie")
                    else:
                        zmianaStanuGrzalki(portGrzalki, stanGrzalki)
                        print("Wyłączam grzanie, zostawiam chłodzenie")
                else:
                    if stanWiatraka is False:
                        zmianaStanuWiatraka(portWiatraka, stanWiatraka)
                        print("Włączam chłodzenie")
                    else:
                        print("Ciągle chłodzę, daj mi trochę czasu")
            else:
                print("Uwaga, temperatura rośnie!")
    return stanGrzalki

# def regulacjaWilgotnosci(t, wilgotnosc, portZraszacza, portWiatraka):
#     stanZraszacza = GPIO.output(portZraszacza, not GPIO.input(portZraszacza))
#     stanWiatraka = GPIO.output(portWiatraka, not GPIO.input(portWiatraka))
#     zadanaWilgotnosc, wahanieWilgotnosci = czytajUstawieniaWilgotnosci(t)
#     from time import sleep
#     if zadanaWilgotnosc + wahanieWilgotnosci > wilgotnosc > zadanaWilgotnosc - wahanieWilgotnosci:
#         print("Wilgotność ok.")
#     else:
#         if wilgotnosc < zadanaWilgotnosc - wahanieWilgotnosci:
#             if stanZraszacza:
#                 print("Nawadniam, nie przeszkadzaj mi.")
#             else:
#                 zmianaStanuZraszacza(portZraszacza)
#                 sleep(30)
#                 zmianaStanuZraszacza(portZraszacza)
#                 print("Włączam nawadnianie")
#         else:
#             if wilgotnosc >= zadanaWilgotnosc + wahanieWilgotnosci + 10:
#                 if stanZraszacza:
#                     if stanWiatraka is False:
#                         zmianaStanuWiatraka(portWiatraka, stanWiatraka)
#                         zmianaStanuZraszacza(portZraszacza, stanZraszacza)
#                         print("Wyłączam zraszanie, włączam wiatrak")
#                     else:
#                         zmianaStanuZraszacza(portZraszacza, stanZraszacza)
#                         print("Wyłączam nawadnianie")
#                 else:
#                     if stanWiatraka is False:
#                         zmianaStanuWiatraka(portWiatraka, stanWiatraka)
#                         print("Włączam wiatrak")
#                     else:
#                         print("Ciągle wietrzę, nie przeszkadzaj.")
#             else:
#                 print("Uwaga, wilgotność rośnie!")
