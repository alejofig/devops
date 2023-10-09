import unittest
import json
from app import app, db
from app.models import Cliente
from datetime import datetime
import os

STATIC_TOKEN = os.getenv("STATIC_TOKEN") 

class TestClienteEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def get_auth_headers(self):
        return {'Authorization': f'Bearer {STATIC_TOKEN}'}

    def test_agregar_cliente(self):
        data = {
            'email': 'test@example.com',
            'app_uuid': 'test_uuid'
        }
        headers = self.get_auth_headers()
        response = self.client.post('/blacklists/', json=data, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'Cliente creado correctamente')

    def test_obtener_cliente_por_email(self):
        cliente = Cliente(email='test@example.com',
                           app_uuid='test_uuid',
                           blocked_reason="fraude",
                           datetime_request=datetime.now(),
                            ip_request="172.1.2.1")
        db.session.add(cliente)
        db.session.commit()
        headers = self.get_auth_headers()
        response = self.client.get('/blacklists/test@example.com', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['is_blacklisted'], True)

    def test_obtener_cliente_inexistente_por_email(self):
        headers = self.get_auth_headers()
        response = self.client.get('/blacklists/nonexistent@example.com', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['is_blacklisted'], False)

if __name__ == '__main__':
    unittest.main()
