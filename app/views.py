from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserForm, ContactForm
from .models import User, Business, BizRefProSearch, Contact, Website, States, Otp, Thumsup, Zones, Media, Referer
from user.ses import send_mail
from django.contrib import messages
import uuid, json, os
from bizrefpro.settings import BASE_DIR
from random import randint
from django.utils import timezone
from datetime import timedelta
from .bizrefpro_mail import send_enquiry_email, send_userforget_password_link_mail, send_otp




# Create your views here.
def index(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business"}
    return render(request, "app/index.html", pageContext)

def contact(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Contact Us"}
    if request.method == "POST":
        cform = ContactForm(request.POST)
        if cform.is_valid():
            contact = Contact(name=cform.cleaned_data['name'], email=cform.cleaned_data['email'], contact=cform.cleaned_data['contact'], message=cform.cleaned_data['message'])
            contact.save()
            messages.add_message(request, messages.SUCCESS, 'Enquiry Sent Successfully')
        
    return render(request, "app/contact.html", pageContext)


def pricing(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Pricing"}
    return render(request, "app/pricing.html", pageContext)

def privacy(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Privacy"}
    return render(request, "app/privacy-policy.html", pageContext)

def terms(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Terms"}
    return render(request, "app/terms.html", pageContext)

def franchise(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Franchise"}
    return render(request, "app/franchise.html", pageContext)
    

def about(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"About Us"}
    return render(request, "app/about-us.html", pageContext)

def faq(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Faq"}
    return render(request, "app/faq.html", pageContext)


def how_it_work(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"How It Works"}
    return render(request, "app/why-join.html", pageContext)


def plan(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"How It Works"}
    return render(request, "app/plan.html", pageContext)


def news(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"News"}
    return render(request, "app/news.html", pageContext)

def career(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Career"}
    return render(request, "app/career.html", pageContext)


def search_result(request):
    if "q" not in request.GET:
        return HttpResponseRedirect("/")
    query = 'SELECT *, MATCH (keywords) AGAINST(\''+request.GET['q']+'\' IN BOOLEAN MODE) AS score FROM app_bizrefprosearch WHERE MATCH (keywords) AGAINST(\''+request.GET['q']+'\' IN BOOLEAN MODE) order by score desc,rank desc'
    search = BizRefProSearch.objects.raw(query)
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Search Result"}
    pageContext['businesses']= search
    pageContext['page'] = "search";
    return render(request, "app/search-result.html", pageContext)


def search_result_test(request):
    if "q" not in request.GET:
        return HttpResponseRedirect("/")
    query = 'SELECT *, MATCH (keywords) AGAINST(\'' + request.GET['q'] + '\' IN BOOLEAN MODE) AS score FROM app_bizrefprosearch WHERE MATCH (keywords) AGAINST(\''+request.GET['q'] + '\' IN BOOLEAN MODE) order by score desc,rank desc'
    search = BizRefProSearch.objects.raw(query)
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Search Result"}
    pageContext['businesses']= search
    pageContext['page'] = "search";
    return render(request, "app/search-result-test.html", pageContext)

def hosting_features(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Hosting Features"}
    return render(request, "app/hosting-features.html", pageContext)


def login_register(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Login Register"}
    states = States.objects.filter(country_id=1)
    pageContext['states'] = states;
    if request.method == 'POST':
        if request.POST['form_type'] == "signup":
            try:
                user = User.objects.get(email=request.POST['email'])
                pageContext['message_type'] = "failed"
                pageContext['message'] = "Email Address Already Exists"
                return render(request, "app/login-register.html", pageContext)
            except:
                uform = UserForm(request.POST)
                if uform.is_valid():
                    if request.POST['state'] == 0:
                        state = None
                    else:
                        try:
                            state = States.objects.get(id=request.POST['state'])
                        except:
                            state = None
                    if request.POST['zone'] == 0:
                        zone = None
                    else:
                        try:
                            zone =Zones.objects.get(id=request.POST['zone'])
                        except:
                            zone = None
                    if request.POST['executive'] == 0:
                        executive = None
                    else:
                        try:
                            executive = Executive.objects.get(id=request.POST['executive'])
                        except:
                            executive = None
                    if 'referer' in request.GET:
                        referer = request.GET['referer']
                        try:
                            referer_object = Referer.objects.get(referer=referer)
                            referer_id = referer_object.user.id
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'], email=uform.cleaned_data['email'],password=make_password(password=uform.cleaned_data['password'], salt=None, hasher="bcrypt"), state=state,zone=zone, executive=executive,reference_id=referer_id)
                        except:
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'], email=uform.cleaned_data['email'],password=make_password(password=uform.cleaned_data['password'], salt=None, hasher="bcrypt"), state=state,zone=zone, executive=executive)
                    else:
                        user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'], email=uform.cleaned_data['email'],password=make_password(password=uform.cleaned_data['password'], salt=None, hasher="bcrypt"), state=state,zone=zone, executive=executive)
                    user.save()
                    pageContext['message_type']="success"
                    pageContext['message']="Registered Successfully"
                    messages.success(request, 'Your Application has been submitted successfully and waiting for approval. We will send notification through mail once approved.')
                    #return render(request, "app/login-register.html", pageContext)
                    return HttpResponseRedirect("/registration-success")
                else:
                    # return HttpResponse('POST method'+request.POST['name'])
                    # request.session['name'] ="Session Created";
                    pageContext['message_type']="failed"
                    pageContext['message']="Something Went wrong"
                    return render(request, "app/login-register.html", pageContext)
        if request.POST['form_type'] == "signin":
            try:
                user = User.objects.get(email=request.POST['email'])
                if check_password(request.POST['password'], user.password):
                    if user.active == False:
                        pageContext['message_type']="failed"
                        pageContext['message']="Your Profile is disabled Contact customer care to approve"
                        return render(request, "app/login-register.html", pageContext)
                    else:
                        request.session['id'] = user.id
                        return HttpResponseRedirect('user/dashboard')
                else:
                    pageContext['message_type']="failed"
                    pageContext['message']="Incorrect username and password"
                    return render(request, "app/login-register.html", pageContext)
            except:
                pageContext['message_type']="failed"
                pageContext['message']="Incorrect username and password"
                return render(request, "app/login-register.html", pageContext)
    pageContext['message_type']=""
    return render(request, "app/login-register.html", pageContext)


def forgot_password(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Forgot Password"}
    return render(request, "app/forgot_password.html", pageContext)

def registration_success(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Registration Success"}
    return render(request, "app/registration-successful.html", pageContext)

def reset_link(request):
    email = request.POST['email'];
    try:
        user = User.objects.get(email=email)
        uuidKey = uuid.uuid4().hex
        user.verification_key = uuidKey
        user.save()
        send_userforget_password_link_mail(user)
        return HttpResponse("ok")
    except:
        return HttpResponse("failed")

def reset_password(request, token):
    try:
        user = User.objects.get(verification_key=token)
        pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Password Reset"}
        return render(request, "app/password-reset.html", pageContext)
    except:
        pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Link Expired"}
        return render(request, "app/link-rexpired.html", pageContext)

def ssl_validation(request):
	return HttpResponse("D7A6A1569AF33477127AB63D7E1C2ECE34978E0B814DF205790B1311A67CA0B3 comodoca.com 5b4825a5529ea")


def syncSearch(request):
    businesses = Business.objects.all()
    for business in businesses:
        website = "";
        try:
            web = Website.objects.get(id=business.website)
            website = web.name
        except:
            pass
        try:
            search = BizRefProSearch.objects.get(business_id=business.id)
            search.title=business.title
            search.description=business.aboutus
            search.keywords=business.keyword
            search.address=business.address1
            search.website=website
            search.contact=business.contact_number
            search.rank=business.rating + business.thumbs_up
            search.save()
        except:
            search = BizRefProSearch(title=business.title,description=business.aboutus,keywords=business.keyword, address=business.city ,website=website, contact=business.contact_number, rank=business.rating+business.thumbs_up,business_id=business.id)
            search.save();
          
    return HttpResponse("Success")

def bizrefpro_promotions(request):
    pageContext =  {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle":"Forgot Password"}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        if name == "" or phone == "":
            return render(request, "promotions/index.html", pageContext)
        else:
            send_enquiry_email(name, email, phone, location)
            return render(request, "promotions/success.html", pageContext)
        
    else:
        return render(request, "promotions/index.html", pageContext)

def send_thumbsup_otp(request):
    email = request.GET['email'];
    business_id = request.GET['business_id'];
    otp_number = randint(100000, 999999);
    try:
        otp = Otp(otp=otp_number,email=email,business_id=business_id)
        otp.save()
        send_otp(email, otp_number)
    except:
        None
    resp = {}
    resp['status']= "success"
    resp["message"] = "Opt successfully sent"
    return HttpResponse(json.dumps(resp))


def thums_up(request):
    resp = {}
    otp = request.GET['otp'];
    email = request.GET['email'];
    business_id = request.GET['business_id'];
    time_threshold = timezone.now() - timedelta(minutes=5)
    Otp.objects.filter(created_at__lt=time_threshold).delete()
    try:
        otp_count = Otp.objects.filter(otp=otp,business_id=business_id).count()
        if otp_count > 0:
            business = Business.objects.get(id=business_id)
            business.thumbs_up +=1
            business.save()
            thumsup = Thumsup(email=email,business_id=business_id,thumbs_up=1)
            thumsup.save()
            resp['status']= "success"
            resp["message"] = "Thumbsup successfully done"
        else:
            resp['status']= "failed"
            resp["message"] = "Incorrect otp" 
    except:
        resp['status']= "failed"
        resp["message"] = "Incorrect otp"   
    return HttpResponse(json.dumps(resp))

def delete_media_file(request):
    resp = {}
    if "id" not in request.session:
        resp['status'] = "failed"
        resp['message'] = "User Not Logged In"
        return HttpResponse(json.dumps(resp))
    else:
        media_id = request.GET['media_id']
        media_role = request.GET['media_role']
        if media_role == "user":
            pass
        elif media_role == "business":
            pass
        try:
            media = Media.objects.get(id=media_id)
            if os.path.exists(BASE_DIR+'/static/uploads/documents/'+media.path):
                os.remove(BASE_DIR+'/static/uploads/documents/'+media.path)
            media.delete() 
        except:
            None
    resp['status'] = "success"
    return HttpResponse(json.dumps(resp))

#error handlers
def handler404(request, exception):
    return render(request, 'errors/404.html', locals())
def handler400(request, exception):
    return render(request, 'errors/400.html', locals())
def handler500(request, exception):
    return render(request, 'errors/500.html', locals())