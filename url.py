import re
s = 'Lorem ipsum http://tinyurl.com/blah dolor http://blabla.com'
print re.findall(r'(https?://\S+)', s)