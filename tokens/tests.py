from datetime import timedelta

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from . import register, clear_handlers
from .models import Token


class TokenModelTest(TestCase):
    def testCreation(self):
        obj = Token.objects.create('foo', {'eggs': 'spam'},
            timedelta(days=1))
        obj.save()
        unicode(obj)


class TokenViewTest(TestCase):
    urls = 'tokens.urls'

    def testView(self):
        obj = Token.objects.create('foo', {'eggs': 'spam'})
        obj.save()

        url = reverse('token_handle', args=[obj.full_code])

        called = [False]

        @register('foo')
        def callback(token):
            self.assertEqual(obj.id, token.id)
            self.assertEqual(obj.token_type, token.token_type)
            self.assertEqual(obj.data, token.data)
            called[0] = True
            return HttpResponse('')

        client = Client()
        response = client.get(url)

        self.assertTrue(called[0])

    def tearDown(self):
        clear_handlers()
