import os
import json
import requests
from groq import Groq
from requests.auth import HTTPBasicAuth


# Initialize the Groq client using the key from .env
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def evaluate_submission(criteria, code):
    prompt = f"Criteria: {criteria}\n\nSubmitted Code:\n{code}"
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system", 
                "content": "You are an automated code reviewer. You must respond in valid JSON format containing exactly two keys: 'status' (must be exactly 'approved' or 'rejected') and 'feedback' (a short explanation)."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def get_paypal_token():
    client_id = os.environ.get("PAYPAL_CLIENT_ID")
    client_secret = os.environ.get("PAYPAL_SECRET")
    
    # We are using the sandbox environment URL
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token" 
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    # Authenticate using HTTP Basic Auth
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    response.raise_for_status()
    
    return response.json()["access_token"]

def release_escrow_funds(receiver_email, amount, reference_id):
    token = get_paypal_token()
    url = "https://api-m.sandbox.paypal.com/v1/payments/payouts"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" # Pass the access token
    }
    
    # Define the payout batch structure
    payload = {
        "sender_batch_header": {
            "sender_batch_id": f"EscrowPayout_{reference_id}",
            "email_subject": "Your code was approved! Here is your bounty."
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(amount),
                    "currency": "USD"
                },
                "note": "Automated payout via TrustNode Escrow",
                "sender_item_id": str(reference_id),
                "receiver": receiver_email
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()