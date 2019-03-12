from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from django.contrib import messages
from app.models import Executive, User, Zones, States, Cities
import datetime
from django.utils import timezone
import logging
from django.db.models import Sum
from django.core import serializers
# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


def login(request):
    pageContext =  {"title": "Bizrefpro Executive Login"}
    pageContext['pageTitle'] = 'Bizrefpro'
    if request.method == 'POST':
        email = request.POST['email']
        try:
            executive = Executive.objects.get(email=email)
            if check_password(request.POST['password'], executive.password):
                request.session['executive_id'] = executive.id
                request.session['executive_type'] = executive.role
                return HttpResponseRedirect('/executive/dashboard')
            else:
                pageContext['message_type']="failed"
                pageContext['message']="Incorrect username and password"
        except:
            pageContext['message_type']="failed"
            pageContext['message']="Incorrect username and password"

    return render(request, "executive/login.html", pageContext)


def dashboard(request):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    executive = Executive.objects.get(id=request.session['executive_id'])
    pageContext = {}
    pageContext['pageTitle'] = "Dashboard"
    if executive.role == 'executive':
        pageContext['breadcrumb'] = "Dashboad >> Excutive("+executive.first_name+" "+str(executive.last_name)+")"
        pageContext['target_role'] = executive.role
        pageContext['target_zone'] = executive.zone.id
        pageContext['executive_id'] = executive.id
        pageContext['state'] = executive.state.id
        pageContext['executive'] = executive
        return render(request, "executive/executive/index.html", pageContext)
    elif executive.role == 'state-manager':
        loggedExecutive = Executive.objects.get(id=request.session['executive_id'])
        try:
            zones = Zones.objects.filter(state=loggedExecutive.state)
        except:
            zones = {}
        pageContext['zones'] = zones 
        pageContext['breadcrumb'] = "Dashboad >> State Manager("+executive.first_name+" "+str(executive.last_name)+")"
        pageContext['state'] = loggedExecutive.state.id
        pageContext['executive_id'] = loggedExecutive.id
        subExecutive = Executive.objects.filter(state=executive.state, role='zone-manager')
        pageContext['subExecutive'] = subExecutive
        return render(request, "executive/state-manager/index.html", pageContext)
    else :
        #city-manager
        pageContext['breadcrumb'] = "Dashboad >> Zone Manager("+executive.first_name+" "+str(executive.last_name)+")"
        pageContext['zone_id'] = executive.zone.id
        pageContext['role'] = executive.role
        pageContext['state'] = executive.state
        return render(request, "executive/zone-manager/index.html", pageContext)


def lead_detail(request, id):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    executive = Executive.objects.get(id=request.session['executive_id'])
    user = User.objects.get(id=id)
    pageContext = dict()
    total_reference = User.objects.filter(reference_id=user.id).count()
    pageContext['user']=user
    pageContext['total_reference'] = total_reference
    if user.active == True:
        pageContext['status'] = 'Active'
    else:
        pageContext['status'] = 'Inactive'
    if executive.role == 'state-manager':
        try:
           zone_manager = Executive.objects.get(zone = user.zone,role = 'zone-manager')
           zone_manager = zone_manager.first_name+" "+str(zone_manager.last_name)
        except:
            zone_manager = ""
        pageContext['breadcrumb'] = "State-Manager ("+executive.first_name+" "+str(executive.last_name)+") >> Zone Manager("+zone_manager+") >>Executive ("+user.executive.first_name+" "+str(user.executive.last_name)+")"
    elif executive.role == 'zone-manager':
        pageContext['breadcrumb'] = "Zone Manager ("+executive.first_name+" "+str(executive.last_name)+")  >> Executive ("+user.executive.first_name+" "+str(user.executive.last_name)+")"
    else:
        pageContext['breadcrumb'] = "Executive ("+executive.first_name+" "+str(executive.last_name)+")"
            
    pageContext['lead_name'] = user.name
    added_year = user.created_at+datetime.timedelta(days=364)
    pageContext['expiry'] = added_year.strftime("%d-%m-%Y")
    if executive.role == 'state-manager':
        pageContext['layoutFile'] = "executive/state-manager/layouts/layout.html"
    elif executive.role == 'zone-manager':
        pageContext['layoutFile'] = "executive/zone-manager/layouts/layout.html"
    else:
        pageContext['layoutFile'] = "executive/executive/layouts/layout.html"
    return render(request, "executive/common/lead-detail.html", pageContext)

