from flask import Flask, redirect, url_for, request, jsonify, send_from_directory
from flask_cors import CORS

from pyflowmeter import sniffer

from prediction import FirewallModel


TYPES_DICT = {
        'TCP SYN flood': 'test_files/pkt.TCP.synflood.spoofed.pcap',
        'UDP null': 'test_files/pkt.UDP.null.pcapng',
        'Real time traffic': 'Real time traffic',
        'TCP reflection': 'test_files/amp.TCP.reflection.SYNACK.pcap',
        'UDP.rdm.fixedlength': 'test_files/pkt.UDP.rdm.fixedlength.pcapng',
        'UDP LDAP': 'test_files/amp.UDP.memcached.ntp.cldap.pcap',
    }

model = FirewallModel()
traffic_sniffer = None
sniffer_created = False
app = Flask(__name__)
CORS(app) 

predicted_data = []

# Serve static files from the dist folder
@app.route('/assets/<path:filename>')
def static_files(filename):
    return send_from_directory('./client/dist/assets', filename)

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

@app.route("/send_traffic", methods=["POST"])
def post_data():
    if request.is_json:
        data = request.get_json()
        confidences, predcted_classes = model.predict(data["flows"])
        for (flow, confidence, predcted_class) in zip(
            data["flows"], confidences, predcted_classes
        ):
            predicted_data.append(
                {
                    "type": predcted_class,
                    "src_ip": f'{flow["src_ip"]}:{flow["src_port"]}',
                    "dst_ip": f'{flow["dst_ip"]}:{flow["dst_port"]}',
                    "confidence": f"{confidence:.2%}",
                    "timestamp": flow["timestamp"],
                }
            )

        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"error": "Invalid JSON data in the request"}), 400


@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(predicted_data)

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
            input_interface=None,
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