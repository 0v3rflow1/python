#!/usr/bin/env python 
# -*- coding: utf-8 -*-
def main():
    datos()
def datos():
    print("::CIFRADO CESAR::\n")
    arc=raw_input("Ingresa path del archivo: ")
    msj=open(arc)
    msj=msj.read()
    n=input("Ingresa el desplazamiento (+ cifra - descrifra): ")
    cifradescifra(msj,n)

def cifradescifra(msj,n):
    print("\n\nCifrando con cesar")
    print("Mensaje orig:\n"+msj)
    msjc=""
    for c in msj:
        code=ord(c)
        msjc+=chr((ord(c)+n)%256)
    if(n>0):
        print("Mensaje cifrado:\n"+msjc);
        EncryptedFile=open('EncryptedFile.dat','w')
        EncryptedFile.write(str(msjc))
        EncryptedFile.close()
    else:
        print("Mensaje descifrado:\n"+msjc);
        DecryptedFile=open('DecryptedFile.dat','w')
        DecryptedFile.write(str(msjc))
        DecryptedFile.close()
    
if __name__=="__main__":
    main()
else:
    main()
