import re
a=open("hist.txt",'r')
text=a.read()
t=re.sub('(\d):',"\n:",text)
with open("his2.txt",'w') as f:
    f.write(t)