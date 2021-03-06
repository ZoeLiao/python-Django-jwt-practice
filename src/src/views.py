import arrow
import json
import jwt

from django.contrib.auth import authenticate
from django.core import serializers
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    if phone is None or password is None:
        return Response({'error': 'Please provide both phone and password'},
                        status=HTTP_400_BAD_REQUEST)

    # TODO: replace with models
    if phone == settings.DEFAULT_PHONE and password == settings.DEFAULT_PASSWORD:
        payload = {
            'phone': phone,
            'iat': arrow.now().timestamp,
            'exp': arrow.now().shift(minutes=5).timestamp
        }
        jwt_token = jwt.encode(payload, settings.SECRET, algorithm='HS256').decode('utf-8')
        request.session['jwt_token'] = jwt_token
        return JsonResponse(jwt_token, safe=False)

    else:
        return Response(
            json.dumps({'Error': 'Invalid credentials'}),
            status=400,
            content_type='application/json'
        )


@csrf_exempt
@api_view(['GET'])
def test_api(request):
    # TODO: import from auth @login_required
    if not request.session.get('jwt_token'):
        return Response(
            json.dumps({'Error': 'Invalid credentials'}),
            status=400,
            content_type='application/json'
        )

    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token':
        return Response(
            json.dumps({'Error': 'Invalid credentials'}),
            status=400,
            content_type='application/json'
        )

    encoded_token = auth[1]
    token = jwt.decode(encoded_token, settings.SECRET, algorithms=['HS256'])
    # TODO: replace with models
    if token.get('phone') == settings.DEFAULT_PHONE: 
        if arrow.get(token.get('exp')) >= arrow.now():
            return Response(
                {'msg': 'Log in with jwt successfully.'},
                status=HTTP_200_OK
            )

    return Response(
        json.dumps({'Error': 'Invalid user'}),
        status=401,
        content_type='application/json'
    )


@csrf_exempt
@api_view(['GET'])
def logout(request):
    jwt_token = request.session.get('jwt_token')
    if not jwt_token:
        return Response(
            json.dumps({'Error': 'Invalid user'}),
            status=401,
            content_type='application/json'
        )

    del request.session['jwt_token']
    return Response(
        {'msg': 'Log out successfully.'},
        status=HTTP_200_OK
    )
