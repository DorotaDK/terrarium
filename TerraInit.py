pinyGrzalek = [2]
pinyCzujnikow = [27] #id czujników
pinyWiatrakow = [3]
pinyZraszaczy = []
host = 'localhost'
user = 'Guest'
password = 'password'
database = 'terraria'


def main():
    import MySQLdb as mdb
    import RPi.GPIO as GPIO
    ile_terrariow = int(input("Witaj, ile chcesz dodac terrariow?\n"))
    try:
        dbConnection = mdb.connect(host, user, password, database)
        with dbConnection:
            for i in range(ile_terrariow):
                imie = input("Podaj imię pupila: ")
                temperatura = input("Ustaw Temperature: ")
                wahanie = input("Ustaw maksymalne odchylenie: ")

                dbCursor = dbConnection.cursor()
                dbCursor.execute(
                    "INSERT INTO zwierzeta (imie, temperatura, wahanie) VALUES ({0}, {1}, {2})".format(imie,
                                                                                                       temperatura,
                                                                                                       wahanie))
    except mdb.Error as e:
        print("Error %d: %s".format(e.args[0], e.args[1]))
    finally:
        if dbConnection:
            dbConnection.close()

    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)


if __name__ == '__main__':
    main()
