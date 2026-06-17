from flask import Flask, request, jsonify

app = Flask(__name__)

# قاعدة بيانات وهمية في الذاكرة (سريعة وخفيفة)
discoveries = []

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    discoveries.append(data)
    print(f"📡 القائد تلقى بلاغاً: {data}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
