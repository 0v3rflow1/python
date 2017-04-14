#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath,math,os,sys;
def main():
    puntofijo();

def puntofijo():
    x=float(input('Ingresa valor inicial(X0): '));
    tolerancia=float(input('Ingresa el porcentaje de error: '));
    N=int(input('Numero maximo de iteraciones: '));
    f=input('Ingrese la función f(x), ya despejada g(f(x)): ');
    er=100;
    i=0;
    print('#iteracion\tg(f(x))\t\terror')
    while(i<=N and er>=tolerancia):
        temp=x;
        x=eval(f);
        er=abs((x-temp));
        print("%d\t\t%.4f\t\t%.4f"%(i,x,er));
        i+=1;

    print("\nLa solucion mas aproximada es: %.4f con un error de %.4f"%(x,er));
    
if __name__=="__main__":
    main();
