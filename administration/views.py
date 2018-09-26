from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import ExecutiveForm
from django.contrib import messages
from app.models import Executive, States, Cities, Zones

# Create your views here.

def dashboard(request):
    pageContext =  {"title": "Bizrefpro Dashboard"}
    pageContext['pageTitle'] = 'Dashboard'
    return render(request, "administration/dashboard.html", pageContext)


def add_employee(request):
    pageContext =  {"title": "Bizrefpro Dashboard"}
    states = States.objects.all()
    pageContext['states'] = states
    pageContext['pageTitle'] = 'Add Employee'
    if request.method == "POST":
        try:
            emailObj = Executive.objects.get(email=request.POST['email'])
            messages.warning(request, 'This Email Already Exists.')
            return render(request, "administration/add_employee.html", pageContext)
        except:
            None
        eform = ExecutiveForm(request.POST)
        if eform.is_valid():
            try:
                state = States.objects.get(id=request.POST['state'])
            except:
                state = None
            try:
                zone = Zones.objects.get(id=request.POST['zone'])
            except:
                zone = None
            executive = Executive(first_name=eform.cleaned_data['first_name'],last_name=eform.cleaned_data['last_name'],email=eform.cleaned_data['email'],role=eform.cleaned_data['role'],password=make_password(password=eform.cleaned_data['password'], salt=None, hasher="bcrypt"),state=state,zone=zone)
            executive.save()
        else:
            print(eform.errors)
    return render(request, "administration/add_employee.html", pageContext)


def all_employee(request):
    pageContext =  {"title": "Bizrefpro Dashboard"}
    pageContext['pageTitle'] = 'All Employee'
    return render(request, "administration/all_employee.html", pageContext)


def login(request):
    pageContext =  {"title": "Bizrefpro Admin Login"}
    pageContext['pageTitle'] = 'Bizrefpro Administration Login'
    return render(request, "administration/login.html", pageContext)


def get_zones(request, id):
    htmlResponse = "";
    htmlResponse +='<option value="0">Select Zone</option>'
    try:
        cities = Zones.objects.filter(state_id=id)
        for city in cities:
            htmlResponse +='<option value="'+str(city.id)+'">'+city.name+'</option>'
    except:
        None        
    return HttpResponse(htmlResponse);


def get_executives(request, id):
    htmlResponse = "";
    htmlResponse +='<option value="0">Select Executives</option>'
    try:
        executives = Executive.objects.filter(zone=id,role='executive')
        for executive in executives:
            htmlResponse +='<option value="'+str(executive.id)+'">'+executive.first_name.capitalize()+' '+executive.last_name.capitalize()+'</option>'
    except:
        None        
    return HttpResponse(htmlResponse);