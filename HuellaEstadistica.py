#!/usr/bin/python
# -*- coding: utf-8 -*-
import re,os,sys,time;
#Funcion principal
def main():
	#Guardamos en ContentArchive lo que
	#retorne la funcion LeeArchivo
	ContentArchive=LeeArchivo();
	#Verificamos si el archivo existe
	if(ContentArchive):
		#Si existe ejecutamos la funcion StatisticalRescues
		#pasando como parametro el contenido del archivo
		StatisticalRescues(ContentArchive);
	else:
		#Si no existe le notificamos al usuario
		print("No se encontro el archivo");
	
#Funcion StatisticalRescues
def StatisticalRescues(ContentArchive):
	#Rescatamos el contenido (Texto)
	#que contiene el documento
	Content=ContentArchive.read();
	#Contamos cuantos caracteres tiene
	#y lo guardamos en _len
	_len=len(Content);
	#Iniciamos contador i a cero
	i=0;
	#creamos una lista vacia
	matrix=[];
	#Llenamos la matriz con los 256
	#caracteres ascci indice uno
	#y con la cantidad de veces que 
	#este aparece en el documento 
	#indice 0 de la matriz

	#Mientras i < 256
	while(i<256):
		#matrix le agregamos un elemento
		#con la estructura [[count],[CodeAscii]]
		matrix+=[[0,[ord(chr(i))]]];
		#Incrementamos el contador 
		#i en una unidad
		i+=1;
	#Recorremos caracter por caracter el
	#contenido del archivo e incrementamos
	#el contador correspondiente al caracter actual 
	for Char in Content:
		#Incrementamos en una unidad el contador
		#del caracter actual, recuerda matrix
		#tiene la estructura matrix[indice][contador][CodeAscii]
		matrix[ord(Char)][0]+=1;
	#Imprimimos el numero de caracteres totales que
	#contiene el documento
	print("\nNumero de caracteres: "+str(_len));
	print("\n======================================\n");
	#Imprimimos los datos de la huella estadistica
	#Es decir las veces que aparece cada caracter Ascii
	print("\nHuella estadistica\n");
	print("\n======================================\n");
	i=0;
	#hacemos un recorrido
	while(i<256):
		#Imprimimos el contenido de la matrix[i]
		#Arrojara [[Contador][CodeAscii]]
		print(str(matrix[i]));
		#incrementamos en una unidad i
		i+=1;
	#imprimimos el contenido del archivo    
	print("\nContenido del archivo:\n======================================\n"+Content);
	#creamos la grafica de la huella digital
	CreateGraphical(matrix,ContentArchive,Content);

#Funcion CreateGraphical
def CreateGraphical(matrix,ContentArchive,Content):
	#Guardamos el nombre del archivo
	Name=os.path.split(ContentArchive.name);
	temp=len(Name)-1;
	Name=Name[temp];
	#Guardamos las estadisticas de la huella digital
	statistical_footprint="";
	#iniciamos i con 0
	i=0;
	#recorremos desde i=0 hasta i=256
	while(i<256):
		#guardamos en statistical_footprint la informacion de la huella estadistica
		#con el formato (code_ascii,caracter,numerodevecesqueaparece)
		statistical_footprint+="("+str(matrix[i][1][0])+","+chr(matrix[i][1][0])+","+str(matrix[i][0])+")\n";
		#aumentamos en una unidad i
		i+=1;
	try:
		#Solicitamos el ancho y alto de la grafica en pixeles
		width=input("\n\nIngresa ancho de la grafica (px): ");
		height=input("\nIngresa alto de la grafica (px): ");
	except:
		#Si no se ingresa un alto y ancho
		#usamos los de por default
		width=6900;
		height=400; 
	#en caso de que las dimensiones no sean validas
	if(width<400 or (not isinstance(height,int))):
		#usamos el default
		width=6900;
	#en caso de que las dimensiones no sean validas         
	if(height<400 or (not isinstance(height,int))):
		#usamos el default
		height=400;
	#damos un nombre a la grafica
	name=str('graficas/graph_'+str(Name)+'.html');
	#creamos el archivo de la grafica
	graph=open(name,'w');
	#Creamos las etiquetas del eje x
	#es decir los caracteres desde 0 - 255
	i=0;
	labels="[";
	while(i<256):
		if(matrix[i][0]>0):
			if(i<255):
				labels+="'"+str((matrix[i][1][0]))+"',";
			else:
				labels+="'"+str((matrix[i][1][0]))+"'";
		i+=1;
	labels+="]";
	i=0;
	data="[";
	#Creamos las etiquetas del eje y
	#es decir las veces que aparece cada
	#caracter en el archivo
	while(i<256):
		if(matrix[i][0]>0):
			if(i<255):
				data+=str(matrix[i][0])+",";
			else:
				data+=str(matrix[i][0]);
		i+=1;
	data+="]";
	#El codigo que genera la grafica
	#JS Y HTML AQUI ENTRAN :P
	code="""
		<html>
			<head>
				<title>Huella estadistica del archivo """+Name+"""</title>
				<script src='Chart.min.js'></script>
				<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'></script>
			</head>
			<body>
				<center>
					<h1>
						Huella estadistica del documento """+Name+"""
					</h1>
				<div style='float:left'>
					<h1>Contenido del archivo<h1/>
					<textarea style="font-size:10px;resize:none;width:980px;height:200px;">
						"""+Content+"""
					</textarea>
				</div>
				<div style='float:left'>
					<h1>Huella estadistica<h1/>
					<textarea style="resize:none;width:400px;height:200px;">
						"""+str(statistical_footprint)+"""
					</textarea>
				</div>
				<div style='clear:both'>
				</center>
				<center>
					<h1>
						Gr&aacute;fica de la huella estadistica del documento """+Name+"""
					</h1>
				</center>
				<canvas id='myChart' width='"""+str(width)+"""' height='"""+str(height)+"""'></canvas>
			</div>
		</body>
		<script type='text/javascript'>
			var data = {
				labels :"""+labels+""",
				datasets : [
					{
						fillColor : 'rgba(255,0,0,0.5)',
						strokeColor : 'rgba(255,0,0,1)',
						pointColor : 'rgba(255,0,0,1)',
						pointStrokeColor : '#fff',
						data : """+data+"""
					}
				]
			}
			options = {animationSteps : 0}
			var ctx = document.getElementById('myChart').getContext('2d');
			var myNewChart = new Chart(ctx).PolarArea(data,options);
			new Chart(ctx).Bar(data);
		</script>
	</html>
	""";
	#Escribimos el codigo en el archivo de la grafica
	graph.write(code);
	#cerramos el archivo de la grafica
	graph.close();
	#cerramos el archivo
	ContentArchive.close();
#Funcion LeeArchivo
def LeeArchivo():
	try:
		#Limpiamos la pantalla
		os.system('clear');
		#Solicitamos la ruta del archivo
		path=raw_input("Ingresa la ruta del archivo: ");
		#Guardamos en una instancia la apertura del archivo
		instance=open(path);
		content=instance;
	except:
		#Si hay error de apertura o no existe
		content=False;
	#Retornamos el contenido
	return content;
if __name__=="__main__":
	main();
