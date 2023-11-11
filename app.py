from flask import Flask, redirect, url_for, request, jsonify, send_from_directory
from flask_cors import CORS

from prediction import FirewallModel

model = FirewallModel()

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

@app.route('/send_traffic', methods=['POST'])
def post_data():
    # try:
        # Check if the request data is in JSON format
        if request.is_json:
            data = request.get_json()  # This will parse the JSON data into a Python dictionary
            print("Received new data:", data)
            confidences, predcted_classes =  model.predict(data['flows'])
            for i, (confidence, predcted_class) in enumerate(zip(confidences, predcted_classes)):
                if predcted_class != '': # BENIGN
                    flow = data['flows'][i]
                    predicted_data.append({'type': predcted_class,
                                            'src_ip': f'{flow["src_ip"]}:{flow["src_port"]}',
                                            'dst_ip': f'{flow["dst_ip"]}:{flow["dst_port"]}',
                                            'confidence': float(confidence)
                                            })
                    # print({'type': predcted_class,
                    #                         'src_ip': data['flows'][i]['src_ip'],
                    #                         'confidence': float(confidence)
                    #                         })
            print(model.predict(data['flows']))
            # socketio.emit('new_data', {'field1': 'test', 'field2': 'test2'})
            # Now you can work with the 'data' dictionary
            return jsonify({"message": "Data received successfully", "data": data}), 200
        else:
            return jsonify({"error": "Invalid JSON data in the request"}), 400
    # except Exception as e:
    #     print(e)
    #     return jsonify({"error": "An error occurred while processing the request", "details": str(e)}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    # data = {"field1": "Value1", "field2": "Value2"}  # Replace with your data retrieval logic
    # data = predicted_data.copy()
    print(len(predicted_data))
    # return jsonify(data)
    return jsonify(predicted_data)

if __name__ == '__main__':
    app.run(debug=True)
    # sudo venv/bin/python cicflowmeter/src/cicflowmeter/sniffer.py -i eth0 -c flows.csv 