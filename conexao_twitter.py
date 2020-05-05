import uuid


import tweepy
from mensagens import Mensagens


def publicar_tuites():

    auth = tweepy.OAuthHandler('VyzupUYulaeOR3xTZHcOF6bJ6', 'Y7fBjYGhpPpas1NMhg7RhsN56olZa6B5KCG1517L3jN9VPYfzl')
    auth.set_access_token('1252698169131110401-xRgChKOyA1DGI9e2qCx4R5nNcscUE1', 'JPqzIgSNLn19UMeHX6HNia7GsAUvPZThcraRaH2ElJInK')

    api = tweepy.API(auth)

    for msg in Mensagens().despesas_totais():
        status = api.update_status(msg)

    for msg in Mensagens().top_gastos():
        try:
            status_top_gastos = api.update_status(msg, id=str(uuid.uuid4()), in_reply_to_status_id=status_top_gastos.id)
        except UnboundLocalError:
            status_top_gastos = api.update_status(msg, id=str(uuid.uuid4()))

    for msg in Mensagens().top_gastos_credor():
        try:
            status_top_gastos_credor = api.update_status(msg, id=str(uuid.uuid4()), in_reply_to_status_id=status_top_gastos_credor.id)
        except UnboundLocalError:
            status_top_gastos_credor = api.update_status(msg, id=str(uuid.uuid4()))

    return None



