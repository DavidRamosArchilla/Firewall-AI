from flask import Flask, redirect, url_for, request, jsonify, send_from_directory
from flask_cors import CORS

from pyflowmeter import sniffer

from prediction import FirewallModel

from multiprocessing import Process

model = FirewallModel()

traffic_sniffer = None

def start_my_sniffer():
    global traffic_sniffer
    traffic_sniffer = sniffer.create_sniffer(
            input_interface='eth0',
            server_endpoint='http://127.0.0.1:5000/send_traffic',
            verbose=False
        )
    print('sniffer arrancado')
    traffic_sniffer.start()

TYPES_DICT = {
        'tcp.synflood': 'test_files/pkt.TCP.synflood.spoofed.pcap',
        'udp.null': 'test_files/pkt.UDP.null.pcapng',
        'Real time traffic': 'Real time traffic'
    }

sniffer_created = False
# def start_sniffer():
#     traffic_sniffer = sniffer.create_sniffer(
#             input_interface='eth0',
#             server_endpoint='http://127.0.0.1:5000/send_traffic',
#             verbose=False
#         )
#     traffic_sniffer.start()
#     try:
#         traffic_sniffer.join()
#     except KeyboardInterrupt:
#         traffic_sniffer.stop()
#     finally:
#         traffic_sniffer.join()

# sniffer_process = Process(target=start_sniffer)
# sniffer_process.start()
app = Flask(__name__)
CORS(app) 

predicted_data = []

# Serve static files from the dist folder
@app.route('/assets/<path:filename>')
def static_files(filename):
    return send_from_directory('./client/dist/assets', filename)

# Catch-all route for the Vue.js application
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return send_from_directory('./client/dist', 'index.html')

# Handle 404 errors
@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return send_from_directory('./client/dist', 'index.html')

@app.route('/traffic-analysis')
def traffic_analysis():
    return send_from_directory('./client/dist', 'index.html')

@app.route('/send_traffic', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        # print("Received new data:", data)
        confidences, predcted_classes =  model.predict(data['flows'])
        for i, (confidence, predcted_class) in enumerate(zip(confidences, predcted_classes)):
            if predcted_class != '': # BENIGN
                flow = data['flows'][i]
                predicted_data.append({'type': predcted_class,
                                        'src_ip': f'{flow["src_ip"]}:{flow["src_port"]}',
                                        'dst_ip': f'{flow["dst_ip"]}:{flow["dst_port"]}',
                                        'confidence': f'{confidence:.2%}',
                                        'timestamp': flow["timestamp"]
                                        })

        print(model.predict(data['flows']))
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"error": "Invalid JSON data in the request"}), 400


@app.route('/get_data', methods=['GET'])
def get_data():
    print(len(predicted_data))
    return jsonify(predicted_data)

# @app.route('/get_traffic_analysis', methods=['GET'])
# def get_traffic_analysis():
    # data = {}
    # for flow in predicted_data:
    #     flow_type = flow['type']
    #     if flow_type not in data:
    #         data[flow_type] = 1
    #     else:
    #         data[flow_type] += 1
    # return jsonify(data)

@app.route('/start_sniffer', methods=['POST'])
def start_sniffer():
    if request.is_json:
        data = request.get_json()
        test_type = data['file']
        test_file = TYPES_DICT[test_type]
        reload_sniffer(test_file)
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"error": "Invalid JSON data in the request"}), 400

def reload_sniffer(test_file):
    print(test_file)
    global traffic_sniffer
    global sniffer_created
    global predicted_data
    if sniffer_created:
        try: 
            traffic_sniffer.stop()
            traffic_sniffer.join()
        except:
            pass
    else:
        sniffer_created = True

    predicted_data = []
    if test_file == 'Real time traffic':
        traffic_sniffer = sniffer.create_sniffer(
            input_interface='eth0',
            server_endpoint='http://127.0.0.1:5000/send_traffic',
        )
    else:
        traffic_sniffer = sniffer.create_sniffer(
            input_file=test_file,
            server_endpoint='http://127.0.0.1:5000/send_traffic',
        )
    traffic_sniffer.start()

if __name__ == '__main__':
    app.run(debug=True)