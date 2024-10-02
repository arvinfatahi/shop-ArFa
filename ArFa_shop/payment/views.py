from django.shortcuts import render, redirect
from myShop.models import FactorModel, FactorProductModel, ProductModel, UserModel
from azbankgateways.models import Bank
# Create your views here.
import logging
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404

def go_to_gateway_view(request):
    final_price_ = request.session.get('final_price_session', 0)

    if final_price_ == 0:
        return HttpResponse("سبد خرید شما خالی است.")
    # amount = 50000
    user_mobile_number = "+989112221234"

    factory = bankfactories.BankFactory()
    try:
        # bank = (
        #     factory.auto_create()
        # )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank = factory.create()
        bank.set_request(request)
        bank.set_amount(final_price_)
        bank.set_client_callback_url("http://127.0.0.1:8000/payment/callback-gateway/")
        bank.set_mobile_number(user_mobile_number)

        bank_record = bank.ready()

        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e

# def callback_gateway_view(request):
#     tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
#     if not tracking_code:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     try:
#         bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
#     except bank_models.Bank.DoesNotExist:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404
#     if bank_record.is_success:
#         return HttpResponse("پرداخت با موفقیت انجام شد.")

#     return HttpResponse(
#         "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
#     )


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    if bank_record.is_success:
        cart = request.session.get('my_cart', None)
        if not cart:
            return HttpResponse("اطلاعات سبد خرید نامعتبر است.")

        if not request.user.is_authenticated:
            return HttpResponse("اطلاعات کاربر نامعتبر است.")

        user = request.user
        
        factor = FactorModel(
            user=user,
            bank_transaction=bank_record,
            is_factor=1
        )
        factor.save()

        for item in cart:
            product_instance = ProductModel.objects.get(id=item['id'])
            factor_product = FactorProductModel(
                factor=factor,
                product=product_instance,
                number=item['qty']
            )
            factor_product.save()
        
        request.session.pop('my_cart', None)
        request.session.modified = True

        return HttpResponse("پرداخت با موفقیت انجام شد.")

    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )
