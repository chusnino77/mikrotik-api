from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .routeros_api import Api
from .models import RouterList
from django.template.loader import render_to_string
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
def loginRequest(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('dashboard_mikrotik')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
                request = request,
                template_name = "login_form.html",
                context={"form":form}
            )
    # return render(request, 'login_form.html')
    
@login_required(login_url='/')
def logoutRequest(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login_mikrotik")

def test(request):
    connect = Api('172.16.7.2',user='admin',password='rb450g')
    ping = connect.talk('/ping \n=address=1.1.1.4\n=count=10')
    return JsonResponse(ping,safe=False)

@login_required(login_url='/')
def dashboard(request):
    routers = RouterList.objects.all()
    bg_color = ['bg-info','bg-warning','bg-success','bg-danger']
    return render(request, 'dashboard.html', {'routers':routers,'bg_color':bg_color})
@login_required(login_url='/')
def testConnection(request):
    router = request.GET
    connect = Api(request.GET.get('ip_address'), user=request.GET.get('username'), password=request.GET.get('password'))
    router = connect.talk('/system/routerboard/print')
    identity = connect.talk('/system/identity/print')
    return JsonResponse({'router':router,'identity':identity}, safe=False)

def routerCreate(request):
    if request.method == 'POST':
        form = RouterForm(request.POST)
    else:
        form = RouterForm()
    return routerSave(request, form, 'router/create.html')

@login_required(login_url='/')
def routerSave(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routers = RouterList.objects.all()
            data['html_router_list'] = render_to_string('router/list.html', {
                'routers': routers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/')
def routerUpdate(request, pk):
    router = get_object_or_404(RouterList, pk=pk)
    if request.method == 'POST':
        form = RouterForm(request.POST, instance=router)
    else:
        form = RouterForm(instance=router)
    return routerSave(request, form, 'router/update.html')

@login_required(login_url='/')
def routerDelete(request, pk):
    router = get_object_or_404(RouterList, pk=pk)
    data = dict()
    if request.method == 'POST':
        router.delete()
        data['form_is_valid'] = True
        routers = RouterList.objects.all()
        data['html_router_list'] = render_to_string('router/list.html', {
            'routers': routers
        })
    else:
        context = {'router': router}
        data['html_form'] = render_to_string('router/delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/')  
def homePage(request,pk):
    router = get_object_or_404(RouterList, pk=pk)
    request.session['id']     = router.id
    request.session['ip_address'] = router.ip_address
    request.session['username']   = router.username
    request.session['password']   = router.password
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/secret/print')
    active = connect.talk('/ppp/active/print')
    clients = []
    for row in client:
        clients.append({'name':row['name'],'service':row['service']})
    actives =  []
    for row in active:
        actives.append({'name':row['name'],'service':row['service']})

    diff = [item for item in clients if item not in actives]
    return render(request, 'homepage.html',{'router':router,'active':active, 'diff':diff,'list_client':client})

@login_required(login_url='/')
def clientList(request):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/secret/print')
    active = connect.talk('/ppp/active/print')
    clients = []
    for row in client:
        clients.append({'name':row['name'],'service':row['service']})
    actives =  []
    for row in active:
        actives.append({'name':row['name'],'service':row['service']})
    diff = [item for item in clients if item not in actives]
    clients = []
    for row in client:
        clients.append({'id':row['.id'],'name':row['name'],'service':row['service'],'profile':row['profile'],'disabled':row['disabled']})
    activ =  []
    for row in active:
        activ.append({'id':row['.id'],'name':row['name'],'service':row['service'],'address':row['address']})
    return render(request, 'client_list.html',{'client': clients, 'active':activ, 'diff':diff, 'router':{'id':request.session.get('id')}})

@login_required(login_url='/')
def clientCreate(request):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    profiles = connect.talk('/ppp/profile/print')
    data = dict()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        form.fields['profile'].choices = [(profile['.id'], profile['name']) for profile in profiles]
        if form.is_valid():
            form_data = form.cleaned_data
            name      = form_data['name']
            password  = form_data['password']
            service   = form_data['service']
            profile   = form_data['profile']
            connect   = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
            command   = "/ppp/secret/add \n=name="+name+"\n=password="+password+"\n=service="+service+"\n=profile="+profile
            save_data = connect.talk(command)
            data['form_is_valid'] = True
            client = connect.talk('/ppp/secret/print')
            clients = []
            for row in client:
                clients.append({'id':row['.id'],'name':row['name'],'service':row['service'],'profile':row['profile'],'disabled':row['disabled']})
            data['html_client_list'] = render_to_string('client/list.html', {
                'client': clients
            })
        else:
            data['form_is_valid'] = False
    else:
        form = ClientForm()
        form.fields['profile'].choices = [(profile['.id'], profile['name']) for profile in profiles]
   
    data['html_form'] = render_to_string('client/create.html', {'form': form}, request=request)
    return JsonResponse(data)

@login_required(login_url='/')
def clientDelete(request, pk):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/secret/print \n?.id='+pk)
    data = dict()
    if request.method == 'POST':
        data['form_is_valid'] = True
        client = connect.talk('/ppp/secret/remove \n=.id='+pk)
        client = connect.talk('/ppp/secret/print')
        clients = []
        for row in client:
            clients.append({'id':row['.id'],'name':row['name'],'service':row['service'],'profile':row['profile'],'disabled':row['disabled']})
        data['html_client_list'] = render_to_string('client/list.html', {
            'client': clients
        })
    else:
        context = {'client': {'id':client[0]['.id'],'name':client[0]['name']}}
        data['html_form'] = render_to_string('client/delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/')
def clientUpdate(request, pk):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/secret/print \n?.id='+pk)
    profiles = connect.talk('/ppp/profile/print')
    data = dict()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        form.fields['profile'].choices = [(profile['.id'], profile['name']) for profile in profiles]
        if form.is_valid():
            name      = form['name'].value()
            password  = form['password'].value()
            service   = form['service'].value()
            profile   = form['profile'].value()
            connect   = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
            command   = "/ppp/secret/set \n=.id="+pk+"\n=name="+name+"\n=password="+password+"\n=service="+service+"\n=profile="+profile
            save_data = connect.talk(command)
            data['form_is_valid'] = True
            client = connect.talk('/ppp/secret/print')
            clients = []
            for row in client:
                clients.append({'id':row['.id'],'name':row['name'],'service':row['service'],'profile':row['profile'],'disabled':row['disabled']})
            data['html_client_list'] = render_to_string('client/list.html', {
                'client': clients
            })
        else:
            data['form_is_valid'] = False
    else:
        profiles = connect.talk('/ppp/profile/print')
        profil_id = ''
        for row in profiles:
            if row['name'] == client[0]['profile']:
                profil_id = row['.id']
        form = ClientForm()
        form.fields['name'].initial     = client[0]['name']
        form.fields['password'].initial = client[0]['password']
        form.fields['service'].initial  = client[0]['service']
        form.fields['profile'].choices  = [(profile['.id'], profile['name']) for profile in profiles]
        form.fields['profile'].initial  = profil_id
        data['html_form'] = render_to_string('client/update.html', {'form': form}, request=request)
        data['client'] = {'id':client[0]['.id']}
    return JsonResponse(data)

@login_required(login_url='/')
def clientEnable(request, pk):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/secret/print \n?.id='+pk)
    data = dict()
    if request.method == 'POST':
        data['form_is_valid'] = True
        form = request.POST
        print(form['state'])
        state = 'no'
        if(form['state'] == 'false'): state = 'yes'
        client = connect.talk('/ppp/secret/set \n=.id='+pk+'\n=disabled='+state)
        client = connect.talk('/ppp/secret/print')
        clients = []
        for row in client:
            clients.append({'id':row['.id'],'name':row['name'],'service':row['service'],'profile':row['profile'],'disabled':row['disabled']})
        data['html_client_list'] = render_to_string('client/list.html', {
            'client': clients
        })
    else:
        context = {'client': {'id':client[0]['.id'],'name':client[0]['name']}}
        data['html_form'] = render_to_string('client/enable.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/')
def clientRemote(request):
    ip = request.GET.get('ip', None)
    return render(request, 'client_remote.html',{'data': ip})

@login_required(login_url='/')
def clientPing(request,pk):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    client = connect.talk('/ppp/active/print \n?.id='+pk)
    client = client[0]
    ping = connect.talk('/ping \n=address='+client['address']+'\n=count=5')
    data = dict()
    context = {'client': client,'ping':ping}
    data['html_form'] = render_to_string('client/ping.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/')
def antenaList(request):
    connect = Api(request.session.get('ip_address'), user=request.session.get('username'), password=request.session.get('password'))
    neighbors = connect.talk('/ip/neighbor/print')
    # return JsonResponse(neighbors,safe=False)
    return render(request, 'antena_list.html',{'neighbors':neighbors, 'router':{'id':request.session.get('id')}})
