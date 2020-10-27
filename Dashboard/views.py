import ast
# Create your views here.
import json
import os
import subprocess
import sys
import requests
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from .models import Server,SSWConfig,SBCConfig,SSW,SBC


def MainDashboardPage(request):
    input_file = open ('config/json/rules.json')
    json_array = json.load(input_file)
    input_file.close()

    return render(request,"Dashboard_Templates/dash_base.html",json_array)




def MonitoringServer(request,slug):
    # try : 
        if(slug=="all-service"):
            main=Server.objects.all()
            input_file = open ('config/json/rules.json')
            json_array = json.load(input_file)
            input_file.close()
            status={}
            for server in main:
                data={'name':server.server_id,'type':server.Type}
                r=requests.post(url="http://127.0.0.1:5000/test",json=data)
                status[server.name]=r.text
            
            
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"all","all":json_array,'status':status})


        elif(slug=="ssw"):
            status={}
            main=Server.objects.filter(Type="ssw")
            # input_file = open ('config/json/rules.json')
            # json_array = json.load(input_file)
            # input_file.close()
            
            for server in main:
                data={'name':server.server_id,'type':server.Type}
                r=requests.post(url="http://127.0.0.1:5000/test",json=data)
                status[server.name]=r.text
    
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"ssw",'status':status})
            

        elif(slug=="sbc"):
            status={}
            main=Server.objects.filter(Type="sbc")
            for server in main:
                data={'name':server.server_id,'type':server.Type}
                r=requests.post(url="http://127.0.0.1:5000/test",json=data)
                status[server.name]=r.text
            return render(request,"Dashboard_Templates/datatable.html",{"alldata":main,"type":"sbc",'status':status})


        else:
            return render(request,"Dashboard_Templates/404.html")
    # except:
    #     return HttpResponse("error")





def AddServer(request):
    try:
        if(request.POST['type']=="ssw"):
            Type=str(request.POST['type'])
            name=str(request.POST['name'])
            ip=str(request.POST['ip'])
            server_object=Server(name=name,Type=Type,ip=ip)
            server_object.save()
            ssw_object=SSW(server_id=server_object)
            ssw_object.save()


            return HttpResponse("ok")

        elif(request.POST['type']=="sbc"):
            
            Type=str(request.POST['type'])
            
            name=str(request.POST['name'])
            ip=str(request.POST['ip'])
            server_object=Server(name=name,Type=Type,ip=ip)
            server_object.save()
            sbc_object=SBC(server_id=server_object)
            sbc_object.save()


            return HttpResponse("ok")
        
    except:
        return HttpResponse("error")




def EditServer(request):
    try:
        server_id=request.POST['id']    
        new_name=request.POST['new_name']
        new_ip=request.POST['new_ip']

        edit_model = Server.objects.get(pk=server_id)
        edit_model.name=new_name
        edit_model.ip=new_ip
        edit_model.save()
        main=Server.objects.filter(Type="ssw")
        return HttpResponse("ok")
    except:
        return HttpResponse("error")



def DeleteServer(request):
    
    try:
        server_id=request.POST['id']
        delete_model = Server.objects.filter(pk=server_id).delete()
        return HttpResponse("ok")
    except:
        return HttpResponse("error")





