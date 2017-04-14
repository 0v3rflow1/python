#-*-encoding:utf-8-*-
from numpy import *
from cv2 import *
from csv import *
import os
def main():
	os.system('clear')
	print("Cifrador y descifrador de imagenes\ncon secuencia cifrante LFSR")
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
def gen_sec_lfsr():
	pol=eval(raw_input("Ingresa los taps del polinomio (ej:[20,3]=>x²⁰+x³+1): "))
	T=input("Periodo de la secuencia cifrante(0 para usar 2^n+1): ")
	i=0;
	pol_str="";
	while(i<len(pol)):
		pol_str+="x^"+str(pol[i])+"+";
		i+=1;
	pol_str+="1";
	print("Tu polinomio es: \n\n"+pol_str);
	print("Generando secuencia LFSR\n##################################\n")
	grad_pol=pol[0];
	for x in range(0,len(pol)):
		if(pol[x]>grad_pol):
			grad_pol=pol[x]
	semilla='0b'+format(int(raw_input("Semilla: ")),str(grad_pol)+'d').replace(" ",'0');
	semilla=format(eval(semilla),str(grad_pol)+'b').replace(" ",'0');
	print(semilla+"\n######################\n\n");
	if(T==0):
		T=2**grad_pol-1;
	print("El periodo maximo de la secuencia cifrante sera de : "+str(T));
	print("\nGENERANDO SECUENCIA\n#####################################################");
	i=0;
	secuencia=semilla;
	tmp="";
	print("Estado\t\t\tsemilla\t\t\trealimentación\t\t\tresultado")
	while(i<T):
		j=0;
		tmp="";		
		while(j<len(pol)):
			if(j!=(len(pol)-1)):
				if(j==0):
					tmp+=semilla[j-1]+"^";
				else:
					tmp+=semilla[j-1]+"^";
			else:
				tmp+=semilla[j-1];
			j+=1;
		vsem=semilla;
		semilla=format(eval('0b'+semilla)>>1,str(grad_pol)+'b').replace(" ",'0');
		semilla=str(eval(tmp))+semilla[1:]
		print(str(i)+'\t\t\t'+str(vsem)+'\t\t\t'+tmp+'='+str(eval(tmp))+'\t\t\t'+semilla)
		secuencia+=semilla;
		i+=1;
	return secuencia;

def cifrar():
	key=[]
	imgcifrada=[]
	path=raw_input("\nIngresa ruta de la imagen: ")
	img=imread(path)
	if(img!=None):
		data=open(path)
		Name=os.path.split(data.name);
		temp=len(Name)-1;
		Name=Name[temp];
		size_img=len(img)
		secuenciaLFSR=gen_sec_lfsr()*((size_img*size_img)^size_img);
		#print("\n########################################\nSecuencia cifrante generada:\n########################################\n"+secuenciaLFSR);
		i=0
		z=0;
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
					num=int("0b"+secuenciaLFSR[((i+z)*8):((i+z+1)*8)],2)
					key_00101=num
					tmp.append(key_00101)
					op_xor=key_00101^img[i][j][k]
					tercia_cifrada.append(op_xor)
					x0=key_00101
					z+=1
					k+=1
				key[i][j].append(tmp)
				imgcifrada[i][j]=tercia_cifrada
				j+=1
			i+=1
		key=array(key)
		imgcifrada=array(imgcifrada)
		imshow("Imagen Original",img)
		waitKey(0)
		imwrite("cifrada_LFSR_"+str(Name)+'.bmp',imgcifrada)
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
		size_img=len(img)
		secuenciaLFSR=gen_sec_lfsr()*((size_img*size_img)^size_img);
		#print("\n########################################\nSecuencia descifrante generada:\n########################################\n"+secuenciaLFSR);
		i=0
		z=0
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
					num=int("0b"+secuenciaLFSR[((i+z)*8):((i+z+1)*8)],2)
					key_00101=num
					tmp.append(key_00101)
					op_xor=key_00101^img[i][j][k]
					tercia_descifrada.append(op_xor)
					x0=key_00101
					k+=1
					z+=1
				key[i][j].append(tmp)
				imgdescifrada[i][j]=tercia_descifrada
				j+=1
			i+=1
		key=array(key)
		imgdescifrada=array(imgdescifrada)
		imshow("Imagen Cifrada",img)
		waitKey(0)
		imwrite("descifrada_LFSR_"+str(Name)+'.bmp',imgdescifrada)
		print("La imagen se descifro correctamente")

	else:
		print('La imagen no existe')
		main()
if __name__=="__main__":
	main()
else:
	main()
