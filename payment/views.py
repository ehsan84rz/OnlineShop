from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from django.conf import settings

import json
import requests

from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rials_total_price = toman_total_price * 10

    zarinpal_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rials_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback'))
    }

    res = requests.post(url=zarinpal_url, data=json.dumps(request_data), headers=request_headers)
    print(res.json())
    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error From ZarinPal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_autority=payment_authority)
    toman_total_price = order.get_total_price()
    rials_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rials_total_price,
            'authority': payment_authority,
        }

        res = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_headers,
        )

        if 'data' in res.json() and 'errors' not in res.json() or len(res.json()['errors']) == 0:
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت با موفقیت انجام شد')

            elif payment_code == 101:
                return HttpResponse('این پرداخت پیش از این با موفقیت انجام و ثبت شده بود')

            else:
                error_code = res.json()['errors']['code']
                error_mesage = res.json()['errors']['message']
                return HttpResponse(f'{error_code} {error_mesage} | این تراکنش نا موفق بود ')
    elif payment_status == 'NOK':
        return HttpResponse('تراکنش ناموفق بود')


def payment_process_sandbox(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rials_total_price = toman_total_price * 10

    zarinpal_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    request_data = {
        'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
        'Amount': rials_total_price,
        'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback'))
    }

    res = requests.post(url=zarinpal_url, data=json.dumps(request_data), headers=request_headers)
    print(res.json())
    data = res.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error From ZarinPal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rials_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        request_data = {
            'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
            'Amount': rials_total_price,
            'Authority': payment_authority,
        }

        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_headers,
        )

        if 'errors' not in res.json() or len(res.json()['errors']) == 0:
            data = res.json()
            print(data)
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت با موفقیت انجام شد')

            elif payment_code == 101:
                return HttpResponse('این پرداخت پیش از این با موفقیت انجام و ثبت شده بود')

            else:
                error_code = res.json()['errors']['code']
                error_mesage = res.json()['errors']['message']
                return HttpResponse(f'{error_code} {error_mesage} | این تراکنش نا موفق بود ')
    elif payment_status == 'NOK':
        return HttpResponse('تراکنش ناموفق بود')
