import time
from pynng import Pub0, Timeout
import json
import asyncio

avionics_address = 'ipc:///tmp/test0.ipc'
altitude_address = 'ipc:///tmp/test1.ipc'
balloon_address = 'ipc:///tmp/test2.ipc'
power_address = 'ipc:///tmp/test3.ipc'


# This function supplys the packet you want to send

def data_to_send():
    json_data = {
        "gps": (43, -77),
        "pressure": 44.8}
    data = json.dumps(json_data)
    return data.encode('utf-8')


# This function creates an instance of a publisher and publishes at a
# frequency in seconds determined by the user there are 2 ways of supplying
# a message to be sent, a function call that returns an encoded dict 
# and a passed variable mes that can be unique to each instance of the

async def open_comms(address, sec, mes, board):

    with Pub0(listen=address) as pub0:
        time.sleep(0.25)
        next_msg = time.time()
        while True:
            next_msg = time.time() + sec
            pub0.send((f'{board}:').encode('utf-8') + data_to_send() +
                      mes.encode('utf-8'))
            await asyncio.sleep(next_msg-time.time())
            print(mes)


async def main():
    # 4 routines to run asynchronously
    L1 = loop.create_task(open_comms(altitude_address, 0.1,
                                     ": sent 0", 'altitude'))
    L2 = loop.create_task(open_comms(avionics_address, 0.2,
                                     ": sent 1", 'avionics'))
    L3 = loop.create_task(open_comms(balloon_address, 0.3,
                                     ": sent 2", 'balloon'))
    L4 = loop.create_task(open_comms(power_address, 0.1,
                                     ": sent 3", 'power'))
    await asyncio.wait([L1, L2, L3, L4])


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except Exception as e:
        pass
    finally:
        loop.close()