def lead(request):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    #user = User.objects.get(id=id)
    pageContext = {}
    executive = Executive.objects.get(id=request.session['executive_id'])
    pageContext['target_role'] = executive.role
    pageContext['target_zone'] = executive.zone.id
    pageContext['executive_id'] = executive.id
    pageContext['state'] = executive.state.id
    pageContext['executive'] = executive
    if executive.role == 'zone-manager':
        pageContext['breadcrumb'] = 'Zone Manager ("'+executive.first_name+" "+str(executive.last_name)+'")>> All Leads'
        pageContext['layout_file'] = 'executive/zone-manager/layouts/layout.html'
    elif executive.role == 'state-manager':
        pageContext['breadcrumb'] = 'State Manager ("'+executive.first_name+" "+str(executive.last_name)+'")>> All Leads'
        pageContext['layout_file'] = 'executive/state-manager/layouts/layout.html'
    else:
        #executive
        pageContext['breadcrumb'] = 'Executive Manager ("'+executive.first_name+" "+str(executive.last_name)+'")>> All Leads'
        pageContext['layout_file'] = 'executive/executive/layouts/layout.html'
    return render(request, "executive/common/lead.html", pageContext)


def executive_lead(request, id):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    # loggedin executive
    loggedExecutive = Executive.objects.get(id=request.session['executive_id'])
    # user = User.objects.get(id=id)
    pageContext = {}
    executive = Executive.objects.get(id=id)
    pageContext['target_role'] = executive.role
    pageContext['target_zone'] = executive.zone.id
    pageContext['executive_id'] = executive.id
    pageContext['state'] = executive.state
    pageContext['executive'] = executive
    if loggedExecutive.role == 'zone-manager':
        pageContext['breadcrumb'] = 'Zone Manager ("'+loggedExecutive.first_name+" "+str(loggedExecutive.last_name)+'")>>Executive("'+executive.first_name+" "+str(executive.last_name)+'") >> All Leads'
        pageContext['layout_file'] = 'executive/zone-manager/layouts/layout.html'
    elif loggedExecutive.role == 'state-manager':
        pageContext['breadcrumb'] = 'State Manager ("'+loggedExecutive.first_name+" "+str(loggedExecutive.last_name)+'")>>Executive("'+executive.first_name+" "+str(executive.last_name)+'") >>All Leads'
        pageContext['layout_file'] = 'executive/state-manager/layouts/layout.html'
    else:
        #executive
        pageContext['breadcrumb'] = 'Executive ("'+loggedExecutive.first_name+" "+str(loggedExecutive.last_name)+'")>> All Leads'
        pageContext['layout_file'] = 'executive/executive/layouts/layout.html'
    return render(request, "executive/common/lead.html", pageContext)


def zone_city_manager(request):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    #loggedin executive
    pageContext = {}
    loggedExecutive = Executive.objects.get(id=request.session['executive_id'])
    try:
        zones = Zones.objects.filter(state=loggedExecutive.state)
    except:
        zones = {}
    pageContext['zones'] = zones 
    pageContext['breadcrumb'] = loggedExecutive.first_name+" "+str(loggedExecutive.last_name)
    pageContext['state'] = loggedExecutive.state.id
    pageContext['executive_id'] = loggedExecutive.id
    return render(request, "executive/state-manager/zone-city-manager.html", pageContext)


