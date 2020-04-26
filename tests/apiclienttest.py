import unittest
from src.apiclient import ApiClient

class ApiClientTest(unittest.TestCase):
    def test_apiclient(self):
        client = ApiClient().apiclient()
        self.assertEqual(type(client), "<class 'kubernetes.client.api_client.ApiClient'>")

if __name__ == '__main__':
    unittest.main()
