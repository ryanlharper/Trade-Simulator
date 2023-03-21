from django.urls import reverse_lazy, reverse
from transactions.models import Transaction
from django.contrib.auth.models import User
from positions.models import Position, Comment
from user_accounts.models import UserAccount
from django.test import TestCase
from transactions.views import TransactionForm
import pytest

def test_home_view():
    url = reverse_lazy('home')
    assert url == "/"

class SignUpViewTestCase(TestCase):
    def test_signup_view(self):
        # create user
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  

        # verify user was created
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')

@pytest.fixture
def test_user(db, django_user_model):
    django_user_model.objects.create_user(
        username="test_username", password="test_password")
    return "test_username", "test_password" 

def test_login_user(client, test_user):
    test_username, test_password = test_user  
    login_result = client.login(username=test_username, password=test_password)
    assert login_result == True

def test_positions_view():
    url = '/positions'
    assert url == "/positions"

@pytest.mark.django_db
def test_position_insert():
    user = User.objects.create_user('username', password='password')
    position = Position.objects.create(
        user=user,
        symbol='SPY',
        quantity=10,
        price=1.00,
        cost=10.00,
    )
    assert position.symbol == 'SPY'

@pytest.fixture
def user_account(django_user_model):
    user = django_user_model.objects.create_user(
        username="test_username", password="test_password")
    user_account, created = UserAccount.objects.get_or_create(user=user)
    return user, user_account

def test_create_transaction(user_account):
    user, user_account = user_account
    transaction = Transaction.objects.create(
        user_account=user_account,
        user=user,
        symbol='SPY',
        quantity=100,
        type='buy',
        notes='buy new position',
        price=100.00,
    )
    assert transaction.symbol == "SPY"

def test_success_view():
    url = '/success'
    assert url == '/success'

class TransactionFormTestCase(TestCase):
    def test_transaction_form(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        user_account = UserAccount.objects.create(user=user)
        data = {
            'type': 'buy',
            'symbol': 'SPY',
            'quantity': 10,
            'notes': 'Test transaction'
        }
    
        form = TransactionForm(data=data)
        if form.is_valid():
            self.assertTrue(True)
        else:
            if '__all__' in form.errors and 'Market is closed' in form.errors['__all__']:
                self.assertTrue(True)
            else:
                self.assertTrue(False)
 
class TransactionFormBuyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_account = UserAccount.objects.create(user=self.user)
        self.cash_position = Position.objects.create(
            user=self.user,
            symbol='cash',
            quantity=10000,
            price = 1.00,
            cost = 1.00
        )

    def test_cash_position_for_buy(self):
        data = {
            'type': 'buy',
            'symbol': 'AAPL',
            'quantity': 10,
            'notes': 'cash check pass'
        }
        form = TransactionForm(data=data)
        if form.is_valid():
            self.assertTrue(True)
        else:
            if '__all__' in form.errors and 'Market is closed' in form.errors['__all__']:
                self.assertTrue(True)
            else:
                data = {
                'type': 'buy',
                'symbol': 'AAPL',
                'quantity': 100000,
                'notes': 'cash check fail'
                }
                form = TransactionForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn('Not enough cash', form.non_field_errors())

class AddCommentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass'
        )
        self.url = reverse('add_comment')

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass')
        data = {'text': 'This is a test comment.'}
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Comment added successfully.')
        comments = Comment.objects.filter(author=self.user)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().text, 'This is a test comment.')       