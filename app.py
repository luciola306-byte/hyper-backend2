from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HYPERCASH_API_KEY = os.getenv("HYPERCASH_API_KEY")
HYPERCASH_API_SECRET = os.getenv("HYPERCASH_API_SECRET")
HYPERCASH_API_URL = "https://api.hypercashbrasil.com.br/api/user/transactions"  # ajuste se necessário

headers = {
    "Content-Type": "application/json",
    "x-api-key": HYPERCASH_API_KEY,
    "x-api-secret": HYPERCASH_API_SECRET
}

@app.route("/create-transaction", methods=["POST"])
def create_transaction():
    data = request.json
    if not data:
        return jsonify({"error": "Sem dados enviados"}), 400

    # Exemplo de payload (ajuste conforme docs HyperCash)
    payload = {
        "amount": data.get("amount"),  # valor em centavos
        "currency": "BRL",
        "payment_method": data.get("payment_method"),  # ex: "credit_card"
        "customer": {
            "name": data.get("customer_name"),
            "email": data.get("customer_email")
        },
        "order_id": data.get("order_id")
    }

    try:
        response = requests.post(HYPERCASH_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



