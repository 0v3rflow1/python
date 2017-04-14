#!/usr/bin/python
#-*-encoding:utf-8-*-
import sys
import os
import hashlib
import random
import emblemas_31337
from re import *
from datetime import datetime
from time import *
class RSA():
	def __init__(self):
		#(ne)=>PUBLICA
		#(nd)=>PRIVADA
		self.generaAlfabetos()
		self.Menu()
		self.p=0
		self.q=0
		self.n=0
		self.d=0
		self.e=0
		
	#PARA EL CIFRADO SE USA LA LLAVE PUBLICA (n,e) DEL RECEPTOR
	#ES DECIR LA LLAVE PUBLICA DE QUIEN VA A RECIBIR EL MSJ
	#USADO PARA CIFRADO DE FICHEROS EN GENERAL
	def public_key_cipher(self,plain_text):
		cipher_text=""					
		for c in plain_text:
			i=0
			while(i<16):
				j=0
				while(j<16):
					if(ord(c)==asciiA[i][j]):
						cipher_text+=str(pow(int(str(i)+str(j)),int(self.e),int(self.n)))+'\n'
						break
					j+=1
				i+=1
		cipher_text=cipher_text.encode('base-64')		
		return cipher_text
	#PARA EL CIFRADO SE USA LA LLAVE PRIVADA (n,d) DEL RECEPTOR
	#ES DECIR LA LLAVE PRIVADA DE QUIEN VA A RECIBIR EL MSJ
	#REGULARMENTE USADO PARA FIRMAR FICHEROS
	def private_key_cipher(self,plain_text):
		cipher_text=""					
		for c in plain_text:
			i=0
			while(i<16):
				j=0
				while(j<16):
					if(ord(c)==asciiA[i][j]):
						cipher_text+=str(pow(int(str(i)+str(j)),int(self.d),int(self.n)))+'\n'#TEOREMA DE FERMAT
						break
					j+=1
				i+=1
		cipher_text=cipher_text.encode('base-64')		
		return cipher_text
		
	#PARA DESCIFRAR CIFRADOS CON LLAVE PRIVADA	(n,d)
	#PARA EL DESCIFRADO SE USA LA LLAVE PUBLICA (n,e) DEL RECEPTOR
	#ES DECIR LA LLAVE PUBLICA DE QUIEN VA A RECIBIR EL MSJ
	#USADO REGULARMENTE PARA COMPROBAR FIRMAS DIGITALES
	def public_key_decipher(self,cipher_text):
		cipher_text=cipher_text.decode('base-64')
		plain_text=""
		z=0
		tmp=0
		tot=len(cipher_text.split('\n'))-1
		for c in cipher_text.split('\n'):
			if(z<tot):
				tmp=pow(int(c),int(self.e),int(self.n))
				i=0;k=0;
				while(i<16):
					j=0
					while(j<16):
						if(asciiB[i][j][0]==tmp):
							plain_text+=chr(asciiB[i][j][1])
						k+=1
						j+=1
					i+=1
				z+=1
		return plain_text
		
	#PARA DESCIFRAR CIFRADOS CON LLAVE PUBLICA	(n,e)
	#PARA EL DESCIFRADO SE USA LA LLAVE PRIVADA (n,d) DEL RECEPTOR
	#ES DECIR LA LLAVE PRIVADA DE QUIEN VA A RECIBIR EL MSJ
	#USADO REGULARMENTE PARA DESCIFRADO DE DOCS
	def private_key_decipher(self,cipher_text):
		cipher_text=cipher_text.decode('base-64')
		plain_text=""
		z=0
		tmp=0
		tot=len(cipher_text.split('\n'))-1
		for c in cipher_text.split('\n'):
			if(z<tot):
				tmp=pow(int(c),int(self.d),int(self.n))
				i=0;k=0;
				while(i<16):
					j=0
					while(j<16):
						if(asciiB[i][j][0]==tmp):
							plain_text+=chr(asciiB[i][j][1])
						k+=1
						j+=1
					i+=1
				z+=1
		return plain_text
	def check_signature(self):
		try:
			path_signed_file=raw_input("Archivo a verificar: ")
			signed_file=open(path_signed_file)
			if(signed_file!=None):
				Name=os.path.split(signed_file.name);
				temp=len(Name)-1;
				Name=Name[temp];
				print("Verificando fichero "+Name+"\n########################\n")
				content_signed_file=signed_file.read()
				signed_file.close()
				self.e=int((findall(r'<pke>(.*)</pke>',content_signed_file)[0]).decode('base-64'),16)
				self.n=int((findall(r'<pkn>(.*)</pkn>',content_signed_file)[0]).decode('base-64'),16)
				digital_signature=findall(r'<signed>(.*)</signed>',content_signed_file)[0]
				firmante=findall(r'<signer>(.*)</signer>',content_signed_file)[0]
				fecha=findall(r'<date>(.*)</date>',content_signed_file)[0]
				hora=findall(r'<time>(.*)</time>',content_signed_file)[0]
				recovered_SHA1=self.public_key_decipher(digital_signature)
				RecoverFile=open("recover_"+Name,"w")
				ContentRecoverFile=content_signed_file
				ContentRecoverFile=sub(r'<signed>.*</signed>',"",ContentRecoverFile)
				ContentRecoverFile=sub(r'<pkn>.*</pkn>',"",ContentRecoverFile)
				ContentRecoverFile=sub(r'<pke>.*</pke>',"",ContentRecoverFile)
				ContentRecoverFile=sub(r'<signer>.*</signer>',"",ContentRecoverFile)
				ContentRecoverFile=sub(r'<date>.*</date>',"",ContentRecoverFile)
				ContentRecoverFile=sub(r'<time>.*</time>',"",ContentRecoverFile)
				RecoverFile.write(ContentRecoverFile)
				RecoverFile.close()
				RecoverFile=open("recover_"+Name)
				ContentRecoverFile=RecoverFile.read()
				RecoverFile.close()
				SHA1FileRecover=hashlib.sha1(ContentRecoverFile).hexdigest()
				if(SHA1FileRecover==recovered_SHA1):
					print("\nLa firma es correcta:\n###########################\n")
					print("Hash recuperado:\n"+str(recovered_SHA1)+"\n\nHash del archivo original:\n"+str(SHA1FileRecover))
					print("\nArchivo "+Name+"\nfirmado por "+firmante+'\nel '+fecha+'\nA las '+hora+' hrs')
				else:
					print("\nLa firma no es correcta:\n###########################\n")
					print("Hash recuperado:\n"+str(recovered_SHA1)+"\n\nHash del archivo original:\n"+str(SHA1FileRecover))
				print("Enter para Continuar...")
				raw_input()
				self.Menu()
				
			else:
				print("El fichero no existe")
				print("Enter para continuar...")
				raw_input()
				self.check_signature()
		except:
			print("Error en la verificación")
			print("Enter para Continuar...")
			raw_input()
			self.Menu()
			
	def Menu(self):
		try:
			self.cls()
			i=0
			while(i<50):
				self.cls()
				print(emblemas_31337.emblemas())
				i+=1
			
			print("0) Generar Llaves")
			print("1) Firmar")
			print("2) Cifrar")
			print("3) Descifrar")
			print("4) Verificar firma")
			print("5) Salir")
			opc=input("\nElige una opción: ")
			if(opc==0):
				self.genKeysRSA()
			elif(opc==1):
				self.signFile()
			elif(opc==2):
				pass
			elif(opc==3):
				pass
			elif(opc==4):
				self.check_signature()
			elif(opc==5):
				self.exit()
			else:
				print("opción no valida")
				print("Enter para Continuar...")
				raw_input()
				self.Menu()
		except:#ValueError:
			#print(ValueError)
			self.Menu()
	
	def verifyKeys(self):
		try:
			PublicKey=open("public.key",'r')
			PrivateKey=open("private.key",'r')
			if(PublicKey!=None and PrivateKey!=None):
				dataPublic=PublicKey.read().decode('base-64')#(n,e)
				dataPublic=dataPublic.split('\n')
				dataPrivate=PrivateKey.read().decode('base-64')#(n,d)
				dataPrivate=dataPrivate.split('\n')
				if(len(dataPublic)==2 and len(dataPrivate)==2):
					try:
						self.n=int(dataPublic[0],16)
						self.e=int(dataPublic[1],16)
						n2=int(dataPrivate[0],16)
						self.d=int(dataPrivate[1],16)
						if(self.n==n2):
							print('Llaves leidas correctamente\n')
							return True
						else:
							self.n=0
							self.e=0
							self.d=0
							return False					
					except:
						return False
				else:
					return False
				return True
			else:
				print("No hay llaves disponibles\n######################\n")
				opc=raw_input("Gustas crear un nuevo par de llaves? (y/n):")
				if(opc=="y"):
					self.genKeys()
				elif(opc=="n"):
					self.Menu()
				else:
					self.Menu()
		except:
			print("No hay llaves disponibles\n######################\n")
			opc=raw_input("Gustas crear un nuevo par de llaves? (y/n):")
			if(opc=="y"):
				self.genKeysRSA()
			elif(opc=="n"):
				self.Menu()
			else:
				self.Menu()
	
	#La firma se realiza cifrando 
	#con la llave privada del emisor		
	def signFile(self):
		self.cls()
		print(emblemas_31337.emblemas())
		print("Firmando documento con algoritmo RSA\n####################################")
		if(self.verifyKeys()):
			PathFile=raw_input("Archivo a firmar: ")
			try:
				File=open(PathFile,'r')
				if(File!=None):
					Name=os.path.split(File.name);
					temp=len(Name)-1;
					Name=Name[temp];
					ContentFile=File.read()
					SHA1File_HEX=hashlib.sha1(ContentFile).hexdigest()
					SHA1File_INT=int(SHA1File_HEX,16)
					print("\nHash:sha1\t\t\t\t### File")
					print("#####################################################")
					print(str(SHA1File_HEX)+"### "+str(Name))
					print("#####################################################")
					File.close()
					firmante=raw_input("\nFirmar como: ")
					if(firmante==""):
						firmante="Anonymous"
					fecha=datetime.now()
					fecha=fecha.strftime("%d/%m/%Y")
					hora=strftime("%H:%M:%S")
					digital_signature=self.private_key_cipher(SHA1File_HEX)
					digital_signature0=digital_signature
					digital_signature="<signed>"+digital_signature.replace('\n','')+"</signed>"
					signed_file=open('signed_'+Name,"w")
					est_public_key='<pkn>'+hex(self.n).encode('base-64').replace('\n','')+'</pkn>'+'<pke>'+hex(self.e).encode('base-64').replace('\n','')+'</pke>'
					signed_file.write(ContentFile+digital_signature+est_public_key+"<signer>"+firmante+"</signer>"+"<date>"+fecha+"</date>"+"<time>"+hora+"</time>")
					print("\nSe firmo el documento "+Name+"\na nombre de "+firmante+'\ncon fecha '+fecha+' y hora '+hora)
					print("\n\nLa firma generada fue:\n#################################\n")
					print(digital_signature0)
					signed_file.close()
					print("El fichero se firmo correctamente")
					print("Enter para continuar...")
					raw_input()
					self.Menu()
				else:
					print("El fichero no existe")
					print("Enter para continuar...")
					raw_input()
					self.signFile()
			except: #ValueError:
				#print(ValueError)
				print("El fichero no existe")
				print("Enter para continuar...")
				raw_input()
				self.signFile()
		else:
			print('No hay llaves')
			
	def genKeysRSA(self):
		try:
			self.p=self.genPrime()
			self.q=self.genPrime()
			self.n=(self.p)*(self.q)
			p_1_q_1=(self.p-1)*(self.q-1)
			self.d=self.genPrimeRelative(p_1_q_1)
			y=1
			self.e=float(p_1_q_1*y+1)/float(self.d)
			while((type(self.e)!=int)or(self.e<1 and self.e>p_1_q_1)):
				y+=1
				if(y<10000):
					self.e=float(p_1_q_1*y+1)/float(self.d)
					r=self.e-int(self.e)
					if(r==0):
						self.e=int(self.e)
				else:
					break
					self.genKeysRSA()
			
			publicKey=(hex(self.n)+'\n'+hex(int(self.e))).encode('base-64')
			privateKey=(hex(self.n)+'\n'+hex(self.d)).encode('base-64')
			
			print("\nLlave publica generada:\n#########################\n"+publicKey)
			print("Llave privada generada\n#########################\n"+privateKey)
			PUBK=open('public.key',"w")
			PUBK.write(publicKey)
			PRIVK=open('private.key',"w")
			PRIVK.write(privateKey)
			PUBK.close()
			PRIVK.close()
			print("\n##############################\nLlaves generadas correctamente")
			print("Enter para Continuar...")
			raw_input()
			self.Menu()
		except:
			self.genKeysRSA()
		
	def genPrimeRelative512(self,Prime):
		PrimeRelative=self.genPrime512()
		while(self.mcd(Prime,PrimeRelative)!=1):
			PrimeRelative=self.genPrime512()
		return PrimeRelative
	
	def genPrimeRelative160(self,Prime):
		PrimeRelative=self.genPrime160()
		while(self.mcd(Prime,PrimeRelative)!=1):
			PrimeRelative=self.genPrime160()
		return PrimeRelative
	
	def genPrimeRelative(self,Prime):
		PrimeRelative=self.genPrime()
		y=1
		while(self.mcd(Prime,PrimeRelative)!=1):
			y+=1
			if(y<1000):
				PrimeRelative=self.genPrime()
			else:
				break
				self.genPrimeRelative()
		return PrimeRelative
	def genPrime(self,minimo=1,maximo=5000):
		lonM=10
		a = os.urandom(23).encode('base-64')
		N = random.randrange(minimo,maximo)
		lon=len(str(bin(N)))-2
		while(N==0 or N%2==0 or self.isPrime(N)!=True or lon<=lonM):
			N=random.randrange(minimo,maximo)
			sys.stdout.write(str('-'))
		return N
		
	def genPrime512(self):
		a = os.urandom(512).encode('base-64')
		hash512=hashlib.sha512(a)
		N512=int(hash512.hexdigest(),16)
		while(N512!=0 and N512%2==0 and self.isPrime(N512)==False):
			a = os.urandom(512).encode('base-64')
			hash512=hashlib.sha512(a)
			N512=int(hash512.hexdigest(),16)
		return N512
		
	def genPrime160(self):
		a = os.urandom(160).encode('base-64')
		hash160=hashlib.sha1(a)
		N160=int(hash160.hexdigest(),16)
		while(N160!=0 and N160%2==0 and self.isPrime(N160)==False):
			a = os.urandom(160).encode('base-64')
			hash160=hashlib.sha1(a)
			N160=int(hash160.hexdigest(),16)
		return N160
		
	# Teorema de Fermat para calcular a^m (mod n)
	def fermat(self,a, m, n):
		b = 1
		while(m!=1):
			if m%2 == 1:
				b = long((a*b) % n)
			a = pow(a,2,n)
			m = m / 2
		b = long((a*b) % n)
		return b

	# Test de primalidad de Miller-Rabin
	def miller_rabin(self,p,s,u):
		num = random.randint(2, p-2)
		a = long(self.fermat(num, s, p))
		if a != 1 and a != (p-1):
			j=1
			while j<u:
				a = long(self.fermat(a, 2, p))
				if a == (p-1):
					return True
				if a == 1:
					return False
				j+=1
			return False
		else:
			return True	

		
	def isPrime(self,p):
		s = long(p - 1)
		u = 0L
		n=1000
		while (s%2==0):
			u += 1
			s = s/2
		for i in range(n):
			prob = float( float( pow(4, i) - 1 ) / pow(4, i) )
			if self.miller_rabin(p,s,u) == False:
				return False
			else:
				return True

	def mcd(self,m,n):
		if m%n==0:
			return n
		else:
			return self.mcd(n,m%n)
		
	def cls(self):
		try:
			os.system('cls' if os.name == 'nt' else 'clear')
		except:
			print chr(27) + "[2J"
			
	def exit(self):
		try:
			os.system('exit' if os.name == 'nt' else 'exit')
		except:
			sys.exit(0)
	def generaAlfabetos(self):
		i=0;k=0;
		while(i<16):
			asciiA.append(list())
			asciiB.append(list())
			j=0
			while(j<16):
				asciiA[i].append(k)
				asciiB[i].append([int(str(i)+str(j)),k])
				k+=1
				j+=1
			i+=1
		
def main():
	global asciiA
	global asciiB
	asciiA=[]
	asciiB=[]
	rsa=RSA()
if __name__=="__main__":
	main()
