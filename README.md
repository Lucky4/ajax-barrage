# A simple ajax example called barrage

一个简答的ajax应用，实现一下功能：
- [x] 提交评论请求后，后台保存评论信息以及视频运行到的时间，响应返回评论信息并显示在屏幕上
- [x] 视频播放后，定时发送ajax请求，获得当前播放时间的弹幕，将响应信息显示在屏幕上

## 效果
![效果](https://github.com/lucky4/barrage/raw/master/screenshot/1.gif)

## 主要代码

barrage.js
~~~js
(function() {
  init();

  var xhr = null;
  var timestamp = 0;

  var inputElem;
  var submitElem;
  var videoElem;
  var showContainer;
  inputElem = document.getElementById('input');
  submitElem = document.getElementById('submit');
  videoElem = document.getElementById('video');
  showContainer = document.getElementById('show-container');

  submitElem.addEventListener('click', handleComment);
  function handleComment() {
    var message;
    var input;

    if (window.XMLHttpRequest) {
      xhr = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
      xhr = new ActiveXObject();
    }

    if (!xhr) {
      console.log('XMLHttpRequest create failed.')
    }

    input = inputElem.value;
    inputElem.value = '';
    if (input === '') {
      return false;
    }

    timestamp = videoElem.currentTime;
    message = JSON.stringify({
      'data': input,
      'timestamp': timestamp
    });

    xhr.onreadystatechange = showMsg;
    xhr.open('POST', 'http://127.0.0.1:8000/backend/add_message/', true);
    xhr.setRequestHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:8000');
    xhr.setRequestHeader('Content-Type', 'text/plain');
    xhr.send(message);
  }

  function showMsg() {
    var tmpData;
    var tmpTimestamp;
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        tmpTimestamp = JSON.parse(xhr.responseText).timestamp;
        tmpData = JSON.parse(xhr.responseText).data;
        if (!videoElem.paused) {
          move(tmpData);
        }
      }
    }
  }

  function move(data) {
    var dataElem = document.createElement('div');
    var dataText = document.createTextNode(data);
    dataElem.style.color = '#000';
    dataElem.appendChild(dataText);

    var videoHeight = showContainer.clientHeight;
    var videoWidth = showContainer.clientWidth;
    var startHeight = Math.floor(Math.random() * videoHeight) - 100; // 防止超出范围
    var startWidth = videoWidth - dataElem.clientWidth - 100;
    dataElem.style.position = 'absolute';
    dataElem.style.top = startHeight + 'px';
    dataElem.style.left = startWidth + 'px';

    var bodyElem = document.getElementsByTagName('body')[0];
    bodyElem.appendChild(dataElem);
    var currWidth = startWidth;
    var action = function() {
      setTimeout(function () {
        if (currWidth === 0) {
          bodyElem.removeChild(dataElem);
          return;
        }
        currWidth = currWidth - 2;
        dataElem.style.left = currWidth + 'px';
        action();
      }, 8);
    }
    action();
  }

  function init() {
    var currTimestamp;
    var showHistory = function() {
      setTimeout(function() {
        if (videoElem.paused) {
          return;
        }

        if (window.XMLHttpRequest) {
          xhr = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
          xhr = new ActiveXObject();
        }

        if (!xhr) {
          console.log('XMLHttpRequest create failed.')
        }

        currTimestamp = JSON.stringify({
          'timestamp': videoElem.currentTime
        });

        xhr.onreadystatechange = showMsgs;
        xhr.open('POST', 'http://127.0.0.1:8000/backend/show_messages/', true);
        xhr.setRequestHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:8000');
        xhr.setRequestHeader('Content-Type', 'text/plain');
        xhr.send(currTimestamp);

        showHistory();
      }, 1000);
    }
    showHistory();
  }

  function showMsgs() {
    var currData;
    var messages;
    var item;
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        messages = JSON.parse(xhr.responseText);
        for (item in messages) {
          currData = messages[item].fields.data;
          move(currData);
        }
      }
    }
  }

})();
~~~

backend.py
~~~py
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
~~~
