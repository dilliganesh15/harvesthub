from flask import Flask, request, jsonify
from twilio.rest import Client
import random

app = Flask(__name__)

# In-memory store for OTPs (use a database in production)
otp_store = {}

# Twilio credentials
account_sid = "AC1bfaf0141d27512aab2127547600a45d"  # Replace with your Twilio account SID
auth_token = "1ef2999dc955eab93c005a6f22dc3c82"    # Replace with your Twilio auth token
client = Client(account_sid, auth_token)

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    mobile_number_with_country_code = data['mobileNumberWithCountryCode']
    
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    otp_store[mobile_number_with_country_code] = otp  # Store OTP
    
    # Send OTP via SMS
    client.messages.create(
        body=f"Your OTP is {otp}",
        from_="+18304838919",  # Replace with your Twilio phone number
        to=mobile_number_with_country_code
    )
    
    return jsonify({"success": True})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    mobile_number_with_country_code = data['mobileNumberWithCountryCode']
    entered_otp = data['otp']
    
    stored_otp = otp_store.get(mobile_number_with_country_code)
    
    if str(entered_otp) == str(stored_otp):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
