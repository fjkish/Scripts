from threading import Thread
import subprocess
import os

def call_script(scriptX,argX):
    print argX
    result = os.system(scriptX + ' ' +argX)


s1 = '\"'+ r'C:\Users\fran2604\Desktop\t1.py' +'\"'
s2 = r'C:\Users\fran2604\Desktop\t2.py'
s3 = r'C:\Users\fran2604\Desktop\t3.py'

t1 = Thread(target=call_script, args=(s1,"1"))
t2 = Thread(target=call_script, args=(s1,"2"))
t3 = Thread(target=call_script, args=(s1,"3"))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()


print "done"