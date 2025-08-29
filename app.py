from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Chave do HyperCash (sandbox ou produção)
HYPERCASH_API_KEY = os.getenv("HYPERCASH_API_KEY")
HYPERCASH_API_URL = "https://sandbox-api.hypercashbrasil.com.br/api/user/transactions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {HYPERCASH_API_KEY}"

}

@app.route("/create-transaction", methods=["POST"])
def create_transaction():
    data = request.json
    if not data:
        return jsonify({"error": "Sem dados enviados"}), 400

    # Monta payload para HyperCash
    payload = {
        "amount": data.get("amount"),  # valor em centavos
        "currency": "BRL",
        "paymentMethod": data.get("payment_method"),  # PIX, BOLETO, CREDIT_CARD
        "customer": {
            "name": data.get("customer_name"),
            "email": data.get("customer_email"),
            "document": {
                "number": data.get("customer_cpf", "00000000000"),
                "type": "CPF"
            }
        },
        "order_id": data.get("order_id")
    }

    # Se for cartão de crédito, incluir dados do cartão
    if data.get("payment_method") == "CREDIT_CARD":
        payload["card"] = {
            "number": data.get("card_number"),
            "holderName": data.get("card_holder"),
            "expirationMonth": data.get("card_exp_month"),
            "expirationYear": data.get("card_exp_year"),
            "cvv": data.get("card_cvv")
        }

    try:
        response = requests.post(HYPERCASH_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        res_json = response.json()

        return jsonify({
            "status": "approved" if res_json.get("status") == "APPROVED" else "pending",
            "transaction_id": res_json.get("id"),
            "message": res_json.get("message", "Pagamento processado")
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)





