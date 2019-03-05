from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserForm, ContactForm, RefererForm
from .models import User, Business, Executive, Contact, Website, SearchAnalytics
from .models import Category, States, Otp, Thumsup, Zones, Media, Referer, Keyword, Countries, Location
from django.contrib import messages
import uuid, os
from urllib.request import urlopen
import urllib.parse
import json
from bizrefpro.settings import BASE_DIR
from random import randint
from django.utils import timezone
from datetime import timedelta
import datetime
from .bizrefpro_mail import send_enquiry_email, send_userforget_password_link_mail, send_otp, send_otp_for_referral, \
    BizEmailService
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db.models import Q
from app.bizrefpro_mail import send_invitation


# Create your views here.
def index(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business"}
    return render(request, "app/index.html", page_context)


def contact(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Contact Us"}
    if request.method == "POST":
        cform = ContactForm(request.POST)
        if cform.is_valid():
            contact = Contact(name=cform.cleaned_data['name'], email=cform.cleaned_data['email'],
                              contact=cform.cleaned_data['contact'], message=cform.cleaned_data['message'])
            contact.save()
            messages.add_message(request, messages.SUCCESS, 'Enquiry Sent Successfully')

    return render(request, "app/contact.html", page_context)


def pricing(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Pricing"}
    return render(request, "app/pricing.html", page_context)


def csr(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Corporate Social Responsibility"}
    return render(request, "app/csr.html", page_context)


def why_we(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Why We"}
    return render(request, "app/why-we.html", page_context)


def privacy(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Privacy"}
    return render(request, "app/privacy-policy.html", page_context)


def terms(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Terms"}
    return render(request, "app/terms.html", page_context)


def franchise(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Franchise"}
    return render(request, "app/franchise.html", page_context)


def about(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "About Us"}
    return render(request, "app/about-us.html", page_context)


def faq(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Faq"}
    return render(request, "app/faq.html", page_context)


def how_it_work(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "How It Works"}
    return render(request, "app/why-join.html", page_context)


def refer_friend(request):
    page_context = dict()
    page_context["title"]= "Best Business Referral Program | Destination to Grow Business"
    page_context["pageTitle"]= "Refer Friend"
    page_context['page'] = "refer_friend"
    return render(request, "app/refer_friend.html", page_context)


def plan(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "How It Works"}
    return render(request, "app/plan.html", page_context)


def news(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "News"}
    return render(request, "app/news.html", page_context)


def career(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Career"}
    return render(request, "app/career.html", page_context)


def search_result(request):
    if "q" not in request.GET:
        return HttpResponseRedirect("/")
    page_context = dict()
    page_context["title"] = "Best Business Referral Program | Destination to Grow Business"
    page_context["pageTitle"]= "Search Result"
    page_context['page'] = "search"
    page_context['page_tag'] = 'Showing result of "' + request.GET['q'] + '"'
    page_context['qpart1'] = request.GET['q']
    page_context['qpart2'] = ""
    if 'location' in request.GET:
        page_context['qpart2'] = request.GET['location']
    return render(request, "app/search-result.html", page_context)


def search(request):
    queryString = request.GET['q']
    location = ""
    if 'location' in request.GET:
        location = request.GET['location']
    stop_words = set(stopwords.words('english'))
    stop_words.add("top")
    word_tokens = word_tokenize(queryString)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    mmlength = len(filtered_sentence)
    queryString = ' '.join(filtered_sentence)
    if location == "" or location == None:
        queryParam = {"q": 'keywords:' + queryString, "defType": "edismax", "qf": "keywords", "mm": mmlength,
                      'sort': "rank desc"}
    else:
        queryParam = {"q": 'keywords:' + queryString, "fq": 'locations:' + location, "defType": "edismax",
                      "qf": "keywords", "mm": mmlength, 'sort': "rank desc"}
    url = "http://localhost:8983/solr/collection1/select?" + urllib.parse.urlencode(queryParam) + "&wt=json"
    webURL = urlopen(url)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    return HttpResponse(json.dumps(JSON_object), content_type='application/json')


def search_result_test(request):
    if "q" not in request.GET:
        return HttpResponseRedirect("/")
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "Search Result"}
    page_context['page'] = "search";
    page_context['qpart1'] = request.GET['q'];
    page_context['qpart2'] = request.GET['location']
    return render(request, "app/search-result-test.html", page_context)


def hosting_features(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "Hosting Features"}
    return render(request, "app/hosting-features.html", page_context)


def login_register(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Login"}
    states = States.objects.filter(country_id=1)
    page_context['states'] = states;
    if request.method == 'POST':
        if request.POST['form_type'] == "signup":
            try:
                user = User.objects.get(email=request.POST['email'])
                page_context['message_type'] = "failed"
                page_context['message'] = "Email Address Already Exists"
                return render(request, "app/login-register.html", page_context)
            except:
                country = Countries.objects.get(id=1)
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
                            zone = Zones.objects.get(id=request.POST['zone'])
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
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), state=state, zone=zone, address1="",
                                        address2="", city="", executive=executive, reference_id=referer_id, active=True)
                            referer_object.referer = ""
                            referer_object.save()
                        except:
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), country=country, state=state,
                                        zone=zone, address1="", address2="", city="", executive=executive, active=True)
                    else:
                        try:
                            referer_object = Referer.objects.get(phone=uform.cleaned_data['phone'])
                            referer_id = referer_object.user.id
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), state=state, zone=zone, address1="",
                                        address2="", city="", executive=executive, reference_id=referer_id, active=True)
                            referer_object.referer = ""
                            referer_object.save()
                        except Exception as e:
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), country=country, state=state,
                                        zone=zone, address1="", address2="", city="", executive=executive, active=True)
                    user.save()
                    bizmail = BizEmailService();
                    # bizmail.send_signup_notification_to_admin(user=user)
                    bizmail.send_approval_notification_to_user(user, uform.cleaned_data['password'])
                    page_context['message_type'] = "success"
                    page_context['message'] = "Registered Successfully"
                    messages.success(request,
                                     'Success! Your Application has been submitted successfully. Please login and complete your profile.')
                    # return render(request, "app/login-register.html", page_context)
                    return HttpResponseRedirect("/registration-success")
                else:
                    # return HttpResponse('POST method'+request.POST['name'])
                    # request.session['name'] ="Session Created";
                    page_context['message_type'] = "failed"
                    page_context['message'] = "Something Went wrong"
                    return render(request, "app/login-register.html", page_context)
        if request.POST['form_type'] == "signin":
            try:
                user = User.objects.get(email=request.POST['email'])
                if check_password(request.POST['password'], user.password):
                    if user.deleted is True:
                        page_context['message_type'] = "failed"
                        page_context['message'] = "Account has been deleted"
                        return render(request, "app/login-register.html", page_context)
                    elif user.active == False:
                        page_context['message_type'] = "failed"
                        page_context['message'] = "Your Profile is disabled Contact customer care to approve"
                        return render(request, "app/login-register.html", page_context)
                    else:
                        request.session['id'] = user.id
                        return HttpResponseRedirect('user/dashboard')
                else:
                    page_context['message_type'] = "failed"
                    page_context['message'] = "Incorrect username and password"
                    return render(request, "app/login-register.html", page_context)
            except:
                page_context['message_type'] = "failed"
                page_context['message'] = "Incorrect username and password"
                return render(request, "app/login-register.html", page_context)
    page_context['message_type'] = ""
    return render(request, "app/login-register.html", page_context)


def register(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business", "pageTitle": "Register"}
    states = States.objects.filter(country_id=1)
    page_context['states'] = states;
    if request.method == 'POST':
        if request.POST['form_type'] == "signup":
            try:
                user = User.objects.get(email=request.POST['email'])
                page_context['message_type'] = "failed"
                page_context['message'] = "Email Address Already Exists"
                return render(request, "app/register.html", page_context)
            except:
                try:
                    user = User.objects.get(phone=request.POST['phone'])
                    page_context['message_type'] = "failed"
                    page_context['message'] = "Contact Number Already Exists"
                    return render(request, "app/register.html", page_context)
                except Exception as e:
                    pass
                country = Countries.objects.get(id=1)
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
                            zone = Zones.objects.get(id=request.POST['zone'])
                        except:
                            zone = None
                    if request.POST['executive'] == 0:
                        executive = None
                    else:
                        try:
                            executive = Executive.objects.get(id=request.POST['executive'], secret_code=request.POST['secret_code'])
                        except:
                            page_context['message_type'] = "failed"
                            page_context['message'] = "Incorrect executive secret code"
                            return render(request, "app/register.html", page_context)
                            executive = None
                    if 'referer' in request.GET:
                        referer = request.GET['referer']
                        try:
                            referer_object = Referer.objects.get(referer=referer)
                            referer_id = referer_object.user.id
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), state=state, zone=zone, address1="",
                                        address2="", city="", executive=executive, reference_id=referer_id, active=True)
                            referer_object.referer = ""
                            referer_object.save()
                        except:
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), country=country, state=state,
                                        zone=zone, address1="", address2="", city="", executive=executive, active=True)
                    else:
                        try:
                            referer_object = Referer.objects.get(phone=uform.cleaned_data['phone'])
                            referer_id = referer_object.user.id
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), state=state, zone=zone, address1="",
                                        address2="", city="", executive=executive, reference_id=referer_id, active=True)
                            referer_object.referer = ""
                            referer_object.save()
                        except Exception as e:
                            user = User(name=uform.cleaned_data['name'], phone=uform.cleaned_data['phone'],
                                        email=uform.cleaned_data['email'],
                                        password=make_password(password=uform.cleaned_data['password'], salt=None,
                                                               hasher="bcrypt"), country=country, state=state,
                                        zone=zone, address1="", address2="", city="", executive=executive, active=True)
                    user.save()
                    bizmail = BizEmailService()
                    bizmail.send_signup_notification_to_admin(user=user)
                    bizmail.send_approval_notification_to_user(user, uform.cleaned_data['password'])
                    if executive is not None:
                        bizmail.send_signup_notification_to_executive(user=user, executive=executive)

                    page_context['message_type'] = "success"
                    page_context['message'] = "Registered Successfully"
                    messages.success(request,
                                     'Success! Your Application has been submitted successfully. Please login and complete your profile.')
                    # return render(request, "app/login-register.html", page_context)
                    return HttpResponseRedirect("/registration-success")
                else:
                    # return HttpResponse('POST method'+request.POST['name'])
                    # request.session['name'] ="Session Created";
                    page_context['message_type'] = "failed"
                    page_context['message'] = "Something Went wrong"
                    return render(request, "app/register.html", page_context)
        if request.POST['form_type'] == "signin":
            try:
                user = User.objects.get(email=request.POST['email'])
                if check_password(request.POST['password'], user.password):
                    if user.deleted is True:
                        page_context['message_type'] = "failed"
                        page_context['message'] = "Account has been deleted"
                        return render(request, "app/login-register.html", page_context)
                    elif user.active == False:
                        page_context['message_type'] = "failed"
                        page_context['message'] = "Your Profile is disabled Contact customer care to approve"
                        return render(request, "app/login-register.html", page_context)
                    else:
                        request.session['id'] = user.id
                        return HttpResponseRedirect('user/dashboard')
                else:
                    page_context['message_type'] = "failed"
                    page_context['message'] = "Incorrect username and password"
                    return render(request, "app/login-register.html", page_context)
            except:
                page_context['message_type'] = "failed"
                page_context['message'] = "Incorrect username and password"
                return render(request, "app/login-register.html", page_context)
    page_context['message_type'] = ""
    return render(request, "app/register.html", page_context)