def setting(request):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    executive = Executive.objects.get(id=request.session['executive_id'])
    if request.method == "POST":
        #
        password = request.POST['password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.warning(request, 'Your password and confirm password didn\'t match')
        else:
            if check_password(password, executive.password):
               executive.password = make_password(password=password2, salt=None, hasher="bcrypt")
               executive.save()
               messages.success(request, 'Your password is updated')
            else:
                messages.warning(request, 'Your current password is incorrect')

    # user = User.objects.get(id=id)
    pageContext = {}
    pageContext['executive'] = executive
    # getting state
    state = ""
    try:
        state_obj = States.objects.get(id=executive.state)
        state = state_obj.name
    except Exception as e:
        print(e)
    zone = ""
    try:
        zone_obj = Cities.objects.get(id=executive.state)
        zone = zone_obj.name
    except Exception as e:
        print(e)
    pageContext['state'] = state
    pageContext['zone'] = zone
    if executive.role == 'zone-manager':
        pageContext['breadcrumb'] = "Zone Manager > Setting"
        pageContext['template_url'] = 'executive/zone-manager/layouts/layout.html'
    elif executive.role == 'state-manager':
        pageContext['breadcrumb'] = "State Manager > Setting"
        pageContext['template_url'] = 'executive/state-manager/layouts/layout.html'
    else:
        pageContext['breadcrumb'] = "Executive > Setting"
        pageContext['template_url'] = 'executive/executive/layouts/layout.html'
    return render(request, "executive/common/setting.html", pageContext)


def executive(request):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    executive = Executive.objects.get(id=request.session['executive_id'])
    pageContext = {}
    pageContext['zone_id'] = executive.zone.id
    pageContext['state'] = executive.state.id
    pageContext['role'] = executive.role
    if executive.role == 'zone-manager':
        pageContext['breadcrumb'] = 'Zone Manager('+executive.first_name+" "+str(executive.last_name)+') >> Executives'
        pageContext['layout_file'] = 'executive/zone-manager/layouts/layout.html'
    elif executive.role == 'state-manager':
        loggedExecutive = Executive.objects.get(id=request.session['executive_id'])
        try:
            zones = Zones.objects.filter(state=loggedExecutive.state)
        except:
            zones = {}
        pageContext['zones'] = zones
        pageContext['breadcrumb'] = 'State Manager('+executive.first_name+" "+str(executive.last_name)+') >> Executives'
        pageContext['layout_file'] = 'executive/state-manager/layouts/layout.html'
    return render(request, "executive/common/executive.html", pageContext)


def executive_list(request, id):
    if "executive_id" not in request.session:
        return HttpResponseRedirect('/executive/login')
    #loggedin executive
    pageContext = {}
    loggedExecutive = Executive.objects.get(id=request.session['executive_id'])
    #zone-manager object
    executive = Executive.objects.get(id=id)
    pageContext = {}
    pageContext['zone_id'] = executive.zone.id
    pageContext['role'] = 'zone-mamanger'
    pageContext['state'] = executive.state
    pageContext['breadcrumb'] = 'Zone Manager('+executive.first_name+""+str(executive.last_name)+') >> Executives'
    if(loggedExecutive.role == 'state-manager'):
        pageContext['breadcrumb'] = 'State Manager ('+loggedExecutive.first_name+''+str(loggedExecutive.last_name)+') >> '+pageContext['breadcrumb']
    pageContext['layout_file'] = 'executive/state-manager/layouts/layout.html'
    return render(request, "executive/common/executive.html", pageContext)


def logout(request):
    del request.session['executive_id']
    return HttpResponseRedirect('/executive/login')

