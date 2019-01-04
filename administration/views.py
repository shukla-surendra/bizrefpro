from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import ExecutiveForm
from django.contrib import messages
from app.models import Executive, States, User, Zones, Category, Keyword, Business
from administration.models import Administrator
from app.bizrefpro_mail import BizEmailService
import json, time, magic, csv
from bizrefpro.settings import BASE_DIR

# Create your views here.

def dashboard(request):
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
    pageContext =  {"title": "Bizrefpro Dashboard"}
    pageContext['pageTitle'] = 'Dashboard'
    return render(request, "administration/dashboard.html", pageContext)


def add_employee(request):
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
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
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
    pageContext =  {"title": "Bizrefpro Dashboard"}
    pageContext['pageTitle'] = 'All Employee'
    return render(request, "administration/all_employee.html", pageContext)


def login(request):
    if "admin_id" in request.session:
        return HttpResponseRedirect('/administration')
    pageContext = {}
    if request.method == 'POST':
        try:
            administrator = Administrator.objects.get(email=request.POST['email'])
            if check_password(request.POST['password'], administrator.password):
                if administrator.active == False:
                    pageContext['message_type']="failed"
                    pageContext['message']="Your Profile is disabled Contact customer care to approve"
                    return render(request, "administration/login.html", pageContext)
                else:
                    request.session['admin_id'] = administrator.id
                    return HttpResponseRedirect('/administration')
            else:
                pageContext['message_type']="failed"
                pageContext['message']="Incorrect username and password"
                return render(request, "administration/login.html", pageContext)
        except:
            pageContext['message_type']="failed"
            pageContext['message']="Incorrect username and password"
            return render(request, "administration/login.html", pageContext)
    pageContext["title"]= "Bizrefpro Admin Login"
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

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/administration/login')

def all_users(request):
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
    pageContext =  {"title": "Bizrefpro Dashboard"}
    pageContext['pageTitle'] = 'All Users'
    return render(request, "administration/all_business_users.html", pageContext)

def get_users(request):
    if "admin_id" not in request.session:
        return HttpResponse(json.dumps({}))
    list = []
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    count = User.objects.count()
    users = User.objects.all().order_by('-id')[start:start+length]
    for user in users:
        status = '<span class="text-warning">Pending</span>'
        action = "<a href='' class='approve_user' data-id = '"+str(user.id)+"'>Approve</a>"
        if user.active:
            action = ""
            status = '<span class="text-success">Approved<span>'
        status = '<a href="/administration/user_login/'+str(user.id)+'" target="_blank">Login</a> '+status
        list.append({"name":user.name,"email":user.email, "phone": user.phone, "city":user.city,"status":status,"action":action})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = count  # show from how many record its filtered.
    mdict['recordsFiltered'] = count  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))

def approve_users(request):
    response = {}
    if "admin_id" not in request.session:
        response['status'] = False
        response['message'] = "Admin not logged in"
        return HttpResponse(json.dumps(response))
    user_id = int(request.GET['user_id'])
    try:
        user = User.objects.get(id=user_id)
        user.active = True
        user.save()
        user_email = BizEmailService()
        user_email.send_approval_notification_to_user(user)
        response['status'] = True
        response['message'] = "User successfully approved"
    except:
        response['status'] = False
        response['message'] = "Unknown error occured"
    return HttpResponse(json.dumps(response))


def category_import(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        mime = magic.Magic(mime=True)
        if "csv_file" in request.FILES:
            csv_file = request.FILES['csv_file']
            mimetype = mime.from_buffer(csv_file.read())
            if mimetype in ["text/plain", 'text/csv']:
                nt = str(time.time())
                stamp = nt.replace(".", "-")
                filename = stamp + "-" + csv_file.name.replace(" ", "-")
                filename = filename.replace(",", "-")
                with open(BASE_DIR + '/static/uploads/' + filename, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)
                with open(BASE_DIR + '/static/uploads/' + filename) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        try:
                            if row[0] not in ["", None]:
                                category = Category(name=row[0],parent_id=parent_id, active=1)
                                category.save()
                        except:
                            pass
                    messages.success(request, 'CSV successfully imported.')
    context = {}
    parent_categories = Category.objects.filter(parent_id=0)
    context['parent_categories'] = parent_categories;
    return render(request, "administration/category_import.html", context)


def keyword_import(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        child_id = request.POST['child_id']
        category = Category.objects.get(id=child_id)
        mime = magic.Magic(mime=True)
        if "csv_file" in request.FILES:
            csv_file = request.FILES['csv_file']
            mimetype = mime.from_buffer(csv_file.read())
            if mimetype in ["text/plain", 'text/csv']:
                nt = str(time.time())
                stamp = nt.replace(".", "-")
                filename = stamp + "-" + csv_file.name.replace(" ", "-")
                filename = filename.replace(",", "-")
                with open(BASE_DIR + '/static/uploads/' + filename, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)
                with open(BASE_DIR + '/static/uploads/' + filename) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        try:
                            if row[0] not in ["", None]:
                                keyword = Keyword(name=row[0], category=category, active=True)
                                keyword.save()
                        except:
                            pass
                    messages.success(request, 'CSV successfully imported.')
    context = {}
    parent_categories = Category.objects.filter(parent_id=0)
    context['parent_categories'] = parent_categories;
    return render(request, "administration/keyword_import.html", context)

def get_sub_category(request, id):
    htmlResponse = "";
    if 'user' in request.GET:
        try:
            parent_categories = Category.objects.filter(parent_id=id).order_by('name')
            for category in parent_categories:
                htmlResponse += '<li><input type="checkbox" name="categories" class="sub_category_id sub_category_'+str(category.id)+'" value="' + str(category.id) + '">' + category.name + '</li>'
        except:
            None

    else:
        htmlResponse += '<option value="">Select SubCategory</option>'
        try:
            parent_categories = Category.objects.filter(parent_id=id)
            for category in parent_categories:
                htmlResponse += '<option value="' + str(category.id) + '">' + category.name + '</option>'
        except:
            None
    return HttpResponse(htmlResponse)


def get_keywords(request, id):
    html_response = ""
    try:
        if 'business_id' in request.GET:
            business_id = request.GET['business_id']
            business = Business.objects.get(id=business_id)
            keywords_list = business.keywords.all().values_list('id', flat=True)
        category = Category.objects.get(id=id)
        keywords = Keyword.objects.filter(category=category)
        for keyword in keywords:
            if 'business_id' in request.GET:
                if keyword.id in keywords_list:
                    html_response += '<li> <input type="checkbox" checked="checked" class="keywords_to_add" data-category="'+str(category.id)+'" data-title="' + keyword.name +'" value="' + str(keyword.id) + '"/>' + keyword.name + '</li>'
                else:
                    html_response += '<li> <input type="checkbox" class="keywords_to_add" data-category="' + str(category.id) + '" data-title="' + keyword.name + '" value="' + str(keyword.id) + '"/>' + keyword.name + '</li>'
            else:
                html_response += '<li> <input type="checkbox" class="keywords_to_add" data-category="' + str(category.id) + '" data-title="' + keyword.name + '" value="' + str(keyword.id) + '"/>' + keyword.name + '</li>'
    except:
        print("error")
    return HttpResponse(html_response)


def user_login(request, id):
    if "admin_id" in request.session:
        request.session['id'] = id
        return redirect("/user/dashboard")
    else:
        return redirect("/")

