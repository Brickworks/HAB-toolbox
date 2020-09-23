import sys
import time
from pynng import Pub0,Sub0,Timeout
import json

avionics_address = 'ipc:///tmp/test0.ipc'
altitude_address = 'ipc:///tmp/test1.ipc'
balloon_address = 'ipc:///tmp/test2.ipc'
power_address = 'ipc:///tmp/test3.ipc'

mes_rec = []
avi_msg = []
alt_msg = []
bal_msg = []
pow_msg = []
msg_log = []


def extract_data(comp_data, prefix):
#extract_data is fed a list of string serialized json messages
#it then deserializes them into readable json
    unpacked_data = []
    while len(comp_data) > 0:
        #takes the encoded string serialized json data and stores it as readable json
        unpacked = json.loads(comp_data.pop(0).decode('utf-8').strip(prefix))
        unpacked_data.append(unpacked)
    return unpacked_data


def main():
    with Sub0(dial=avionics_address, recv_timeout=300) as sub0, \
            Sub0(dial=altitude_address, recv_timeout=300) as sub1, \
            Sub0(dial=balloon_address, recv_timeout=500) as sub2, \
            Sub0(dial=power_address, recv_timeout=300) as sub3: #pubsub obj constructors

        sub0.subscribe(b'avionics') #sub to the altitude topic
        sub1.subscribe(b'altitude') #sub to the avionics topic
        sub2.subscribe(b'balloon')
        sub3.subscribe(b'power')
        sub0.recv_buffer_size = 1024
        sub1.recv_buffer_size = 1024
        sub2.recv_buffer_size = 1024
        sub3.recv_buffer_size = 1024
        time.sleep(0.05)
        start = time.time()
        try:
            while True:
                try:
                    mes_rec.append(sub0.recv())
                    mes_rec.append(sub1.recv())
                    mes_rec.append(sub2.recv())
                    mes_rec.append(sub3.recv())
                    msg_log.append(time.time()-start)
                except Timeout:
                    print('Timeout, no message recieved')
                    time.sleep(0.25)
        except KeyboardInterrupt:
            pass
        print(mes_rec)
        extract_data(mes_rec,"altitude:")


if __name__ == "__main__":
    main()