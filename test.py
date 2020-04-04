import unittest
import app
from unittest.mock import patch
from requests.exceptions import Timeout

class Responce:
    def __init__(self, status_code=200, text=''):
        self.status_code = status_code
        self.text = text

    def json(self):
        return {
            'text': [self.text,]
        }

class TranslateTest(unittest.TestCase):

    def setUp(self):
        self.data = {
            'hi': 'привет',
        }

    #@unittest.skip('')
    def test_real_translate(self):
        for in_data, out_data in self.data.items():
            self.assertDictEqual(
                app.translate(in_data), 
                {
                    'in': in_data,
                    'out': out_data
                })

    def test_timeout(self):
        with patch('app.requests.get', side_effect=Timeout):
            self.assertDictEqual(app.translate('hi'), {'error': 'Таймоут'})
    
    def test_status_codes(self):
        for code in app.CODES.keys():
            with patch('app.requests.get', return_value=Responce(code)):
                res = app.translate('hi')
                self.assertIn('error', res)

    def test_translate(self):
        for in_data, out_data in self.data.items():
            with patch('app.requests.get', return_value=Responce(200, out_data)):
                self.assertDictEqual(
                    app.translate(in_data),
                    {
                        'in': in_data,
                        'out': out_data
                    })



if __name__ == "__main__":
    unittest.main()
