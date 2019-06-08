from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import ExecutiveForm
from django.contrib import messages
from app.models import Executive, States, User, Zones, Category, Keyword, Business, SearchAnalytics
from administration.models import Administrator
from app.bizrefpro_mail import BizEmailService
import json, time, magic, csv
from bizrefpro.settings import BASE_DIR
from django.db import connection

# Create your views here.


def dashboard(request):
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
    page_context = dict()
    page_context['title'] = "Bizrefpro Dashboard"
    page_context['pageTitle'] = 'Dashboard'
    return render(request, "administration/dashboard.html", page_context)


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
            try:
                executive = Executive.objects.get(secret_code=eform.cleaned_data['secret_code'])
                messages.error(request, "Secret Code already exists")
            except:
                executive = Executive(first_name=eform.cleaned_data['first_name'],last_name=eform.cleaned_data['last_name'], email=eform.cleaned_data['email'], secret_code=eform.cleaned_data['secret_code'], role=eform.cleaned_data['role'], password=make_password(password=eform.cleaned_data['password'], salt=None, hasher="bcrypt"), state=state, zone=zone)
                executive.save()
                messages.success(request, "Employee Added Successfully")
        else:
            messages.error(request,eform.errors)
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
    htmlResponse = ""
    htmlResponse +='<option value="0">Select Executives</option>'
    try:
        executives = Executive.objects.filter(zone=id,role='executive').exclude(deleted=True)
        for executive in executives:
            htmlResponse +='<option value="'+str(executive.id)+'">'+executive.first_name.capitalize()+' '+str(executive.last_name).capitalize()+'</option>'
    except Exception as e:
        print(e)
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
    users = User.objects.all().order_by('-id').exclude(deleted=True)[start:start+length]
    for user in users:
        status = '<span class="text-warning">Pending</span>'
        action = "<a href='' class='approve_user' data-id = '"+str(user.id)+"'>Approve</a>"
        if user.active:
            action = ""
            status = '<span class="text-success">Approved<span>'
        action = '<a href="/administration/user_login/'+str(user.id)+'" target="_blank">Login</a>'+action+" <a href='' class='delete_user text-danger' data-id = '"+str(user.id)+"'>Delete</a>"
        list.append({"name":user.name,"email":user.email, "phone": user.phone, "city":user.city,"status":status,"action":action})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = count  # show from how many record its filtered.
    mdict['recordsFiltered'] = count  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))

def get_employees(request):
    if "admin_id" not in request.session:
        return HttpResponse(json.dumps({}))
    list = []
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    count = Executive.objects.count()
    executives = Executive.objects.all().order_by('-id').exclude(deleted=True)[start:start+length]
    for executive in executives:
        list.append({"name": executive.first_name + " " + executive.last_name,"email":executive.email, "phone": executive.phone, "role":executive.role})
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
            keywords_list = business.keywords.all().exclude(deleted=True).values_list('id', flat=True)
        category = Category.objects.get(id=id)
        keywords = Keyword.objects.filter(category=category).exclude(deleted=True)
        for keyword in keywords:
            if 'business_id' in request.GET:
                if keyword.id in keywords_list:
                    html_response += '<li><input type="checkbox" checked="checked" class="keywords_to_add" data-category="'+str(category.id)+'" data-title="' + keyword.name +'" value="' + str(keyword.id) + '"/>' + keyword.name + '</li>'
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


def top_keywords(request):
    if "admin_id" not in request.session:
        return HttpResponseRedirect('/administration/login')
    page_context = dict()
    page_context["title"]="Bizrefpro Dashboard"
    page_context['pageTitle'] = 'Top Keywords'
    return render(request, "administration/top_keywords.html", page_context)


def get_hits(request):
    if "admin_id" not in request.session:
        return HttpResponse(json.dumps({}))
    list = []
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    cursor = connection.cursor()
    cursor.execute("""select count(*) as count from (select search_keywords, 
    sum(`search_counter`) as hits 
    from app_searchanalytics 
    group by search_keywords 
    order by hits desc) t""")
    result = cursor.fetchall()
    count = result[0][0]
    analytics = SearchAnalytics.objects.raw("""select id, search_keywords, 
    sum(`search_counter`) as hits 
    from app_searchanalytics 
    group by search_keywords 
    order by hits desc""")[start:start+length]
    rank = start
    for analytic in analytics:
        rank = rank + 1
        list.append({"rank":str(rank),"keyword":analytic.search_keywords, "hits": str(analytic.hits)})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = count  # show from how many record its filtered.
    mdict['recordsFiltered'] = count  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))

