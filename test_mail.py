import pytest
from flask_testing import TestCase
from app import app as flask_app
from unittest.mock import patch
from flask_mail import Message

class TestMailFunctionality(TestCase):  # Cambié el nombre de la clase para seguir la convención
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app

    @patch('routes.mail.send')  # Asegúrate de que el patch apunte a la ubicación correcta
    def test_send_email(self, mock_mail_send):  # El nombre del método comienza con 'test_'
        with self.client:
            response = self.client.post('/send_email', json={
                'email': 'test@example.com',
                'subject': 'Test Subject',
                'content': 'Test Content'
            })

            assert response.status_code == 200
            mock_mail_send.assert_called_once()
            args, kwargs = mock_mail_send.call_args
            message: Message = args[0]
            assert message.recipients == ['test@example.com']
            assert message.subject == 'Test Subject'
            assert message.body == 'Test Content'

