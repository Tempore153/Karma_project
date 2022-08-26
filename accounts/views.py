from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from karma import settings
#liqpay
from liqpay import LiqPay

from django.views.generic import TemplateView, View


from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'accounts/dashboard.html')

def about(request):
    return render(request, 'accounts/about.html')

def donate(request):
    return render(request, 'accounts/donate.html')

#LiqPay class
class PayView(TemplateView):
    template_name = 'accounts/payment.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '100',
            'currency': 'USD',
            'description': 'Payment for clothes',
            'order_id': 'order_id_1',
            'version': '3',
            'sandbox': 0, # sandbox mode, set to 1 to enable it
            'server_url': 'https://test.com/billing/pay-callback/', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})

@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)
        return HttpResponse()