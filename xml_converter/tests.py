from pathlib import Path

from django.test import TestCase, Client


TEST_DIR = Path(__file__).parent / Path('test_files')


class XMLConversionAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": "",
            })

    def test_api_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": [
                    {
                        "Address": [
                            {"StreetLine1": "123 Main St."},
                            {"StreetLine2": "Suite 400"},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94103"},
                        ]
                    },
                    {
                        "Address": [
                            {"StreetLine1": "400 Market St."},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94108"},
                        ]
                    },
                ],
            })

    def test_api_convert_invalid_xml(self):
        with (TEST_DIR / Path('invalid.xml')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"error": "Invalid XML"})

    def test_api_convert_no_file(self):
        response = self.client.post('/api/converter/convert/', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "No file uploaded"})

    def test_api_convert_non_xml_file(self):
        with (TEST_DIR / Path('not_xml.txt')).open() as fp:
            response = self.client.post('/api/converter/convert/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"error": "Invalid XML"})


class XMLConversionPageTestCase(TestCase):
    def test_connected_convert_empty_document(self):
        with (TEST_DIR / Path('empty.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": "",
            })

    def test_connected_convert_addresses(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "Root": [
                    {
                        "Address": [
                            {"StreetLine1": "123 Main St."},
                            {"StreetLine2": "Suite 400"},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94103"},
                        ]
                    },
                    {
                        "Address": [
                            {"StreetLine1": "400 Market St."},
                            {"City": "San Francisco"},
                            {"State": "CA"},
                            {"PostCode": "94108"},
                        ]
                    },
                ],
            })

    def test_upload_successful_json_formatted(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
                'output_format': 'formatted',
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('text/html', response['Content-Type'])

    def test_upload_successful_json_plain(self):
        with (TEST_DIR / Path('addresses.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
                'output_format': 'plain',
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('application/json', response['Content-Type'])

    def test_upload_invalid_xml_file(self):
        with (TEST_DIR / Path('invalid.xml')).open() as fp:
            response = self.client.post('/connected/', {
                'file': fp,
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'error_page.html')

    def test_upload_without_file(self):
        response = self.client.post('/connected/', {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error_page.html')

    def test_access_upload_page(self):
        response = self.client.get('/connected/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_page.html')
