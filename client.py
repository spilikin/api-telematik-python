from zeep import Client
import string
import base64

challenge=(string.letters + string.hexdigits)[0:63]

client = Client('./wsdl/r1.6.4/conn/AuthSignatureService.wsdl')
#client = Client('http://localhost:8080/soap-api/AuthSignatureService/7.4?wsdl')

service = client.create_service(
    '{http://ws.gematik.de/conn/AuthSignatureService/WSDL/v7.4}AuthSignatureServiceBinding',
    'http://localhost:8080/soap-api/AuthSignatureService/7.4')

response = service.ExternalAuthenticate(
    CardHandle='unknown card handle',
    Context={
        'MandantId': 'unknown MandantId',
        'ClientSystemId': 'unknown ClientSystemId',
        'WorkplaceId': 'unknown WorkplaceId',
    },
    OptionalInputs={},
    BinaryString={
        'Base64Data':base64.b64encode(challenge)
    }
)

print response.SignatureObject.Base64Signature._value_1