def forgot_password(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "Forgot Password"}
    return render(request, "app/forgot_password.html", page_context)


def registration_success(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "Registration Success"}
    return render(request, "app/registration-successful.html", page_context)


def reset_link(request):
    email = request.POST['email']
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
        page_context = dict()
        page_context["title"] = "Best Business Referral Program | Destination to Grow Business"
        page_context["pageTitle"] = "Password Reset"
        page_context["msg_type"] = ''
        page_context['showForm'] = True
        if request.method == 'POST':
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            if password == cpassword:
                user.password = make_password(password=cpassword, salt=None, hasher="bcrypt")
                user.verification_key = ""
                user.save()
                page_context['msg_type'] = 'success'
                page_context['showForm'] = False
                page_context['message'] = 'Password has been reset successfully'
            else:
                page_context['msg_type'] = 'failure'
                page_context['showForm'] = True
                page_context['message'] = 'Both password didn\'t match'
        return render(request, "app/password-reset.html", page_context)
    except:
        page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                        "pageTitle": "Link Expired"}
        return render(request, "app/link-rexpired.html", page_context)


def ssl_validation(request):
    return HttpResponse("D7A6A1569AF33477127AB63D7E1C2ECE34978E0B814DF205790B1311A67CA0B3 comodoca.com 5b4825a5529ea")


