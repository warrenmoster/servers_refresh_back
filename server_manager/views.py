import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import Server
# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")

def server_list(request):
    if request.method == 'GET':
        servers = Server.objects.all().values('server_name', 'ip_address', 'location',  'is_monitored',
                                              'health_monitored', 'passwordless')
        data = {'servers': list(servers)}
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request Method'})
@csrf_exempt
def add_server(request):
    if request.method =='POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        server_name = body_data.get('server_name')
        ip_address = body_data.get('ip_address')
        password = body_data.get('password')
        is_monitored = body_data.get('is_monitored')
        passwordless = body_data.get('passwordless')
        location = body_data.get('location')
        health_monitored = body_data.get('health_monitored')

        # Check if server with the given server_name already exists
        existing_server = Server.objects.filter(server_name=server_name).first()
        if existing_server:
            # If server exists, update the fields and save the record
            existing_server.ip_address = ip_address
            existing_server.password = password
            existing_server.is_monitored = is_monitored
            existing_server.passwordless = passwordless
            existing_server.location = location
            existing_server.health_monitored = health_monitored
            existing_server.save()
        else:
            new_server = Server(server_name=server_name, ip_address=ip_address, 
                                password=password, is_monitored=is_monitored,
                                passwordless=passwordless, location=location, health_monitored=health_monitored)
            new_server.save()
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request Method'})
    
@csrf_exempt
def delete_server(request):
    if request.method == 'DELETE':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print(body_data)

        server_name = body_data.get('server_name')
        Server.objects.filter(server_name=server_name).delete()
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request Method'})
    
def get_csrf_token(request):
    print(request)
    token = get_token(request)
    data = {
        "csrf_token" : token
    }
    return JsonResponse(data)