from urllib.parse import urlunparse
import requests
import xml.etree.ElementTree as xml
from zeep import Client as SOAPClient
import os
import base64

XMLNS = {
    'service_info': 'http://ws.gematik.de/conn/ServiceInformation/v2.0',
    'product': 'http://ws.gematik.de/int/version/ProductInformation/v1.1',
    'service_directory': 'http://ws.gematik.de/conn/ServiceDirectory/v3.1'
}

class Client(object):
    def __init__(self, host, port, use_tls, mandant_id, client_system_id, workplace_id):
        self.sds_url = urlunparse(('http', "{}:{}".format(host, port), 'connector.sds', None, None, None))
        self._services = {}
        self.context = {
            'MandantId': mandant_id,
            'ClientSystemId': client_system_id,
            'WorkplaceId': workplace_id
        }


    def __enter__(self):
        response = requests.get(self.sds_url)
        directory = xml.fromstring(response.text)
        for service_info in directory.findall('.//service_info:Service', XMLNS):
            service_name = service_info.attrib['Name']
            if not service_name in self._services:
                self._services[service_name] = {}
            for version_info in service_info.findall('.//service_info:Version', XMLNS):
                service_version = version_info.attrib['Version'];
                # TODO: Make findinf WSDL files more 'clever'
                soap_client = SOAPClient(os.path.join(os.path.dirname(os.path.join(os.path.realpath(__file__))), '../resources/wsdl/r2.1.1/conn/{}.wsdl'.format(service_name)))
                self._services[service_name][service_version] = {
                    'name': service_name,
                    'version': service_version,
                    'endpoint_url': version_info.find('service_info:Endpoint', XMLNS).attrib['Location'],
                    'soap_client': soap_client
                }

        return self

    def __exit__(self, type, value, traceback):
        if traceback != None:
            return False
        return True

    def services_info(self):
        return self._services

    def get_cards(self):
        service_info = self._services['EventService']['7.2.0']
        service = service_info['soap_client'].create_service(
            '{http://ws.gematik.de/conn/EventService/WSDL/v7.2}EventServiceBinding',
            service_info['endpoint_url'])

        response = service.GetCards(
            Context=self.context
        )

        return response.Cards.Card

    def get_cards(self):
        service_info = self._services['EventService']['7.2.0']
        service = service_info['soap_client'].create_service(
            '{http://ws.gematik.de/conn/EventService/WSDL/v7.2}EventServiceBinding',
            service_info['endpoint_url'])

        response = service.GetCards(
            Context=self.context
        )

        return response.Cards.Card

    def verify_pin(self, card_handle, pin_type):
        service_info = self._services['CardService']['8.1.2']
        service = service_info['soap_client'].create_service(
            '{http://ws.gematik.de/conn/CardService/WSDL/v8.1}CardServiceBinding',
            service_info['endpoint_url'])

        response = service.VerifyPin(
            CardHandle=card_handle,
            Context=self.context,
            PinTyp=pin_type.value
        )

        return response

    def external_authenticate(self, card_handle, data_to_sign):
        service_info = self._services['AuthSignatureService']['7.4.0']
        service = service_info['soap_client'].create_service(
            '{http://ws.gematik.de/conn/AuthSignatureService/WSDL/v7.4}AuthSignatureServiceBinding',
            service_info['endpoint_url'])

        response = service.ExternalAuthenticate(
            CardHandle=card_handle,
            Context=self.context,
            OptionalInputs={
                'SignatureType': 'urn:ietf:rfc:3447',
                'SignatureSchemes': 'RSASSA-PKCS1-v1_5'
            },
            BinaryString={
                'Base64Data':base64.b64encode(data_to_sign)
            }
        )

        return response.SignatureObject.Base64Signature._value_1
