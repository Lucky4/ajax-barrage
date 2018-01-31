# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Barrage(models.Model):
    data = models.CharField(max_length=200)
    timestamp = models.IntegerField()