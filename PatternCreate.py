import hashlib
import sys
import random
class PatternCreate:
  ext=None
  def __init__(self,ext=0):
    self.ext=ext;
  def generate_pattern(self):
    ext=int(self.ext)
    i=0
    string=str(random.randint(0,31337));
    while(i<ext):
        string+=hashlib.sha512(string).hexdigest()
        i=len(string)
    return string[0:ext]

def main(argv):
  obj=PatternCreate(argv[1])
  pattern=obj.generate_pattern()
  file=open('pattern.txt','w+')
  file.write(pattern)
  file.close()
  print pattern
  print "\nPatron de "+obj.ext+" caracteres generado correctamente..."
  
if __name__=="__main__":
  if(len(sys.argv)==2): 
    main(sys.argv)
  else:
    print('Parametros no validos PatternCreate.py <longitud>')
