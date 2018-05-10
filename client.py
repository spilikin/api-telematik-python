from zeep import Client
from zeep.exceptions import Fault
import string
import base64
import requests
import binascii
import telematik.conn.api as connapi
from pprint import pprint

challenge=(string.letters + string.hexdigits)[0:64]

client = Client('./wsdl/r1.6.4/conn/AuthSignatureService.wsdl')
#client = Client('http://localhost:8080/soap-api/AuthSignatureService/7.4?wsdl')

service = client.create_service(
    '{http://ws.gematik.de/conn/AuthSignatureService/WSDL/v7.4}AuthSignatureServiceBinding',
    'http://localhost:9095/soap-api/AuthSignatureService/7.4.0')

try:
    response = service.ExternalAuthenticate(
        CardHandle='smc-b_1',
        Context={
            'MandantId': 'unknown MandantId',
            'ClientSystemId': 'unknown ClientSystemId',
            'WorkplaceId': 'unknown WorkplaceId',
        },
        OptionalInputs={
            'SignatureType': 'urn:ietf:rfc:3447',
            'SignatureSchemes': 'RSASSA-PKCS1-v1_5'
        },
        BinaryString={
            'Base64Data':base64.b64encode(challenge)
        }
    )
    result = base64.b64decode(response.SignatureObject.Base64Signature._value_1)
    print ( binascii.hexlify(result) )
except Fault as error:
    print ("Error: {} ".format(error.message) )
