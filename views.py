from django.conf import settings
from django.http import HttpResponse 
import requests
import json
from django.shortcuts import redirect


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# amount = 100000
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = '09123456789'  # Optional
# Important: need to edit for realy server. Add appname
CallbackURL = 'http://127.0.0.1:8000/appname/verify/'


def send_request(request):
    global amount 
    amount = request.GET['amount']
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                global authority
                authority=  response['Authority']
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return {'status': False, 'code': str(response['Status'])}
            
        return HttpResponse(response)
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(Authority):
    global Authoritystatus
    Authoritystatus = Authority.GET['Authority']
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": Authoritystatus,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers,timeout=10)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return HttpResponse (str({'status': True, 'RefID': response['RefID']}))
        else:
            return HttpResponse (str({'status': False, 'code': str(response['Status'])}))
    return response