def bizrefpro_promotions(request):
    page_context = {"title": "Best Business Referral Program | Destination to Grow Business",
                    "pageTitle": "Forgot Password"}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        if name == "" or phone == "":
            return render(request, "promotions/index.html", page_context)
        else:
            send_enquiry_email(name, email, phone, location)
            return render(request, "promotions/success.html", page_context)

    else:
        return render(request, "promotions/index.html", page_context)


def send_thumbsup_otp(request):
    resp = dict()
    email = request.GET['email']
    business_id = request.GET['business_id']
    otp_number = randint(100000, 999999)
    try:
        try:
            User.objects.get(email=email)
            otp = Otp(otp=otp_number, email=email, business_id=business_id)
            otp.save()
            send_otp(email, otp_number)
        except:
            resp['status'] = "failed"
            resp["message"] = "Please enter registered Email ID"
    except:
        resp['status'] = "failed"
        resp["message"] = "Error occured"
    return HttpResponse(json.dumps(resp))


def send_refer_otp(request):
    resp = dict()
    email = request.GET['email']
    try:
        user = User.objects.get(email=email)
        otp_number = randint(100000, 999999)
        try:
            otp = Otp(otp=otp_number, email=email)
            otp.save()
            send_otp_for_referral(email, otp_number)
            resp['status'] = "success"
            resp["message"] = "Otp successfully sent"
        except Exception as ex:
            print(ex)
            resp['status'] = "failed"
            resp["message"] = "Unknown Error Occured"
    except Exception as ex:
        resp['status'] = "failed"
        resp["message"] = "You are not registered"
    return HttpResponse(json.dumps(resp), content_type="application/json")


