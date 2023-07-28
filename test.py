import threading
from time import sleep
thusk = 1
b = True;
def r():
    global b
    while b:
        print(3)
def p():
    global thusk
    global b
    thusk = 1
    th = threading.Thread(target = r)
    th.start()
    while b:
        print(1)
        

def q():
    global thusk
    global b
    while b:
        print(2)
        
        
        
t1 = threading.Thread(target=p)
t2 = threading.Thread(target=q)


t1.start()
t2.start()

sleep(10)
b = False
t1.join()
t2.join()



        
