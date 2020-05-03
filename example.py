import telematik.api.konnektor as konnektor_api
import string
import binascii


with konnektor_api.connect(host='localhost',
    port=8080,
    use_tls=False,
    mandant_id='MandantId',
    client_system_id='ClientSystemId',
    workplace_id='WorkplaceId') as kon:

    print (kon.services_info())

    cards = kon.get_cards()
    for card in cards:
        print('Found Card: card_type: {}, card_handle: {}'.format(card.CardType, card.CardHandle))

    card = cards[0]

    verify_pin_result = kon.verify_pin(card.CardHandle, konnektor_api.PinType.PIN_SMC)
    print (verify_pin_result)


    # 512 Bits
    challenge=bytearray((string.ascii_letters + string.hexdigits)[0:64], 'UTF-8')
    print ('Signing {} with card {}'.format(binascii.hexlify(challenge), card.CardHandle))
    signed_data = kon.external_authenticate(card.CardHandle, challenge)
    print ('Got signed result: {}'.format(binascii.hexlify(signed_data)) )

    # 384 Bits
    #challenge=bytearray((string.ascii_letters + string.hexdigits)[0:32], 'UTF-8')
    #print ('Signing {} with card {}'.format(binascii.hexlify(challenge), card.CardHandle))
    #signed_data = kon.external_authenticate(card.CardHandle, challenge)
    #print ('Got signed result: {}'.format(binascii.hexlify(signed_data)) )

    # 256 Bits
    #challenge=bytearray((string.ascii_letters + string.hexdigits)[0:32], 'UTF-8')
    #print ('Signing {} with card {}'.format(binascii.hexlify(challenge), card.CardHandle))
    #signed_data = kon.external_authenticate(card.CardHandle, challenge)
    #print ('Got signed result: {}'.format(binascii.hexlify(signed_data)) )
