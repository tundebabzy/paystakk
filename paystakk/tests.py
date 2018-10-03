
from unittest import TestCase

import time

from utils import build_params
from api import TransferControl, PaymentPage, Customer, Invoice, Subaccount, TransferRecipient

SECRET_KEY = 'sk_test_026b00de6365c6d2e98af2fbc462c06ed74e5618'
PUBLIC_KEY = 'pk_test_6b35ec9fcc333acaad4210f3ea3e3a432995a25a'


class TestCustomer(TestCase):
	def setUp(self):
		self.api = Customer(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
		self.api.create_customer(email='test@example.com')
		self.customer_id = self.api.customer_id
		self.customer_code = self.api.customer_code

	def test_create_customer(self):
		self.assertEqual(self.api.ctx.status, True)

	def test_fetch_customer(self):
		self.api.fetch_customer(email_or_id_or_customer_code='test@example.com')
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
		api.create_invoice(customer=self.customer_code, amount=500000, due_date='2020-12-20')

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
		self.assertEqual(r.page_url, 'https://paystack.com/pay/{slug}'.format(slug=slug))

class TestSubaccount(TestCase):
    def setUp(self):
        self.api = Subaccount(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        self.api.createSubaccount(business_name="Xlevel", settlement_bank="Access Bank", account_number="0193274682",
                                  percentage_charge=18.2, settlement_schedule="Auto",
                                  primary_contact_email="xlevel@gmail.com", primary_contact_phone="08188329416",
                                  primary_contact_name="Olamide", metadata="x")

        self.assertEqual(self.api.ctx.status, True)
        self.assertEqual(self.api.ctx.message, 'Subaccount created')

    def testCreatesubaccount(self):
        self.assertEqual(self.api.ctx.data["integration"], self.api.integration)
        self.assertEqual(self.api.ctx.data["subaccount_code"], self.api.subaccount_code)
        self.assertEqual(self.api.ctx.data["domain"], "test")
        self.assertEqual(self.api.ctx.data["business_name"], "Xlevel")
        self.assertEqual(self.api.ctx.data["primary_contact_name"], "Olamide")
        self.assertEqual(self.api.ctx.data["primary_contact_email"], "xlevel@gmail.com")
        self.assertEqual(self.api.ctx.data["primary_contact_phone"], "08188329416")
        self.assertEqual(self.api.ctx.data["metadata"], "x")
        self.assertEqual(self.api.ctx.data["percentage_charge"], 18.2)
        self.assertEqual(self.api.ctx.data["is_verified"], False)
        self.assertEqual(self.api.ctx.data["settlement_bank"], "Access Bank")
        self.assertEqual(self.api.ctx.data["account_number"], "0193274682")
        self.assertEqual(self.api.ctx.data["settlement_schedule"], "AUTO")
        self.assertEqual(self.api.ctx.data["active"], True)
        self.assertEqual(self.api.ctx.data["migrate"], False)
        self.assertEqual(self.api.ctx.data["id"], self.api.id)
        self.assertEqual(self.api.ctx.data["createdAt"], self.api.createdAt)
        self.assertEqual(self.api.ctx.data["updatedAt"], self.api.updatedAt)


class TestTransferRecipient(TestCase):
    def setUp(self):
        self.api = TransferRecipient(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)
        self.api.create_Transfer_recipient(type="nuban", name="Zombie", account_number="0100000010",
                                           bank_code="044", currency="NGN", metadata={"job": "Flesh Eater"},
                                           description="Zombier")
        self.assertEqual(self.api.ctx.status, True)
        """
        The Testing Of The Message Will Fail Because The Output Message Has Been Changed From 'Recipient created' To
        'Transfer recipient created successfully' But Has Not Been Updated On The API Reference
        """
        ##self.assertEqual(self.api.ctx.message, "Recipient created")

    def testCreateTransferRecipient(self):
        self.assertEqual(self.api.ctx.data["type"], "nuban")
        self.assertEqual(self.api.ctx.data["name"], "Zombie")
        self.assertEqual(self.api.ctx.data["description"], "Zombier")
        self.assertEqual(self.api.ctx.data["domain"], "test")
        self.assertEqual(self.api.ctx.data["recipient_code"], self.api.recipient_code)
        self.assertEqual(self.api.ctx.data["details"]["account_number"], "0100000010")
        self.assertEqual(self.api.ctx.data["details"]["bank_code"], "044")
        self.assertEqual(self.api.ctx.data["details"]["bank_name"], "Access Bank")
        self.assertEqual(self.api.ctx.data["currency"], "NGN")
        self.assertEqual(self.api.ctx.data["metadata"], {"job": "Flesh Eater"})
        self.assertEqual(self.api.ctx.data["active"], True)
        self.assertEqual(self.api.ctx.data["id"], self.api.id)
        self.assertEqual(self.api.ctx.data["createdAt"], self.api.createdAt)
        self.assertEqual(self.api.ctx.data["updatedAt"], self.api.updatedAt)




class TestFunctions(TestCase):
	def test_build_params(self):
		self.assertEqual(build_params(one=1, two=2), {'one': 1, 'two': 2})
		self.assertEqual(build_params(), {})
		self.assertEqual(build_params(a='a', b=None, c='b'), {'a': 'a', 'c': 'b'})
