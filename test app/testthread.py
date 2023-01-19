from threading import Thread
import time
import datetime
from time import strftime ,gmtime

class myThread(Thread):
    def __init__(self, name, counter, delay):
        super(myThread, self).__init__()
        self.name= name
        self.counter=counter
        self.delay=delay
    def run(self):
        print("san sang chay" + self.name)
        while self.counter:
            time.sleep(self.delay)
            print("%s: %s" % (self.name, time.ctime(time.time())))
            self.counter-=1
        print("ket thuc vong lap", self.name)
    def ThreadofThread():
        print("chay di nao thread3")
        thread3 = myThread("thread 3", 2, 3)
        thread3.start()    
try:
    print("bat dau")
    print("bat dau")
    print("bat dau")
    print("bat dau")
    print("bat dau")
    thread1 = myThread("thread 1", 2, 2)
    thread2 = myThread("thread 2", 2, 5)
    money = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    # - datetime.datetime(2022, 7, 7, 22, 0, 40)
    string = strftime("%H:%M:%S\n%d-%m-%Y", gmtime())  
    print(money)
    myThread.ThreadofThread()
    thread1.start()
    thread2.start()
    print("bat dau")
    print("bat dau")
    print("bat dau")
    print("bat dau")
    print("bat dau")

except:
 	print("Error")

# ->chạy tuần tự, đến thread khi đó mới chạy đồng thời các thread với nhau
# chạy tuần tự sẽ xử lí hết trước, thread chạy đồng thời (một khi đã có thread thì gần như chạy đồng thời)