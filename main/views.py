from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(["POST"])
def initiate_payment(request):

    return Response({"message":"Initiated STK PUSH"})


def handle_callback(request):
    return None