def referabusiness(request):
    resp = dict()
    if request.method == "POST":
        form = RefererForm(request.POST)
        if form.is_valid():
            count = Otp.objects.filter(otp=form.cleaned_data['otp'], email=form.cleaned_data['referer_email']).count()
            print(count)
            if count > 0:
                try:
                    user = User.objects.get(email=form.cleaned_data['referer_email'])
                    referer_count = Referer.objects.filter(name=form.cleaned_data['name']).filter(Q(email=form.cleaned_data['email'])|Q(phone=form.cleaned_data['contact'])).count()
                    if referer_count == 0:
                        referer = Referer(name=form.cleaned_data['name'], email=form.cleaned_data['email'], phone=form.cleaned_data['contact'], user=user)
                        referer.save()
                        bizrefpro_email = BizEmailService()
                        bizrefpro_email.notify_referred_to_admin(referer,user)
                        if referer.email not in ["", None]:
                            uuid_key = uuid.uuid4().hex
                            send_invitation(referer.name, referer.email, user.name, uuid_key)
                        resp['message'] = "Reference is sent successfully"
                        resp['success'] = True
                    else:
                        resp['message'] = "Already refered"
                        resp['success'] = False
                except User.DoesNotExist:
                    resp['message'] = "Referal email does not exists"
                    resp['success'] = False
            else:
                resp['message'] = "Incorrect Otp"
                resp['success'] = False
        else:
            resp['errors'] = form.errors
            resp['message'] = "Invalid Form"
    else:
        resp['success'] = True
    return HttpResponse(json.dumps(resp), content_type="application/json")


