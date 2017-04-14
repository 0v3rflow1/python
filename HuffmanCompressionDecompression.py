# -*- coding: utf-8 -*-
import Tkinter,os,sys
from Tkinter import *
import tkFileDialog

code = {}
stri=""
def Freq(stri):
    freq = {}
    for ch in stri:
    	freq[ch] = freq.get(ch,0)+1
    #print freq
    SortFreq(stri,freq)

def SortFreq(stri,freq):
    tuples=[]
    for all in freq:
    	tuples.append((freq[all],all))
    tuples.sort()
    #print tuples
    BuildTree(stri,tuples)

def BuildTree(stri,tuples):
    global string
    while len(tuples)>1:
    	leastTwo=tuple(tuples[0:2])
    	rest=tuples[2:]
    	combFreq=leastTwo[0][0]+leastTwo[1][0]
    	tuples=rest+[(combFreq,leastTwo)]
    	tuples.sort()
    #print tuples 
    trimed = Trim(tuples[0])
    Coding(trimed)
    #print("\nTRIMED\n"+str(trimed))
    #print("\nCODING\n"+str(Coding(trimed)))

    encode =encoding(stri)
    i=0;
    encode_hex=''
    while(i<len(encode)):
	encode_hex+=chr(eval('0b'+encode[i:(i+8)]))
	i+=8
	
    boxTextC.delete('1.0',END)
    boxTextC.insert(INSERT, "%s"%(encode))
    encode=encode_hex;
    fileEncode=open('FileEncode.dat','w')
    fileEncode.write(encode)
    fileEncode.close()
    fileTrimed=open('FileTrimed.dat','w')
    fileTrimed.write(str(trimed))
    fileTrimed.close()
    tam = os.path.getsize("FileEncode.dat")
    print("Tamaño del archivo comprimido:%s Bytes"%float(tam))

def Trim(tuples):
    p=tuples[1];
    if type(p)==type(""):
    	return p
    else:
    	return (Trim(p[0]),Trim(p[1]))


def Coding(node,pat=""):
    global code
    if type(node)==type(""):
    	code[node] = pat

    else:
        Coding(node[0],pat+'0')
        Coding(node[1],pat+'1')
    return code	
	

def encoding(str):
    global code
    result=""
    for let in str:
    	result+=code[let]
    return result	

def decoding(tree,str):
    result=""
    p=tree
    for num in str:
    	if num=='0':
    	    p=p[0]
    	else:
    	    p=p[1]
    	if type(p)==type(""):
    	    result+=p
    	    p=tree
    return result
    

def OpenFile(decode_msj=False):
    path=tkFileDialog.askopenfilename(parent=ventana,title='Escoje el Archivo')
    tam = os.path.getsize(path)
    campoTextoEntrada.delete(0,END)
    campoTextoEntrada.insert(0,path)
    _file=open(path)
    stri=_file.read()
    boxTextD.delete('1.0',END)
    boxTextD.insert(INSERT, "%s"%(stri))
    if(decode_msj==False):
        Huffman(stri,tam)
    else:
        HuffmanInverse(stri,tam)

def Huffman(msj,tam):
	print("Tamaño del archivo original:%s Bytes"%float(tam))
	Freq(msj)
    

def HuffmanInverse(msj,tam):
    FileTrimed=open('FileTrimed.dat')
    print("Tamaño del archivo comprimido:%s Bytes"%float(tam));
    trimed=eval(FileTrimed.read());
    encode=msj
    encode_hex=''
    i=0
    while(i<len(encode)):
		encode_hex+=format(ord(encode[i]),"8b").replace(" ",'0')
		i+=1
    boxTextC.delete('1.0',END)
    encode=encode_hex
    boxTextC.insert(INSERT, "%s"%(encode))
    decode=decoding(trimed,encode)
    boxTextD.delete('1.0',END)
    boxTextD.insert(INSERT, "%s"%(decode))
    fileDecode=open('FileDecode.dat','w')
    fileDecode.write(str(decode))
    fileDecode.close()
    tam = os.path.getsize("FileDecode.dat")
    print("Tamaño del archivo descomprimido:%s Bytes"%float(tam))

def main():
    global ventana,campoTextoEntrada,boxTextD,boxTextC,stri
    ventana = Tkinter.Tk()
    ventana.title("31337::Compresor-Huffman::00101")
    #ventana.maxsize(height=180,width=600)
    #ventana.minsize(height=180,width=600)
    ventana.geometry("813x590")
    logo = PhotoImage(file="logo.gif")
    Label(ventana,image=logo).grid(row=0,column=1)
    Label(ventana, text="31337::Compresor-Huffman::00101").grid(row=1,column=1)

    campoTextoEntrada = Entry(ventana, width=60)
    campoTextoEntrada.grid(row=2, column=1)
    botonAbrirLectura = Button(ventana, text="Comprimir", width=15,command=lambda:OpenFile(False))
    botonAbrirLectura.grid(row=1, column=3)

    botonAbrirEscrituraD = Button(ventana, text="Descomprimir", width=15,command=lambda:OpenFile(True))
    botonAbrirEscrituraD.grid(row=2, column=3)

    boxTextD=Text(ventana,width=50)
    boxTextD.grid(row=7,column=1)
    boxTextC=Text(ventana,width=50)
    boxTextC.grid(row=7,column=3)
    ventana.mainloop()
    
if __name__=="__main__":
    main()
else:    
    main()
