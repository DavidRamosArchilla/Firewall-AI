from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_traffic', methods=['POST'])
def post_data():
    try:
        # Check if the request data is in JSON format
        if request.is_json:
            data = request.get_json()  # This will parse the JSON data into a Python dictionary
            print("Received data:", data)
            # Now you can work with the 'data' dictionary
            return jsonify({"message": "Data received successfully", "data": data}), 200
        else:
            return jsonify({"error": "Invalid JSON data in the request"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the request", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)