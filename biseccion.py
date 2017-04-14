#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath,math,os,sys;
def main():
    biseccion();

def biseccion():
    A=C=I=G=Num=Cp=B=0;
    f=input('Digite la función: ');
    A=float(input('Digita el valor de A: '));
    C=float(input('Digita el valor de C: '));
    N=float(input('Digita el numero de iteraciones: '));
    Cp=float(input('Digite el criterio de parada: '));
    Er=float(Cp+1);
    x=A;
    fA=eval(f);
    x=C;
    fC=eval(f);
    if(fA*fC>0):
        print('No existen Raíces en esta Ecuación');
    else:
        while(Er>Cp and I<N):
            I=I+1;
            Ant=B;
            G=A+C;
            B=G/2;
            x=B;
            fB=eval(f);
            if(fA*fB<=0):
                C=B;
                fC=fB;
            else:
                A=B;
                fA=fB;
            Er=abs(((B-Ant) /B)*100);
            print('A= %.4f\tB= %.4f\tC= %.4f\tfA= %.4f\tfB= %.4f\tfC= %.4f\tEr= %.1f%%'%(A,B,C,fA,fB,fC,Er));
        
        print('\n\nLa Raíz es: %.4f'%B);

    
if __name__=="__main__":
    main();
