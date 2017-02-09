from __future__ import division
from django.shortcuts import render, redirect
from django.db.models import Count
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.http import Http404
from django.contrib.auth.models import User
from .models import Model, CalibrationHistory, CurrentCalibration, CalibrationResult, UserModel, Node, Devices
from .models import CalibrationData
from .form import UserModelDescriptionForm
from . import calibration
from . import upmu
# from redis import Redis
import pdb
import datetime

# redis = Redis(host='redis', port=6379)
