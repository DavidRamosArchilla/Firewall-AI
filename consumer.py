import time
from multiprocessing import Process, Queue, Lock

from custom_tcplife import run_tcplife_info
from custom_tcptracer import run_tcptracer_info
import requests

url = 'http://127.0.0.1:5000/send_traffic'

def consumer(queue):
    while True:
        tcp_life_msg = []
        tcp_tracer_msg = []
        while not queue.empty():
            info = queue.get()
            if info['source'] == 'tcplife':
                print('tcplife')
                tcp_life_msg.append(info['data'])
            elif info['source'] == 'tcptracer':
                print('tcptracer')
                tcp_tracer_msg.append(info['data'])

        if len(tcp_life_msg) != 0 or len(tcp_tracer_msg) != 0:
        # send the data to the server
            traffic_data = {
                'tcplife': tcp_life_msg,
                'tcptracer': tcp_tracer_msg
            }
            response = requests.post(url, json=traffic_data)
            # if response.status_code == 200:
            #     print("Server response:", response.json())
            # else:
            #     print("Error:", response.text)
        time.sleep(2)  # Read information every 2 seconds


shared_queue = Queue()
lock = Lock()

tcp_life_producer_process = Process(target=run_tcplife_info, args=(shared_queue, lock))
tcp_tracer_producer_process = Process(target=run_tcptracer_info, args=(shared_queue, lock))
consumer_process = Process(target=consumer, args=(shared_queue,))
tcp_life_producer_process.start()
tcp_tracer_producer_process.start()
consumer_process.start()
