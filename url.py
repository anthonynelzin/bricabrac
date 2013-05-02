import re
string = 'Je cherche une URL http://nelz.in/anthony/ et je la trouve.'
print re.findall(r'(https?://\S+)', string)