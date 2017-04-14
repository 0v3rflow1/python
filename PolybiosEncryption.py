#!/usr/bin/python
# -*- coding: utf-8 -*-
def main():
    global asciiA
    asciiA=[]
    generaAlfabetos()
    ejecuta()

def ejecuta():
    opc=input("cifrar o descifrar (0/1): ")
    if(opc==0):
        cifrar()
    elif(opc==1):
        descifrar()
    else:
        print("Opcion no valida")
    
def cifrar():
    msj=raw_input("Ingresa path del archivo a cifrar: ")
    msj=open(msj)
    msj=msj.read()
    msjc=""
    for c in msj:
        i=0
        while(i<16):
            j=0
            while(j<16):
                if(ord(c)==asciiA[i][j]):
                    msjc+=str(chr(i))+str(chr(j))
                    break
                j+=1
            i+=1
    print("Mensaje Cifrado:\n"+msjc)
    EncryptedFile=open('EncryptedFile.dat','w')
    EncryptedFile.write(str(msjc))
    EncryptedFile.close()

def descifrar():
    msjc=raw_input("Ingresa path del archivo a descifrar: ")
    msjc=open(msjc)
    msjc=msjc.read()
    msj=""
    z=0
    while(z<len(msjc)):
        i=ord(msjc[z])
        j=ord(msjc[z+1])
        msj+=str(chr(asciiA[i][j]))
        z+=2
    print("Mensaje descifrado:\n"+msj)
    DecryptedFile=open('DecryptedFile.dat','w')
    DecryptedFile.write(str(msj))
    DecryptedFile.close()
    
def generaAlfabetos():
    i=0;k=0;
    while(i<16):
        asciiA.append(list())
        j=0
        while(j<16):
            asciiA[i].append(k)
            k+=1
            j+=1
        i+=1    
if __name__=="__main__":
    main()
else:
    main()
