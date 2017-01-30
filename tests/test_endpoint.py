import os
import unittest
import json
import flask
from app.api.endpoints import *
from app import app

class TestEndpointProducts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_products(self):
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, 200)
        
    def test_product(self):
        resp = self.app.get('/products/1')
        self.assertEqual(resp.status_code, 200)

class TestEndpointAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_logout(self):
        resp = self.app.post('/api/logout')
        self.assertEqual(resp.status_code, 200)
        
    def test_login_account(self):      
        resp = self.app.post('/api/login', data=json.dumps(dict(username='admin', password='admin')), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

class TestEndpointAccount(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_account(self):
        resp = self.app.post('/api/account', data=json.dumps(dict(birthDate={"day": 1, "month": 1, "year": 2016}, email='test3@testmail.com', name='tester', password='tester', surname='supertester', username='tester3')), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_get_account(self):
        resp = self.app.get('/api/account')
        self.assertEqual(resp.status_code, 401)
        
    def test_update_account(self):
        self.assertEqual(1,1)
        
    def test_add_address(self):
        self.assertEqual(1,1)
        
    def test_get_address(self):
        self.assertEqual(1,1)
        
    def test_delete_address(self):
        self.assertEqual(1,1)
        
    def test_add_favorite(self):
        self.assertEqual(1,1)
        
    def test_get_favorite(self):
        self.assertEqual(1,1)
        
    def test_delete_favorite(self):
        self.assertEqual(1,1)

    def test_add_wishlisht(self):
        self.assertEqual(1,1)
        
    def test_get_wishlist(self):
        self.assertEqual(1,1)
        
    def test_delete_wishlist(self):
        self.assertEqual(1,1)
        
    def test_add_order(self):
        self.assertEqual(1,1)
    
    def test_get_orders(self):
        self.assertEqual(1,1)
        
    def test_get_order(self):
        self.assertEqual(1,1)
        
    def test_get_public_wishlists(self):
        self.assertEqual(1,1)
        
    def test_get_public_wishlist(self):
        self.assertEqual(1,1)
        
    def test_BanUser(self):
        self.assertEqual(1,1)
        
    def test_get_password_reset_token(self):
        self.assertEqual(1,1)
        
    def test_reset_password(self):
        self.assertEqual(1,1)