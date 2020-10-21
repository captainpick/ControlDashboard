import ast
# Create your views here.
import json
import os
import subprocess
import sys

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Service, SoftSwitch , SBC


def MainDashboardPage(request):
    input_file = open ('config/json/service_names.json')
    json_array = json.load(input_file)
    input_file.close()

    return render(request,"Dashboard_Templates/dash_base.html",json_array)




def MonitoringService(request,slug):
    try : 
        if(slug=="all-service"):
            main=Service.objects.all()
            input_file = open ('config/json/service_names.json')
            json_array = json.load(input_file)
            input_file.close()
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"all","all":json_array})


        elif(slug=="ssw"):
            main=Service.objects.filter(Type="ssw")
            input_file = open ('config/json/service_names.json')
            json_array = json.load(input_file)
            input_file.close()
    
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"ssw"})
            

        elif(slug=="sbc"):
            main=Service.objects.filter(Type="sbc")
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"sbc"})
        else:
            return render(request,"Dashboard_Templates/404.html")
    except:
        return HttpResponse("error")





def AddService(request):
    try:
        if(request.POST['type']=="ssw"):
            Type=str(request.POST['type'])
            name=str(request.POST['name'])
            ip=str(request.POST['ip'])
            service_object=Service(name=name,Type=Type,ip=ip)
            service_object.save()
            ssw_object=SoftSwitch(service_id=service_object)
            ssw_object.save()


            return HttpResponse("ok")

        elif(request.POST['type']=="sbc"):
            
            Type=str(request.POST['type'])
            name=str(request.POST['name'])
            ip=str(request.POST['ip'])
            service_object=Service(name=name,Type=Type,ip=ip)
            service_object.save()
            sbc_object=SBC(service_id=service_object)
            sbc_object.save()
            return HttpResponse("ok")
        
    except:
        return HttpResponse("error")




def EditService(request):
    try:
        serivce_id=request.POST['id']    
        new_name=request.POST['new_name']
        new_ip=request.POST['new_ip']

        edit_model = Service.objects.get(pk=serivce_id)
        edit_model.name=new_name
        edit_model.ip=new_ip
        edit_model.save()
        main=Service.objects.filter(Type="ssw")
        return HttpResponse("ok")
    except:
        return HttpResponse("error")



def DeleteService(request):
    
    try:
        serivce_id=request.POST['id']
        delete_model = Service.objects.filter(pk=serivce_id).delete()
        return HttpResponse("ok")
    except:
        return HttpResponse("error")





