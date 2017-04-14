import cv2
import numpy as np
from matplotlib import pyplot as plt
try:
	name=raw_input("Ingresa nombre de la imagen: ")
	img = cv2.imread(name)
	if(img!=None):
		color = ('b','g','r')
		for i,col in enumerate(color):
			histr = cv2.calcHist([img],[i],None,[256],[0,256])
			plt.xlim([0,256])
		plt.show()
	else:
		print("No existe la imagen")
except:
	print("Error")
