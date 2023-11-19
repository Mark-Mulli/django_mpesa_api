import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main import mpesa
from main.serializer import PaymentSerializer


# Create your views here.
@api_view(["POST"])
def initiate_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        phone = serializer.validated_data["phone"]
        amount = serializer.validated_data["amount"]
        headers = mpesa.generate_request_headers()
        data = {
            "BusinessShortCode": mpesa.get_business_shortcode(),
            "Password": mpesa.generate_password(),
            "Timestamp": mpesa.get_current_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": mpesa.get_business_shortcode(),
            "PhoneNumber": phone,
            "CallBackURL": mpesa.get_callback_url(),
            "AccountReference": "Sth unique",
            "TransactionDesc": "Payment for services"
        }

        resp = requests.post(mpesa.get_payment_url(), json=data, headers=headers)
        print("RESPONSE FROM SAF ", resp.json())

        return Response({"message": "Initiated STK PUSH"})


@api_view(["POST"])
def handle_callback(request):
    data = request.data
    print("CALLBACK FROM SAF", data)
    return Response({"message": "Received callback"})
