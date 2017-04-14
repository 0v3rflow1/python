#!/usr/bin/python
#-*-encoding:utf-8-*-
from numpy import *
from cv2 import *
from csv import *
import os
def main():
    global matriz
    global det
    global ext
    matriz=matrix([[11,17,11],[6,13,23],[8,3,4]])
    ext=256
    det=linalg.det(matriz)
    det=round(det%ext)
    MCD=mcd(det,ext)
    #system('clear')
    print("Cifrador y descifrador de imagenes\ncon algoritmo de Hill")
    print("**********************************************************")
    print("0)Cifrar imagen")
    print("1)Descifrar imagen")
    print("2)Salir")
    try:
        opc=input("Elige una opción: ")
        if(opc>=0 and opc<=2):
			if(MCD==1):
				if(opc==0):
					cifrar()
				elif(opc==1):
					descifrar()
				elif(opc==2):
					os.system('exit')
			else:
				print("La matriz usada no es valida")
        else:
            print("Opcion invalida")
            main()
    except:
        print("Opcion invalida")
        main()
        
def cifrar():
    img_cifrada=[]    
    path=raw_input("Ingresa ruta de la imagen: ")
    img=imread(path)
    if(img!=None):
		data=open(path)
		Name=os.path.split(data.name);
		temp=len(Name)-1;
		Name=Name[temp];
		num=len(img)
		i=0
		while(i<num):
			img_cifrada.append([])
			j=0
			while(j<num):
				new_tercia=squeeze(asarray(dot(matriz,img[i][j])%ext))
				img_cifrada[i].append(new_tercia)
				j+=1
			i+=1
		img_cifrada=array(img_cifrada)
		imshow("Imagen Original",img)
		waitKey(0)
		imwrite("cifrada_"+str(Name)+'.bmp',img_cifrada)
		print("La imagen se cifro correctamente")
    else:
        print('La imagen no existe')
        main()
        
def descifrar():
	InvDetMatriz=inv_mult(det,ext)
	if(InvDetMatriz!=False):
		matrizinv=((matriz_cofactor(matriz).T)*InvDetMatriz)%ext
		path=raw_input("Ingresa ruta de la imagen: ")
		img=[]
		imgcif=imread(path)
		if(imgcif!=None):
			data=open(path)
			Name=os.path.split(data.name);
			temp=len(Name)-1;
			Name=Name[temp];
			num=len(imgcif)
			i=0
			while(i<num):
				img.append([])
				j=0
				while(j<num):
					new_tercia=squeeze(asarray(dot(matrizinv,imgcif[i][j])%ext))
					img[i].append(new_tercia)
					j+=1
				i+=1
			img=array(img)
			imshow("Imagen Descifrada",img)
			waitKey(0)
			imwrite("descifrada"+str(Name)+'.bmp',img)
			print("La imagen se descifro correctamente")
		else:
			print('La imagen no existe')
			main()
	else:
		print("La matriz que se usa no es valida")
        
def matriz_cofactor(matriz):
    return linalg.inv(matriz).T * linalg.det(matriz)
    
def inv_mult(a,n):
	if(mcd(a,n)!=1):
		return False
	else:
		for i in range(1,n):
			if((a*i-1)%n==0):
				return i
def mcd(m,n):
	if m%n==0:
		return n
	else:
		return mcd(n,m%n)
		
if __name__=="__main__":
    main()
