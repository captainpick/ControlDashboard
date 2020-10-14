from django.shortcuts import render
import os,subprocess,sys,subprocess
from django.http import HttpResponse
from .models import SoftSwitch,Service
from django.core import serializers
# Create your views here.
import json
import json

import ast


def MainDashboardPage(request):
    input_file = open ('config/json/service_names.json')
    json_array = json.load(input_file)
    input_file.close()

    return render(request,"Dashboard_Templates/index.html",json_array)




def MonitoringService(request,slug):
    if(slug=="ssw"):
       main=Service.objects.filter(Type="ssw")
       
    #    print(main.service_id)
    #    b=SoftSwitch(service_id=main)
    #    b.save()
       return render(request,"Dashboard_Templates/ServiceMonitoring.html",{"alldata":main})
    elif(slug=="sbc"):
        main=Service.objects.filter(Type="sbc")
       
    #    print(main.service_id)
    #    b=SoftSwitch(service_id=main)
    #    b.save()
        return render(request,"Dashboard_Templates/ServiceMonitoring.html",{"alldata":main})









def StartService(request):
    service=str(request.POST['data'])
    service=service.replace(".service","")
    os.system("service "+service+" start")
    # return HttpResponse(request.POST['Success'])

def StopService(request):
    service=str(request.POST['data'])
    service=service.replace(".service","")
    os.system("service "+service+" stop")
    # return HttpResponse(request.POST['data'])