# return list of executive for zone-mamanger, state-manager
def get_executive_data(request):
    minRange = ""
    maxRange = ""
    searchZone = ""
    try:
        search = str(request.GET.getlist('columns[0][search][value]')[0])
        dateRange = search.split(",")
        searchZone = dateRange[0]
        if dateRange[1] !="" and dateRange[2] !="":
            minRange = timezone.make_aware(datetime.datetime.strptime(dateRange[1], "%Y-%m-%d"))
            maxRange = timezone.make_aware(datetime.datetime.strptime(dateRange[2], "%Y-%m-%d"))          
    except  Exception as e:
        print('%s (%s)' % (e, type(e)))
    try:
       zone = Zones.objects.get(id=request.GET['zone'])
    except:
        zone = None
    role = request.GET['role']
    try:
       state = States.objects.get(id=request.GET['state'])
    except:
       state = None
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    if role=='state-manager':
        if searchZone != "":
            object_list = Executive.objects.filter(role='executive', zone=searchZone,state=state)[start:start+length]  # or any kind of queryset
            total = Executive.objects.filter(role='executive', zone=searchZone, state=state).count()
        else:
            object_list = Executive.objects.filter(role='executive', state=state)[start:start+length]  # or any kind of queryset
            total = Executive.objects.filter(role='executive',  state=state).count()
    else:
        # zone-manager
        object_list = Executive.objects.filter(role='executive', zone=zone)[start:start+length]  # or any kind of queryset
        total = Executive.objects.filter(role='executive',  zone=zone).count()
    list = []
    totalRevenue = 0
    for object in object_list:
        totalSum = 0
        if object.zone != None:
            zone=object.zone.name
        else:
            zone=""
        if minRange =="" and maxRange == "":
            leads = User.objects.filter(executive=object).count()
            totalSum = User.objects.filter(executive=object).aggregate(Sum('amount'))
            totalSum = totalSum['amount__sum']
        else:
            leads = User.objects.filter(executive=object,created_at__range=[minRange, maxRange]).count()
            totalSum = User.objects.filter(executive=object,created_at__range=[minRange, maxRange]).aggregate(Sum('amount'))            
            totalSum = totalSum['amount__sum']
        if totalSum != None:
            totalRevenue +=totalSum
        if object.active == True:
            status = "Active"
        else:
            status = "In-Active"
        list.append({"executive": "<a href='/executive/lead/"+str(object.id)+"'>"+object.first_name+" "+str(object.last_name)+"</a>", "zone": zone, "leads": leads, "revenue": totalSum, "status": status, "action": "<a href='#' class='text-primary'>Edit</a>"})
    list.append({"executive": "<h4>Total:</h4>", "zone": '', "leads": '', "revenue": totalRevenue, "status": '', "action": ""})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = total  # show from how many record its filtered.
    mdict['recordsFiltered'] = total  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))


# return list of lead for executive, state-manager, zone-manager
'''
#reqired field to fetch data
zone-manager : zone
Executive : executive id
state-manager : state

'''
def get_executive_lead(request):
    minRange = ""
    maxRange = ""
    try:
        search = str(request.GET.getlist('columns[0][search][value]')[0])
        dateRange = search.split(",")
        if dateRange[0] !="" and dateRange[1] !="":
            minRange = timezone.make_aware(datetime.datetime.strptime(dateRange[0], "%Y-%m-%d"))
            maxRange = timezone.make_aware(datetime.datetime.strptime(dateRange[1], "%Y-%m-%d"))          
    except  Exception as e:
        print('%s (%s)' % (e, type(e)))
    try:
        executive = Executive.objects.get(id=request.GET['executive_id'])
    except:
        executive = None
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    target_role = request.GET['role']
    try:
        zone = Zones.objects.get(id=request.GET['zone'])
    except:
        zone = None
    try:
        state = States.objects.get(id=request.GET['state'])
    except:
        state = None
    totalAmount = 0
    if target_role == "zone-manager":
        if minRange == "" or maxRange =="":
            object_list = User.objects.filter(zone=zone)[start:start + length]  # or any kind of queryset
            total = User.objects.filter(zone=zone).count()
        else:
            object_list = User.objects.filter(zone=zone,created_at__range=[minRange, maxRange])[start:start + length]  # or any kind of queryset
            total = User.objects.filter(zone=zone,created_at__range=[minRange, maxRange]).count()
        
    elif target_role == "state-manager":
        if minRange == "" or maxRange =="":
            object_list = User.objects.filter(state=state)[start:start+length]  # or any kind of queryset
            total = User.objects.filter(state=state).count()
        else:
            object_list = User.objects.filter(state=state,created_at__range=[minRange, maxRange])[start:start+length]  # or any kind of queryset
            total = User.objects.filter(state=state,created_at__range=[minRange, maxRange]).count()
    else:
        #executive
        if minRange == "" or maxRange =="":
            object_list = User.objects.filter(executive=executive)[start:start+length]  # or any kind of queryset
            total = User.objects.filter(executive=executive).count()
        else:
            object_list = User.objects.filter(executive=executive,created_at__range=[minRange, maxRange])[start:start+length]  # or any kind of queryset
            total = User.objects.filter(executive=executive,created_at__range=[minRange, maxRange]).count()
    list = []
    for object in object_list:
        if object.active == True:
            status = "Active"
        else:
            status = "In-Active"
        addedYear = object.created_at+datetime.timedelta(days=364)
        ref_count = User.objects.filter(reference_id=object.id).count()
        list.append({"lead": '<input type="checkbox" value="'+str(object.id)+'" name="selectcheck" class="selectcheck"><a href="/executive/lead_detail/'+str(object.id)+'">'+object.name+'</a>', "created": str(object.created_at.strftime("%d-%m-%Y")), "renew": str(addedYear.strftime("%d-%m-%Y")), "revenue": object.amount,"referer":'<a href="" class="show_referer" data-id="'+str(object.id)+'">'+str(ref_count)+'</a>', "status": status})
        totalAmount += object.amount
    list.append({"lead": "<h4>Total:</h4>", "created": "", "renew": "", "revenue": "<h4>"+str(totalAmount)+"</h4>", "referer":"", "status": ""})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = total  # show from how many record its filtered.
    mdict['recordsFiltered'] = total  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))

