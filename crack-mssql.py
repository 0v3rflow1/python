#!/usr/bin/env python
#Level7 haxtor https://hax.tor.hu/level7/
#b1a593a5e2a5f6a5c6a5b6a511a5f3a532a5
#by undefined
import os
def cifrar():
	cadena=raw_input('Ingresa la cadena a cifrar: ')
	encryptF="";
	for c in cadena:
		charx=int(hex(ord(c)),16)
		charx<<=8;
		bl=charx>>4;
		bb=charx>>4;
		sh='0x'+format((bl|bb),'4x').replace(' ','0');
		nh=int(sh,16)
		encrypt=nh^0xA5A5;
		n2=bin(encrypt).replace('0b','')
		sc=hex(int('0b'+n2[8:12]+n2[4:8]+n2[:4]+n2[12:16],2));
		encryptF+=sc.replace('0x','');
	print('encrypt: 0x'+encryptF)
	
def descifrar():
	encrypt=raw_input('Ingresa la cadena a descifrar en formato hexadecimal 0x')
	decryptF="";
	len_=len(encrypt)
	i=0
	codes=[]
	while(i<len_):
		codes.append(int('0x'+encrypt[i]+encrypt[i+1]+encrypt[i+2]+encrypt[i+3],16))
		i+=4
	i=0
	len_=len(codes)
	decryptF="";
	decryptFS="";
	while(i<len_):
		decrypt=0xA5A5^codes[i];
		print(codes[i])
		bl=decrypt>>4;
		bb=decrypt>>4;
		sh='0x'+format((bl|bb),'4x').replace(' ','0');
		decrypt=int(sh,16)
		sd=hex(decrypt).replace('0x','');
		sd=sd[1]+sd[0];
		decryptF+=sd
		decryptFS+=chr(int('0x'+sd,16));
		i+=1;
	print('decrypt: 0x'+decryptF)
	print('decrypt:'+decryptFS)
def salir():
	os.system('exit')

def menu():
	print('Selecciona una opcion: ')
	print('0)Cifrar\n1)Descifrar\n2)Salir');
	opc=raw_input('\n<opcion> ')
	e=True
	while(e==True):
		if(opc=='0'):
			e=False
			cifrar()
		elif(opc=='1'):
			e=False
			descifrar()
		elif(opc=='2'):
			e=False
			salir()
		else:
			os.system('reset')
			print('Selecciona una opcion: ')
			print('0)Cifrar\n1)Descifrar\n2)Salir');
			opc=raw_input('\n<opcion> ')
def main():
	menu();
	
if __name__=="__main__":
	main()
	

