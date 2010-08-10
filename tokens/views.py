from django.shortcuts import get_object_or_404

from . import handlers
from .models import Token

def handle_token(request, token):
    token_id, token_code = token.split('-')
    token = get_object_or_404(Token, id=token_id, code=token_code)
    try:
        handler = handlers[token.token_type]
    except KeyError:
        token.delete()
        return HttpResponseRedirect('/')
    return handler(token)