def get_zonecity_manager(request):
    minRange = ""
    maxRange = ""
    searchZone = ""
    totalRevenue = 0
    try:
        search = str(request.GET.getlist('columns[0][search][value]')[0])
        dateRange = search.split(",")
        searchZone = dateRange[0]
        if dateRange[1] !="" and dateRange[2] !="":
            minRange = timezone.make_aware(datetime.datetime.strptime(dateRange[1], "%Y-%m-%d"))
            maxRange = timezone.make_aware(datetime.datetime.strptime(dateRange[2], "%Y-%m-%d"))          
    except  Exception as e:
        print('%s (%s)' % (e, type(e)))
    try:
        state = States.objects.get(id=request.GET['state'])
    except:
        state = None
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    try:
        if searchZone !="":
            zone=Zones.objects.get(id=searchZone)
            object_list = Executive.objects.filter(state=state,zone=zone,role='zone-manager')[start:start + length]  # or any kind of queryset
            total = Executive.objects.filter(state=state,zone=zone,role='zone-manager').count()
        else:
            object_list = Executive.objects.filter(state=state, role='zone-manager')[start:start + length]  # or any kind of queryset
            total = Executive.objects.filter(state=state, role='zone-manager').count()
        list = []
        for object in object_list:
            if object.active == True:
                status = "Active"
            else:
                status = "In-Active"
            try:
                zone_name = object.zone.name
            except:
                zone_name = ""
            total_executive = Executive.objects.filter(zone=object.zone, role='executive').count()
            if minRange == "" or maxRange =="":
                leads_count = User.objects.filter(zone=object.zone).count()
                amountSum = User.objects.filter(zone=object.zone).aggregate(Sum('amount'))
                amountSum = amountSum['amount__sum']
                totalRevenue += amountSum
            else:
                leads_count = User.objects.filter(zone=object.zone,created_at__range=[minRange, maxRange]).count()
                amountSum = User.objects.filter(zone=object.zone, created_at__range=[minRange, maxRange]).aggregate(Sum('amount'))
                amountSum = amountSum['amount__sum']
                totalRevenue += amountSum

            list.append({"zone-city-manager": '<input type="checkbox" value="'+str(object.id)+'" name="selectcheck" class="selectcheck"><a href="/executive/executive/'+str(object.id)+'">'+object.first_name+" "+str(object.last_name)+'</a>', "zone-city": zone_name, "executive_count": total_executive, "leads_count": leads_count,"revenue": amountSum,  "status": status, "action":'<a href="javascript:void(0)" class="text-primary">Edit</a>'})
        list.append({"zone-city-manager": '<h4>Total:</h4>', "zone-city": '', "executive_count": '', "leads_count": '',"revenue": totalRevenue, "status": "", "action":''})
        mdict = {"data": list}
        mdict['draw'] = request.GET['draw']
        mdict['recordsTotal'] = total  # show from how many record its filtered.
        mdict['recordsFiltered'] = total  # show how many record filtered.
        return HttpResponse(json.dumps(mdict))
    except:
        return HttpResponse(json.dumps([]))


def get_reference(request):
    data = list()
    if 'id' in request.GET:
        id = request.GET['id']
        referers = User.objects.filter(reference_id=id)
        for object in referers:
            referer_count = User.objects.filter(reference_id=object.id).count()
            data.append({'id': object.id,'name': object.name,'email': object.email, 'reference': referer_count})
    return HttpResponse(json.dumps(data), content_type="application/json")


    