def thums_up(request):
    resp = {}
    otp = request.GET['otp'];
    email = request.GET['email'];
    business_id = request.GET['business_id'];
    time_threshold = timezone.now() - timedelta(minutes=5)
    Otp.objects.filter(created_at__lt=time_threshold).delete()
    try:
        otp_count = Otp.objects.filter(otp=otp, business_id=business_id).count()
        if otp_count > 0:
            try:
                tup = Thumsup.objects.get(email=email, business_id=business_id, thumbs_up=1)
                resp['status'] = "failed"
                resp["message"] = "Your review has been already submitted"
            except:
                thumsup = Thumsup(email=email, business_id=business_id, thumbs_up=1)
                thumsup.save()
                business = Business.objects.get(id=business_id)
                business.thumbs_up += 1
                business.save()
                resp['status'] = "success"
                resp["message"] = "You have successfully submitted your rating."
        else:
            resp['status'] = "failed"
            resp["message"] = "This otp might be expired or incorrect."
    except:
        resp['status'] = "failed"
        resp["message"] = "This otp might be expired or incorrect."
    return HttpResponse(json.dumps(resp))


def thums_down(request):
    resp = {}
    otp = request.GET['otp'];
    email = request.GET['email'];
    business_id = request.GET['business_id'];
    time_threshold = timezone.now() - timedelta(minutes=5)
    Otp.objects.filter(created_at__lt=time_threshold).delete()
    try:
        otp_count = Otp.objects.filter(otp=otp, business_id=business_id).count()
        if otp_count > 0:
            try:
                thumsup = Thumsup.objects.get(email=email, business_id=business_id, thumbs_down=1)
                resp['status'] = "failed"
                resp["message"] = "Your review has been already submitted"
            except:
                thumsup = Thumsup(email=email, business_id=business_id, thumbs_down=1)
                thumsup.save()
                business = Business.objects.get(id=business_id)
                business.thumbs_down += 1
                business.save()
                resp['status'] = "success"
                resp["message"] = "You have successfully submitted your rating"
        else:
            resp['status'] = "failed"
            resp["message"] = "This otp might be expired or incorrect."
    except:
        resp['status'] = "failed"
        resp["message"] = "This otp might be expired or incorrect."
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
            if os.path.exists(BASE_DIR + '/static/uploads/documents/' + media.path):
                os.remove(BASE_DIR + '/static/uploads/documents/' + media.path)
            media.delete()
        except:
            None
    resp['status'] = "success"
    return HttpResponse(json.dumps(resp))


def autocomplete(request):
    resp = []
    search_text = request.GET['term']
    keywords = Keyword.objects.filter(name__icontains=search_text).exclude(deleted=True)[:10]
    for keyword in keywords:
        resp.append({"id": keyword.name, "value": keyword.name, "label": keyword.name})
    return HttpResponse(json.dumps(resp))


def location_autocomplete(request):
    resp = []
    search_text = request.GET['term']
    locations = Location.objects.filter(name__icontains=search_text).exclude(deleted=True)[:10]
    for location in locations:
        resp.append({"id": location.name, "value": location.name, "label": location.name})
    return HttpResponse(json.dumps(resp))


