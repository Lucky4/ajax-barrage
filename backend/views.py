# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from backend.models import Barrage

import json

def index(request):
    return render(request, 'barrage.html')


@csrf_exempt # 禁止掉了csrf检查
def add_message(request):
    data = json.loads(request.body)['data']
    timestamp = json.loads(request.body)['timestamp']

    m = Barrage(data=data, timestamp=timestamp)
    m.save()

    message = json.dumps({
        'data': data,
        'timestamp': timestamp
    })

    return HttpResponse(message)


@csrf_exempt
def show_messages(request):
    curr_timestamp = json.loads(request.body)['timestamp']
    s = serializers.serialize("json", Barrage.objects.filter(timestamp=curr_timestamp), fields=('data'))

    return HttpResponse(s)
