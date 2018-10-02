from unittest import TestCase
import time
from utils import build_params
from api import TransferControl, PaymentPage, Customer, Invoice, Transaction, Refund


SECRET_KEY = 'YOUR PAYSTACK SECRET_KEY'
PUBLIC_KEY = 'YOUR PAYSTACK PUBLIC_KEY'


class TestCustomer(TestCase):
    def setUp(self):
        self.api = Customer(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        self.api.create_customer(email='test@example.com')
        self.customer_id = self.api.customer_id
        self.customer_code = self.api.customer_code

    def test_create_customer(self):
        self.assertEqual(self.api.ctx.status, True)

    def test_fetch_customer(self):
        self.api.fetch_customer(
            email_or_id_or_customer_code='test@example.com')
        self.assertEqual(self.customer_code, self.api.customer_code)
        self.assertEqual(self.customer_id, self.api.customer_id)
        self.assertEqual(True, self.api.ctx.status)

        self.api.fetch_customer(email_or_id_or_customer_code='not@example.com')
        self.assertEqual(False, self.api.ctx.status)
        self.assertEqual(self.api.customer_id, '')
        self.assertEqual(self.api.customer_code, '')


class TestInvoice(TestCase):
    def setUp(self):
        self.api = Customer(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        self.api.create_customer(email='test@example.com')
        self.customer_code = self.api.customer_code

    def test_create_invoice(self):
        api = Invoice(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        api.create_invoice(customer=self.customer_code,
                           amount=500000, due_date='2020-12-20')

        self.assertEqual(self.api.ctx.status, True)

    def test_list_invoices(self):
        api = Invoice(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        api.list_invoices()

        self.assertEqual(api.ctx.status, True)


class TestTransferControl(TestCase):
    def test_balance(self):
        api = TransferControl(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        api.get_balance()

        self.assertEqual(api.ctx.status, True)
        self.assertEqual(api.ctx.message, 'Balances retrieved')


class TestPaymentPage(TestCase):
    def test_create_page(self):
        r = PaymentPage(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        slug = str(time.time())
        r.create_page(name='test page', slug=slug)

        self.assertEqual(r.ctx.status, True)
        self.assertEqual(r.ctx.message, 'Page created')
        self.assertEqual(r.name, 'test page')
        self.assertEqual(r.slug, slug)
        self.assertEqual(
            r.page_url, 'https://paystack.com/pay/{slug}'.format(slug=slug))


class TestTransaction(TestCase):
    def setUp(self):
        self.api = Transaction(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        custom_fields = [{'display_name':
                          'Cart ID',
                          'variable_name':
                          'cart_id',
                          'value': '8393'}]
        self.api.initialize_transaction(
            amount=30000, email='test@gmail.com', reference='sales90',
            invoice_limit=4, metadata={'custom_fields': custom_fields},
            transaction_charge=200, bearer='account', channels=['card'])
        self.transaction_reference = self.api.transaction_reference
        self.transaction_access_code = self.api.transaction_access_code

    def test_create_transaction(self):
        self.assertEqual(self.api.ctx.status, True)
        self.assertEqual(self.api.ctx.message, 'Authorization URL created')
        self.assertEqual(self.api.ctx.data['reference'],
                         'sales90')
        self.assertEqual(self.transaction_reference,
                         self.api.transaction_reference)
        self.assertEqual(self.transaction_access_code,
                         self.api.transaction_access_code)

    def test_verify_transaction(self):
        self.api.verify_transaction(reference='sales90')
        self.assertEqual(True, self.api.ctx.status)
        self.assertEqual(self.api.ctx.message, 'Verification successful')
        self.assertEqual(self.api.ctx.data['amount'], 3000000)
        self.assertEqual(self.api.ctx.data['currency'], 'NGN')
        self.assertEqual(self.api.ctx.data['status'], 'success')
        self.assertEqual(self.api.ctx.data['reference'], 'sales90')
        self.assertEqual(self.api.ctx.data['domain'], 'test')
        self.assertEqual(self.api.ctx.data['metadata'], '0')
        self.assertEqual(self.api.ctx.data['gateway_response'], 'Successful')
        self.assertEqual(self.api.ctx.data['message'], 'null')
        self.assertEqual(self.api.ctx.data['channel'], 'card')

    def test_list_transaction(self):
        self.api.list_transaction(perPage=10, page=2, customer=3765111,
                                  status='abandoned', from_='2018-09-27',
                                  to='2018-10-2', amount=3000000)
        self.assertEqual(self.api.ctx.status, True)
        self.assertEqual(self.api.ctx.message, 'Transactions retrieved')

    def test_fetch_transaction(self):
        self.api.fetch_transaction(transaction_id='54941338')
        self.assertEqual(True, self.api.ctx.status)
        self.assertEqual(self.api.ctx.message, 'Transaction retrieved')
        self.assertEqual(self.api.ctx.data['id'], 54941338)
        self.assertEqual(self.api.ctx.data['amount'], 3000000)
        self.assertEqual(self.api.ctx.data['currency'], 'NGN')
        self.assertEqual(self.api.ctx.data['status'], 'abandoned')
        self.assertEqual(self.api.ctx.data['reference'], 'sales155')
        self.assertEqual(self.api.ctx.data['domain'], 'test')
        self.assertEqual(self.api.ctx.data['gateway_response'],
                         'The transaction was not completed')
        self.assertEqual(self.api.ctx.data['message'], None)
        self.assertEqual(self.api.ctx.data['channel'], 'card')

    def test_view_transaction_timeline(self):
        self.api.view_transaction_timeline(transaction_id=54941338)
        self.assertEqual(True, self.api.ctx.status)
        self.assertEqual(self.api.ctx.message, 'Timeline retrieved')
        self.assertEqual(self.api.ctx.data, {})

    def test_transaction_total(self):
        self.api.transaction_total(from_='2018-09-27', to='2018-10-02')
        self.assertEqual(True, self.api.ctx.status)
        self.assertEqual(self.api.ctx.message, 'Transaction totals')
        self.assertEqual(self.api.ctx.data['total_transactions'], 0)
        self.assertEqual(self.api.ctx.data['total_volume'], 0)
        self.assertEqual(self.api.ctx.data['total_volume_by_currency']
                         [0]['currency'], 'NGN')
        self.assertEqual(self.api.ctx.data['total_volume_by_currency']
                         [0]['amount'], 0)
        self.assertEqual(self.api.ctx.data['pending_transfers'], 0)
        self.assertEqual(self.api.ctx.data['pending_transfers_by_currency']
                         [0]['currency'], 'NGN')
        self.assertEqual(self.api.ctx.data['pending_transfers_by_currency']
                         [0]['amount'], 0)


class TestRefund(TestCase):
    def setUp(self):
        self.api = Transaction(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        self.api.initialize_transaction(amount=30000, email='test@gmail.com')
        self.transaction_reference = self.api.transaction_reference

    def test_create_refund(self):
        api = Refund(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        api.create_refund(transaction=self.transaction_reference, amount=5000)
        self.assertEqual(self.api.ctx.status, True)


class TestFunctions(TestCase):
    def test_build_params(self):
        self.assertEqual(build_params(one=1, two=2), {'one': 1, 'two': 2})
        self.assertEqual(build_params(), {})
        self.assertEqual(build_params(a='a', b=None, c='b'),
                         {'a': 'a', 'c': 'b'})
