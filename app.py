from flask import Flask, request, jsonify

app = Flask(__name__)

VAULT_PASSWORD = "369369"

@app.route("/api/vault", methods=["POST"])
def vault():
    password = request.json.get("password")

    if password == VAULT_PASSWORD:
        return jsonify({
            "success": True,
            "message": "تم الوصول بنجاح"
        })

    return jsonify({
        "success": False,
        "message": "كلمة المرور غير صحيحة"
    }), 401
