from yookassa import Configuration
from yookassa import Payment
import uuid


class Yookassa:
    def __init__(self, acc_id, key):
        Configuration.configure(acc_id, key)

    def create_payment(self, total_price=0, description='Заказ'):
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": total_price,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.merchant-website.com/return_url"
            },
            "description": description
        }, idempotence_key)

        # get confirmation url
        confirmation_url = payment.confirmation.confirmation_url
        print(payment)
        print(confirmation_url)

        return confirmation_url


