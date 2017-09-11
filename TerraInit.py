pinyGrzalek = [2]
pinyCzujnikow = [27]
pinyWiatrakow = [3]
pinyZraszaczy = [4]

def main():
	import RPi.GPIO as GPIO
	from TerraCore import Terrarium
	import pickle
	plik = open('Terraria.txt', 'wb')
	ile_terrariow = int(input("Eloszki, ile chcesz dodac terrariow?\n"))
	pickle.dump(ile_terrariow, plik)
	for i in range(ile_terrariow):
	    terrarium = Terrarium()
	    terrarium.ustawNumer_Terrarium()
	    terrarium.ustawNazwe()
	    terrarium.ustawTemperatura()
	    terrarium.ustawWilgotnosc()
	    terrarium.wypisz_dane()
	    terrarium.wypisz_temp()
	    terrarium.wypisz_wilg()
	    pickle.dump(terrarium, plik)
	plik.close()
	
	GPIO.setwarnings(False)
	
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(pinyGrzalek, GPIO.OUT) 
	GPIO.output(pinyGrzalek, GPIO.HIGH)
	
	GPIO.setup(pinyWiatrakow, GPIO.OUT) 
	GPIO.output(pinyWiatrakow, GPIO.HIGH)
	
	GPIO.setup(pinyZraszaczy, GPIO.OUT) 
	GPIO.output(pinyZraszaczy, GPIO.HIGH)
if __name__=='__main__':
	main()	

