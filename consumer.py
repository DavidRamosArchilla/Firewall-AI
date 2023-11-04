import time
from multiprocessing import Process, Queue, Lock

from custom_tcplife import run_tcplife_info
from custom_tcptracer import run_tcptracer_info
import requests

url = '127.0.0.1:5000/send_traffic'

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
            # Process the information
            print("Processing:", info['data'])
        # send the data to the server
        traffic_data = {
            'tcplife': tcp_life_msg,
            'tcptracer': tcp_tracer_msg
        }
        requests.post(url, json=traffic_data)
        time.sleep(2)  # Read information every 2 seconds


shared_queue = Queue()
lock = Lock()

tcp_life_producer_process = Process(target=run_tcplife_info, args=(shared_queue, lock))
tcp_tracer_producer_process = Process(target=run_tcptracer_info, args=(shared_queue, lock))
consumer_process = Process(target=consumer, args=(shared_queue,))
tcp_life_producer_process.start()
tcp_tracer_producer_process.start()
consumer_process.start()
