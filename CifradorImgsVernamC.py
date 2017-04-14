#-*-encoding:utf-8-*-
from numpy import *
from cv2 import *
from csv import *
import os

def main():
	os.system('clear')
	print("Cifrador y descifrador de imagenes\ncon algoritmo de Vernam [Cuadratico]")
	print("**********************************************************")
	print("0)Cifrar imagen")
	print("1)Descifrar imagen")
	print("2)Salir")
	try:
		opc=input("Elige una opción: ")
		if(opc>=0 and opc<=2):
			if(opc==0):
				cifrar()
			elif(opc==1):
				descifrar()
			elif(opc==2):
				os.system('exit')
		else:
			print("Opcion invalida")
			main()
	except e:
		print("Opcion invalida" +e)
		
	
def cifrar():
	key=[]
	imgcifrada=[]
	path=raw_input("Ingresa ruta de la imagen: ")
	img=imread(path)
	if(img!=None):
		data=open(path)
		Name=os.path.split(data.name);
		temp=len(Name)-1;
		Name=Name[temp];
		a=input("ingresa a: ")
		b=input("ingresa b: ")
		c=input("ingresa c: ")
		x0=input("ingresa semilla (x0): ")
		n=input("ingresa n: ")
		size_img=len(img)
		i=0
		while(i<size_img):
			key.append([])
			imgcifrada.append([])
			j=0
			size_img0=len(img[i])
			while(j<size_img0):
				tmp=[]
				tercia_cifrada=[]
				key[i].append([])
				imgcifrada[i].append([])
				k=0
				while(k<3):
					key_00101=generaKeyConLinealC(a,b,c,x0,n)
					tmp.append(key_00101)
					op_xor=key_00101^img[i][j][k]
					tercia_cifrada.append(op_xor)
					x0=key_00101
					k+=1
				key[i][j].append(tmp)
				imgcifrada[i][j]=tercia_cifrada
				j+=1
			i+=1
		key=array(key)
		imgcifrada=array(imgcifrada)
		imshow("Imagen Original",img)
		waitKey(0)
		imwrite("cifrada_cua_"+str(Name)+'.bmp',imgcifrada)
		print("La imagen se cifro correctamente")
		
	else:
		print('La imagen no existe')
		main()
		
def descifrar():
	key=[]
	imgdescifrada=[]
	path=raw_input("Ingresa ruta de la imagen: ")
	img=imread(path)
	if(img!=None):
		data=open(path)
		Name=os.path.split(data.name);
		temp=len(Name)-1;
		Name=Name[temp];
		a=input("ingresa a: ")
		b=input("ingresa b: ")
		c=input("ingresa c: ")
		x0=input("ingresa semilla (x0): ")
		n=input("ingresa n: ")
		size_img=len(img)
		i=0
		while(i<size_img):
			key.append([])
			imgdescifrada.append([])
			j=0
			size_img0=len(img[i])
			while(j<size_img0):
				tmp=[]
				tercia_descifrada=[]
				key[i].append([])
				imgdescifrada[i].append([])
				k=0
				while(k<3):
					key_00101=generaKeyConLinealC(a,b,c,x0,n)
					tmp.append(key_00101)
					op_xor=key_00101^img[i][j][k]
					tercia_descifrada.append(op_xor)
					x0=key_00101
					k+=1
				key[i][j].append(tmp)
				imgdescifrada[i][j]=tercia_descifrada
				j+=1
			i+=1
		key=array(key)
		imgdescifrada=array(imgdescifrada)
		imshow("Imagen Cifrada",img)
		waitKey(0)
		imwrite("descifrada_cua_"+str(Name)+'.bmp',imgdescifrada)
		print("La imagen se descifro correctamente")
		
	else:
		print('La imagen no existe')
		main()
	
def generaKeyConLinealC(a,b,c,x0,n):
	num=(a*(x0**2)+b*x0+c)%n
	return num
		
if __name__=="__main__":
	main()
else:
	main()