def import_csv(request):
    """
    used for temporary data import
    :param request:
    :return HttpResponse:
    """
    '''
       with open(BASE_DIR + '/static/uploads/category-sub-keyword.csv') as csv_file:
           csv_reader = csv.reader(csv_file, delimiter=',')
           parent_category = "";
           child_category = "";
           for row in csv_reader:
               if row[0] not in ["", None] and row[1] in ["", None] and row[2] in ["", None]:
                   parent_category = Category(name=row[0], parent_id=0, active=1)
                   parent_category.save()
               if row[0] in ["", None] and row[1] not in ["", None] and row[2] in ["", None]:
                   child_category = Category(name=row[1], parent_id=parent_category.id, active=1)
                   child_category.save()
               if row[0] in ["", None] and row[1] in ["", None] and row[2] not in ["", None]:
                   keyword = Keyword(name=row[2], category=child_category, active=True)
                   keyword.save()
       return HttpResponse("ok")
       '''
    return HttpResponse("Already Imported")


def dispaly_business(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except:
        pass
    businesses = Business.objects.filter(category_id=category_id, active=True, deleted=False).order_by('-search_ranking')
    docs = []
    page_context = dict()
    for business in businesses:
        group_rating = calculate_group_rating(business)
        business_points = business.rating + business.thumbs_up + group_rating
        down_rating = calculate_group_thumbs_down_rating(business)
        website = ""
        try:
            web = Website.objects.get(id=business.website)
            website = web.name
        except Exception as ex:
            print("exception(No website)", ex)
        docs.append({
            "id": business.id,
            "title": business.title,
            "description": business.aboutus,
            "address": business.address1,
            "website": website,
            "business_id": business.id,
            "thumbs_down": str(business.thumbs_down + down_rating),
            "contact": str(business.contact_number),
            "rank": str(business_points)
        })

    page_context['docs'] = docs
    page_context['page'] = "search"
    try:
        category
        page_context['page_tag'] = 'Showing result of "' + category.name + '"'
    except NameError as e:
        print(e)
    page_context['doc_len'] = len(docs)
    return render(request, "app/category-data.html", page_context)


def search_analytics(request):
    if "q" in request.GET:
        search_query = request.GET['q']
        today = datetime.date.today()
        try:
            analytics = SearchAnalytics.objects.get(search_keywords=search_query, analytics_date=today)
            analytics.search_counter = analytics.search_counter + 1
            analytics.save()
        except SearchAnalytics.DoesNotExist:
            analytics = SearchAnalytics(search_keywords=search_query, analytics_date=today)
            analytics.save()
    return HttpResponse("ok")





# error handlers
def handler404(request, exception):
    return render(request, 'errors/404.html', locals())


def handler400(request, exception):
    return render(request, 'errors/400.html', locals())


def handler500(request, exception):
    return render(request, 'errors/500.html', locals())


def calculate_group_rating(business):
    points = 0
    if business is not None:
        total_thumbs_up = 0
        user_id = business.user.id
        object_list = User.objects.filter(reference_id=user_id)
        for object in object_list:
            thumbs_up = 0
            businesses = Business.objects.filter(user=object)
            for business in businesses:
                if business.active is True:
                    thumbs_up += business.thumbs_up
                    total_thumbs_up += thumbs_up
        points = total_thumbs_up
    return points


def calculate_group_thumbs_down_rating(business):
    points = 0
    if business is not None:
        total_thumbs_down = 0
        user_id = business.user.id
        object_list = User.objects.filter(reference_id=user_id)
        for object in object_list:
            thumbs_down = 0
            businesses = Business.objects.filter(user=object)
            for business in businesses:
                if business.active is True:
                    thumbs_down += business.thumbs_down
                    total_thumbs_down += thumbs_down
        points = total_thumbs_down
    return points
