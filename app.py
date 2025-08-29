from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HYPERCASH_API_KEY = os.getenv("pk_b48f62cc1f920cdaaf9c7bea2cf1e0a20edba5f9")
HYPERCASH_API_SECRET = os.getenv("sk_b4ed44b6073bae4aed687393a6b7baf8e0047746T")
HYPERCASH_API_URL = "https://api.hypercashbrasil.com.br/api/user/transaction"  # ajuste se necessário

headers = {
    "Content-Type": "application/json",
    "x-api-key": "pk_b48f62cc1f920cdaaf9c7bea2cf1e0a20edba5f9",
    "x-api-secret": "sk_b4ed44b6073bae4aed687393a6b7baf8e0047746T"
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
        response = requests.post("https://api.hypercashbrasil.com.br/api/user/transactions", json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
