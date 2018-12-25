from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import BusinessForm, UpdateProfileForm
from app.models import User,Countries, States, Cities,Category, Website, Business, Media, Referer, Thumsup, Keyword, Location
from .rating import calculate_rating, get_calculate_rating
import time, magic, uuid, urllib.parse, urllib.request
from bizrefpro.settings import BASE_DIR
import os, json, datetime
from app.bizrefpro_mail import send_invitation


def dashboard(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    else:
        user = User.objects.get(id= request.session['id'])
        signupDate = user.created_at.strftime("%d-%m-%Y")
        expiryDate = user.created_at+datetime.timedelta(days=364)
        expiryDate = expiryDate.strftime("%d-%m-%Y")
        doc_points = 0
        businesses = Business.objects.filter(user=user)
        for business in businesses:
            doc_points += (get_calculate_rating(business.id) + business.thumbs_up)
        status = ""
        if user.active == True:
            status = "Active"
        else:
            status = "Not Active"
        if user.user_type == "f":
            accountType = "Free"
        else:
            accountType = "Paid"
        if user.member_type == 'l':
            expiryDate = '-'
        return render(request, "user/index.html", {"user":user,"expiryDate":expiryDate,"docPoint":doc_points, "amount":user.amount,"accountType":accountType,"status":status, "created_at":signupDate,"title": "Best Business Referral Program | Destination to Grow Business"})

def profile(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    else:
        user = User.objects.get(id=request.session['id']);
        countries = Countries.objects.all()
        states = States.objects.all()
        cities = Cities.objects.all()
        form = UpdateProfileForm()
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST)
            if form.is_valid():
                user.name = form.cleaned_data["name"]
                user.phone = form.cleaned_data["phone"]
                user.address1 = form.cleaned_data["address1"]
                user.address2 = form.cleaned_data["address2"]
                try:
                   user.country = Countries.objects.get(id=request.POST["country"])
                except:
                    user.country = None
                try:
                    user.state = States.objects.get(id=request.POST["state"])
                except:
                    user.state = None
                
                user.city = form.cleaned_data["city"]
                user.save()
                messages.success(request, 'Profile details updated.')
                mime = magic.Magic(mime=True)
                if "pancard" in request.FILES:
                    pancard = request.FILES['pancard']
                    mimetype = mime.from_buffer(pancard.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(pancard)
                        try:
                            #check if media already exists then update it
                            media = Media(title="pancard", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="pancard",path=fileName,user=user, media_type=mimetype,verified=1, ref_type="user")
                            media.save();
                if "dl" in request.FILES:
                    dl = request.FILES['dl']
                    mimetype = mime.from_buffer(dl.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(dl)
                        try:
                            #check if media already exists then update it
                            media = Media(title="dl", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="dl",path=fileName,user=user, media_type=mimetype, verified=1, ref_type="user")
                            media.save();
                if "aadhar" in request.FILES:
                    aadhar = request.FILES['aadhar']
                    mimetype = mime.from_buffer(aadhar.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(aadhar)
                        try:
                            #check if media already exists then update it
                            media = Media(title="aadhar", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="aadhar",path=fileName,user=user, media_type=mimetype, verified=1, ref_type="user")
                            media.save();
                if "voterid" in request.FILES:
                    voterid = request.FILES['voterid']
                    mimetype = mime.from_buffer(voterid.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(voterid)
                        try:
                            #check if media already exists then update it
                            media = Media(title="voterid", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="voterid",path=fileName,user=user, media_type=mimetype,verified=1, ref_type="user")
                            media.save();

                if "electricity" in request.FILES:
                    electricity = request.FILES['electricity']
                    mimetype = mime.from_buffer(electricity.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(electricity)
                        try:
                            #check if media already exists then update it
                            media = Media(title="electricity", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="electricity",path=fileName,user=user, media_type=mimetype,verified=1, ref_type="user")
                            media.save();
                if "passport" in request.FILES:
                    passport = request.FILES['passport']
                    mimetype = mime.from_buffer(passport.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(passport)
                        try:
                            #check if media already exists then update it
                            media = Media(title="passport", user=user, ref_type="user")
                            oldfile = media.path
                            media.path = fileName
                            media.media_type = mimetype
                            media.verified = 1
                            media.save()
                            #deleting old file
                            try:
                                os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                            except OSError:
                                pass
                        except:
                            #save new media
                            media = Media(title="passport",path=fileName,user=user, media_type=mimetype, verified=1, ref_type="user")
                            media.save();
        try:   
            passport = Media.objects.get(title="passport", user=user, ref_type="user")
        except:
            passport = None
        try:
            pancard = Media.objects.get(title="pancard", user=user, ref_type="user")
        except:
            pancard = None
        try:
            dl = Media.objects.get(title="dl", user=user, ref_type="user")
        except:
            dl =None
        try:
            aadhar = Media.objects.get(title="aadhar", user=user, ref_type="user")
        except:
            aadhar = None
        try:
            voterid = Media.objects.get(title="voterid", user=user, ref_type="user")
        except:
            voterid = None
        try:
            electricity = Media.objects.get(title="electricity", user=user, ref_type="user")
        except:
            electricity = None
        pageContext = {"title": "Best Business Referral Program | Destination to Grow Business", "countries":countries,"states":states,"cities":cities}
        user = User.objects.get(id=request.session['id']);
        pageContext["user"] = user
        pageContext["form"] = form
        pageContext["pancard"] = pancard
        pageContext["dl"] = dl
        pageContext["aadhar"] = aadhar
        pageContext["passport"] = passport
        pageContext["voterid"] = voterid
        pageContext["electricity"] = electricity
        return render(request, "user/profile.html",pageContext)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")


def manage_website(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    else:
        user = User.objects.get(id=request.session['id'])
        websites = Website.objects.filter(user=user)
        return render(request, "user/manage-website.html", {"title": "Manage Website", "message_type":"","websites":websites})


def add_website(request):
    if "id" not in request.session:
            return HttpResponseRedirect('/login-register')
    else:
        if request.method == 'POST':
            user = User.objects.get(id=request.session['id'])
            uuidKey = uuid.uuid4().hex
            website = Website(name=request.POST['name'], verification_key=uuidKey,user=user)
            website.save()
            messages.success(request, 'Website Successfully Added.')
        categories = Category.objects.all()
        context = {"title": "Add Website", "message_type":"","categories":categories}
        return render(request, "user/add-website.html", context)

def edit_website(request,id):
        if "id" not in request.session:
            return HttpResponseRedirect('/login-register')
        else:
            if request.method == 'POST':
                website = Website.objects.get(id=id)
                website.name=request.POST['name']
                website.save()
                messages.success(request, 'Website Successfully Updated.')
            categories = Category.objects.all()
            website = Website.objects.get(id=id);
            url = urllib.parse.urljoin(website.name, website.verification_key+'.html')
            context = {"title": "Edit Website", "message_type":"","categories":categories,"website":website}
            context['url'] = url
            return render(request, "user/edit-website.html", context)


def improve_website(request):
        if "id" not in request.session:
            return HttpResponseRedirect('/login-register')
        else:
            return render(request, "user/improve-website.html", {"title": "Edit Website", "message_type":""})


def manage_business(request):
        if "id" not in request.session:
            return HttpResponseRedirect('/login-register')
        else:
            user = User.objects.get(id=request.session['id'])
            businesses = Business.objects.filter(user=user)
            return render(request, "user/manage-business.html", {"title": "Manage Business", "message_type":"","businesses":businesses})


def edit_business(request, id):
        if "id" not in request.session:
            return HttpResponseRedirect('/login-register')
        else:
            business = Business.objects.get(id=id)
            savedKeywords = business.keywords.all()
            countries = Countries.objects.all()
            states = States.objects.all()
            cities = Cities.objects.all()
            locations = Location.objects.all()
            form = BusinessForm()
            if request.method == "POST":
                form = BusinessForm(request.POST)
                if form.is_valid():
                    business.business_name = form.cleaned_data['business_name']
                    business.address1 = form.cleaned_data['address1']
                    business.address2 = form.cleaned_data['address2']
                    business.landmark = form.cleaned_data['landmark']
                    business.location = form.cleaned_data['location']
                    business.category_id = form.cleaned_data['category_id']
                    business.title = form.cleaned_data['title']
                    business.aboutus = form.cleaned_data['aboutus']
                    business.email = form.cleaned_data['email']
                    business.contact_number = form.cleaned_data['contact_number']
                    business.landline = form.cleaned_data['landline']
                    business.designation = form.cleaned_data['designation']
                    business.last_name = form.cleaned_data['last_name']
                    business.first_name = form.cleaned_data['first_name']
                    try:
                        country = Countries.objects.get(id=request.POST['country'])
                    except:
                        country = None
                    #try:
                    #    state = States.objects.get(id=request.POST['state'])
                    #except:
                    #    state = None
                    business.country = country
                    #business.state = state
                    business.state = request.POST['state']
                    #business.keyword = form.cleaned_data['keyword']
                    business.city = form.cleaned_data['city']
                    gst_value = ""
                    if form.cleaned_data['gst_no']:
                        gst_value = form.cleaned_data['gst_no']
                        if gst_value is None:
                            gst_value = ""
                    business.gst_no = gst_value
                    website = request.POST['website']
                    if website == "":
                        website = 0;
                    business.website = website
                    business.save()
                    business.keywords.set(request.POST.getlist('keywords'))
                    list_parent_category = []
                    for kid in request.POST.getlist('keywords'):
                        keyword = Keyword.objects.get(id=kid)
                        list_parent_category.append(keyword.category.id)
                    business.categories.set(list_parent_category)
                    business.state_list.set(request.POST.getlist('states'))
                    business.locations.set(request.POST.getlist('locations'))
                    messages.success(request, 'Business Successfully Updated.')
                    #saving attached media
                    mime = magic.Magic(mime=True)                    
                    if "pancard" in request.FILES:
                        pancard = request.FILES['pancard']
                        mimetype = mime.from_buffer(pancard.read())
                        if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                            fileName = handle_uploaded_file(pancard)
                            try:
                                media = Media.objects.get(title="pancard", business=business, ref_type="business")
                                oldfile = media.path
                                media.path = fileName
                                media.media_type=mimetype
                                media.verified = 1
                                media.save()
                                #deleting old file from system
                                try:
                                    os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                                except OSError:
                                    pass
                            except:
                                media = Media(title="pancard",path=fileName,business=business, media_type=mimetype, ref_type="business", verified=True)
                                media.save()
                    if "bankstatement" in request.FILES:
                        bankstatement = request.FILES['bankstatement']
                        mimetype = mime.from_buffer(bankstatement.read())
                        if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                            fileName = handle_uploaded_file(bankstatement)
                            try:
                                media = Media.objects.get(title="bankstatement", business=business, ref_type="business")
                                oldfile = media.path
                                media.path = fileName
                                media.media_type=mimetype
                                media.verified = 1
                                media.save()
                                #deleting old file from system
                                try:
                                    os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                                except OSError:
                                    pass
                            except:
                                media = Media(title="bankstatement",path=fileName,business=business, media_type=mimetype, ref_type="business", verified=True)
                                media.save()
                    if "rentagreement" in request.FILES:
                        rentagreement = request.FILES['rentagreement']
                        mimetype = mime.from_buffer(rentagreement.read())
                        if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                            fileName = handle_uploaded_file(rentagreement)
                            try:
                                media = Media.objects.get(title="rentagreement", business=business, ref_type="business")
                                oldfile = media.path
                                media.path = fileName
                                media.media_type=mimetype
                                media.verified = 1
                                media.save()
                                #deleting old file from system
                                try:
                                    os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                                except OSError:
                                    pass
                            except:
                                media = Media(title="rentagreement",path=fileName,business=business, media_type=mimetype, ref_type="business", verified=True)
                                media.save()

                    if "utilitybill" in request.FILES:
                        utilitybill = request.FILES['utilitybill']
                        mimetype = mime.from_buffer(utilitybill.read())
                        if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                            fileName = handle_uploaded_file(utilitybill)
                            try:
                                media = Media.objects.get(title="utilitybill", business=business, ref_type="business")
                                oldfile = media.path
                                media.path = fileName
                                media.media_type=mimetype
                                media.verified = 1
                                media.save()
                                #deleting old file from system
                                try:
                                    os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                                except OSError:
                                    pass
                            except:
                                media = Media(title="utilitybill",path=fileName,business=business, media_type=mimetype, ref_type="business", verified=True)
                                media.save()

                    if "registration_certificate" in request.FILES:
                        registration_certificate = request.FILES['registration_certificate']
                        mimetype = mime.from_buffer(registration_certificate.read())
                        if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                            fileName = handle_uploaded_file(registration_certificate)
                            try:
                                media = Media.objects.get(title="registration_certificate", business=business, ref_type="business")
                                oldfile = media.path
                                media.path = fileName
                                media.media_type=mimetype
                                media.verified = 1
                                media.save()
                                #deleting old file from system
                                try:
                                    os.remove(BASE_DIR+'/static/uploads/documents/'+oldfile)
                                except OSError:
                                    pass
                            except:
                                media = Media(title="registration_certificate",path=fileName,business=business, media_type=mimetype, ref_type="business", verified=True)
                                media.save()
                else:
                    print("Invalid form");    
            categories = Category.objects.filter(parent_id=0)
            user = User.objects.get(id=request.session['id'])
            websites = Website.objects.filter(user=user)
            calculate_rating(business_id=id)
            business = Business.objects.get(id=id)
            videos = Media.objects.filter(business=business,ref_type="business",media_type="video")            
            try:
                pancard = Media.objects.get(title="pancard", business=business, ref_type="business")
            except:
                pancard = None
            try:
                bankstatement = Media.objects.get(title="bankstatement", business=business, ref_type="business")
            except:
                bankstatement = None
            try:
                registration_certificate = Media.objects.get(title="registration_certificate", business=business, ref_type="business")
            except:
                registration_certificate = None
            try:
                utilitybill = Media.objects.get(title="utilitybill", business=business, ref_type="business")
            except:
                utilitybill = None
            try:
                rentagreement = Media.objects.get(title="rentagreement", business=business, ref_type="business")
            except:
                rentagreement = None
                
         
            myContext = {"title": "Manage Business", "message_type":"","business":business,"websites":websites, "form":form, "categories":categories,"countries":countries,"states":states,"cities":cities,"savedKeywords":savedKeywords, "locations":locations}
            myContext['vidoes'] = videos 
            myContext['pancard'] = pancard
            try:
                selectedCategories = business.categories.all().values_list('id', flat=True)
                myContext['selectedCategories'] = selectedCategories
                choosenCategory = Category.objects.get(id=business.category_id)
                myContext['category'] = choosenCategory
                subcategories = Category.objects.filter(parent_id=choosenCategory.id)
                myContext['subcategories'] = subcategories
                selected_locations = business.locations.all()
                myContext['selected_locations'] = selected_locations
            except:
                myContext['category'] = None
            myContext['bankstatement'] = bankstatement
            myContext['registration_certificate'] = registration_certificate
            myContext['utilitybill'] = utilitybill
            myContext['rentagreement'] = rentagreement 
            return render(request, "user/edit-business.html", myContext)


def add_business(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    else:
        categories = Category.objects.filter(parent_id=0)
        locations = Location.objects.all()
        user = User.objects.get(id=request.session['id'])
        websites = Website.objects.filter(user=user)
        countries = Countries.objects.all()
        states = States.objects.all()
        cities = Cities.objects.all()
        form = BusinessForm()
        if request.method == 'POST':
            form = BusinessForm(request.POST)
            #handle uploaded images
            if form.is_valid():
                videolist = []
                mime = magic.Magic(mime=True)
                vfiles = request.FILES.getlist('videos')
                mime = magic.Magic(mime=True)
                for f in vfiles:
                    mimetype = mime.from_buffer(f.read())
                    if mimetype in ["video/mp4"]:
                        videolist.append(handle_uploaded_file(f))
                try:
                    country = Countries.objects.get(id=request.POST['country'])
                except:
                    country = None
                #try:
                #    state = States.objects.get(id=request.POST['state'])
                #except:
                #    state = None
                state = request.POST['state']
                website = request.POST['website']
                if website == "":
                    website = 0
                gst_value=""
                if form.cleaned_data['gst_no']:
                    gst_value = form.cleaned_data['gst_no']
                business = Business(business_name=form.cleaned_data['business_name'],user=user,address1=form.cleaned_data['address1'],address2=form.cleaned_data['address2'], landmark=form.cleaned_data['landmark'], location=form.cleaned_data['location'],country=country, state=state, city=form.cleaned_data['city'], pincode=form.cleaned_data['pincode'], first_name =form.cleaned_data['first_name'], last_name =form.cleaned_data['last_name'], designation=form.cleaned_data['designation'],category_id=form.cleaned_data['category_id'],landline=form.cleaned_data['landline'],contact_number=form.cleaned_data['contact_number'],email=form.cleaned_data['email'],website=website, aboutus=form.cleaned_data['aboutus'],title=form.cleaned_data['title'],gst_no=gst_value)
                business.save()
                business.categories.set(request.POST.getlist('categories'))
                business.keywords.set(request.POST.getlist('keywords'))
                business.state_list.set(request.POST.getlist('states'))
                business.locations.set(request.POST.getlist('locations'))
                if "pancard" in request.FILES:
                    pancard = request.FILES['pancard']
                    mimetype = mime.from_buffer(pancard.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(pancard)
                        media = Media(title="pancard",path=fileName,business=business, media_type=mimetype,verified=1, ref_type="business")
                        media.save();
                if "bankstatement" in request.FILES:
                    bankstatement = request.FILES['bankstatement']
                    mimetype = mime.from_buffer(bankstatement.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(bankstatement)
                        media = Media(title="bankstatement",path=fileName,business=business, media_type=mimetype,verified=1, ref_type="business")
                        media.save();
                if "rentagreement" in request.FILES:
                    rentagreement = request.FILES['rentagreement']
                    mimetype = mime.from_buffer(rentagreement.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(rentagreement)
                        media = Media(title="rentagreement",path=fileName,business=business, media_type=mimetype,verified=1, ref_type="business")
                        media.save();

                if "utilitybill" in request.FILES:
                    utilitybill = request.FILES['utilitybill']
                    mimetype = mime.from_buffer(utilitybill.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(utilitybill)
                        media = Media(title="utilitybill",path=fileName,business=business, media_type=mimetype,verified=1, ref_type="business")
                        media.save();

                if "registration_certificate" in request.FILES:
                    registration_certificate = request.FILES['registration_certificate']
                    mimetype = mime.from_buffer(registration_certificate.read())
                    if mimetype in ["application/pdf", 'image/png', 'image/jpg', 'image/jpeg', 'image/gif']:
                        fileName = handle_uploaded_file(registration_certificate)
                        media = Media(title="registration_certificate",path=fileName,business=business, media_type=mimetype,verified=1, ref_type="business")
                        media.save();
                for video in videolist:
                    media = Media(title="",path=video,business=business, media_type="video",verified=1, ref_type="business")
                    media.save();
                messages.success(request, 'Business Successfully Added.')
                return redirect('/user/edit-business/'+str(business.id))
        return render(request, "user/add-business.html", {"title": "Add Business", "message_type":"", "form":form,"categories":categories,"websites":websites,"countries":countries,"states":states,"locations":locations,"cities":cities})


# method to handle file uploads
def handle_uploaded_file(f):
    nt = str(time.time())
    stamp = nt.replace(".","-")
    filename = stamp+"-"+f.name.replace(" ","-")
    filename = filename.replace(",","-")
    with open(BASE_DIR+'/static/uploads/documents/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


def delete_business(request, id):
    Business.objects.filter(id=id).delete()
    messages.success(request, 'Business Successfully Deleted.')
    return redirect('/user/manage-business')

def delete_website(request, id):
    Website.objects.filter(id=id).delete()
    messages.success(request, 'Website Successfully Deleted.')
    return redirect('/user/manage-website')

def download_verification_file(request, id):
    website = Website.objects.get(id=id)
    content = 'bizrefpro verification id:'+website.verification_key
    response = HttpResponse(content,content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename='+website.verification_key+".html"
    return response


def verify_site(request, id):
    website = Website.objects.get(id=id)
    url = urllib.parse.urljoin(website.name, website.verification_key+'.html')
    urlRequest = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(urlRequest)
        #print(type(response))
        #need to work for exact key validation validation
        website.verification_status = True
        website.save();
        messages.success(request, 'Website Successfully Verified.')
    except:
        print("something wrong")
        messages.error(request, 'Couldn\'t Verify the Website.')
    return redirect("/user/edit-website/"+str(website.id))


def add_member(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    else:
        if request.method == 'POST':
            try:
                user = User.objects.get(id=request.session['id'])
                name = request.POST['name']
                email = request.POST['email']
                phone = request.POST['phone']
                uuidKey = uuid.uuid4().hex
                try:
                   Referer.objects.get(email=email)
                   messages.error(request, 'User already registered')
                except:
                    referer = Referer(name=name,email=email,phone=phone,user=user,referer=uuidKey)
                    referer.save()
                    send_invitation(referer.name, referer.email, user.name, uuidKey)
                    messages.success(request, 'Invitation sent')
            except:
                pass
    return render(request, "user/add-member.html", {})

def manage_group(request):
    if "id" not in request.session:
        return HttpResponseRedirect('/login-register')
    return render(request, "user/manage-group.html", {})

def get_user_groupes(request):
    if "id" not in request.session:
        return HttpResponse(json.dumps([]))
    try:
        total_thumsup = 0
        total_thumsdown = 0
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        object_list = User.objects.filter(reference_id=request.session['id'])[start:start + length]  # or any kind of queryset
        total = User.objects.filter(reference_id=request.session['id']).count()
        list = []
        for object in object_list:
            thumbs_up = 0
            thumbs_down = 0
            busineses = Business.objects.filter(user=object)
            for business in busineses:
                thumbs_up += business.thumbs_up
                thumbs_down += business.thumbs_down
                total_thumsup = thumbs_up
                total_thumsdown = thumbs_down
            status = "Pending"
            if object.active == True:
                status = '<a href="#" data-id="'+str(object.id)+'" class="text-danger detach">Detach</a>'
            list.append({"name": object.name, "positive_points": '<a href="/user/view-review-detail/'+str(object.id)+'/positive">'+str(thumbs_up)+'</a>', "negative_points": '<a href="/user/view-review-detail/'+str(object.id)+'/negative">'+str(thumbs_down)+'</a>', "action":status})
        total_thumsup1 = 0
        total_thumsdown1 = 0
        document_point = 0
        try:
            thumbs_up = 0
            thumbs_down = 0
            current_user = User.objects.get(id=request.session['id'])
            busineses = Business.objects.filter(user=current_user)
            for business in busineses:
                thumbs_up += business.thumbs_up
                thumbs_down += business.thumbs_down
                total_thumsup1 = thumbs_up
                total_thumsdown1 = thumbs_down
                document_point += get_calculate_rating(business.id)
            list.append({"name": current_user.name, "positive_points": '<a href="/user/view-review-detail/'+str(current_user.id)+'/positive">'+str(thumbs_up)+'</a>', "negative_points": '<a href="/user/view-review-detail/'+str(current_user.id)+'/negative">'+str(thumbs_down)+'</a>', "action":'<a href="#" data-id="'+str(current_user.id)+'" class="text-danger">--</a>'})
        except:
            None
        total_positive = total_thumsup+total_thumsup1
        total_negative = total_thumsdown+total_thumsdown1
        list.append({"name": '<h4>Rating Point</h4>', "positive_points":str(total_positive), "negative_points": total_negative, "action":"<!--<strong>"+str(total_positive-total_negative)+"</strong> (Positive-Negative)-->"})
        list.append({"name": 'Doc Point', "positive_points":str(document_point) , "negative_points": "", "action":""})
        list.append({"name": '<h4>Total Point</h4>', "positive_points":str(total_positive+document_point) , "negative_points": "", "action":"<!--<strong>"+str((total_positive+document_point)-total_negative)+"</strong>-->"})
        business = Business
        mdict = {"data": list}
        mdict['draw'] = request.GET['draw']
        mdict['recordsTotal'] = total  # show from how many record its filtered.
        mdict['recordsFiltered'] = total  # show how many record filtered.
        return HttpResponse(json.dumps(mdict))
    except:
        return HttpResponse(json.dumps([]))



def detach_user(request):
    if "id" not in request.session:
        return HttpResponse(json.dumps([]))
    try:
       id = request.GET['id'];
       user = User.objects.get(id=id)
       user.reference_id = 0
       user.save()
    except:
        pass
    return HttpResponse(json.dumps([]))

def view_review_detail(request, id, review_type):
    context = {}
    context['id'] = id;
    context['review_type'] = review_type;
    return render(request, "user/view-review-detail.html", context)

def get_business_review(request, id, review_type):
    list = []
    user = User.objects.get(id=id)
    businesses = Business.objects.filter(user=user)
    count = 0
    for business in businesses:
        if review_type == "positive":
            thumsup = Thumsup.objects.filter(business_id=business.id,thumbs_up=1)
        else:
            thumsup = Thumsup.objects.filter(business_id=business.id,thumbs_down=1)
        for thumsObj in thumsup:
            count = count+1
            uObj = User.objects.get(email=thumsObj.email)
            list.append({"name":uObj.name, "email":uObj.email, "state":uObj.state.name})
    mdict = {"data": list}
    mdict['draw'] = request.GET['draw']
    mdict['recordsTotal'] = count  # show from how many record its filtered.
    mdict['recordsFiltered'] = count  # show how many record filtered.
    return HttpResponse(json.dumps(mdict))

def get_envitations(request):
    if "id" not in request.session:
        return HttpResponse(json.dumps([]))
    try:
       mdict = {}
       user = User.objects.get(id=request.session['id'])
       start = int(request.GET['start'])
       length = int(request.GET['length'])
       referers = Referer.objects.filter(user=user).exclude(referer="").order_by('-id')[start:start+length]
       count = Referer.objects.filter(user=user).exclude(referer="").count()
       list = []
       for obj in referers:
           list.append({"name":obj.name, "email":obj.email, "phone":obj.phone})
       mdict = {"data": list}
       mdict['draw'] = request.GET['draw']
       mdict['recordsTotal'] = count  # show from how many record its filtered.
       mdict['recordsFiltered'] = count  # show how many record filtered.
       return HttpResponse(json.dumps(mdict))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps([]))

