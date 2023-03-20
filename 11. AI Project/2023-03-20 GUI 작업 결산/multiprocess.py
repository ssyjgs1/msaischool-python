from send_email import *
from multiprocessing import Process
import time
from datetime import datetime

target = 'military drone' 
test_1 = "1"
test_2 = "2"
test_3 = "3"

while True:
    now = datetime.now()
    print("timestamp : ", now.timestamp())

    # multiprocess or thread 수정 필요
    th3 = Process(target = send_alarm, args= (target, test_1, test_2, test_3,))
    th3.start()
    th3.join()
    time.sleep(60)
    th3.terminate()

    time.sleep(10)