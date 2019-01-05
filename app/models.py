from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
        name = models.CharField(max_length=100)
        slug = models.CharField(max_length=100)
        parent_id = models.IntegerField(default=0)
        active = models.BooleanField(default=True)
        deleted = models.BooleanField(default=False)

        def __str__(self):
            return self.name


class Keyword(models.Model):
        name = models.CharField(max_length=150)
        slug = models.CharField(max_length=100)
        category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
        active = models.BooleanField(default=True)
        deleted = models.BooleanField(default=False)

        def __str__(self):
            return self.name


class User(models.Model):
    MAYBECHOICE = (('f', 'Free'), ('p', 'Paid'),)
    PAYMENTMODES = (('n', 'Net Banking'), ('c', 'Cash'), ('w', 'Cheque/Wire'),('e', 'ECS'),)
    MEMBERSHIPTYPES = (('l', 'LifeTime'), ('y', 'Yearly'),)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=120)
    phone = models.CharField(max_length=12, blank=True, null=True)
    address1 = models.CharField(max_length=120, blank=True, null=True)
    address2 = models.CharField(max_length=120, blank=True, null=True)
    country = models.ForeignKey('Countries',on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    zone = models.ForeignKey('Zones',on_delete=models.SET_NULL, null=True)
    executive = models.ForeignKey('Executive',on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=120,default="", blank=True, null=True)
    verification_key = models.CharField(max_length=100, default="", blank=True, null=True)
    reference_id = models.CharField(max_length=50, default="", blank=True, null=True)
    amount = models.FloatField(default=0.0)
    user_type = models.CharField(max_length=1, choices=MAYBECHOICE, default = 'f')
    payment_mode = models.CharField(max_length=1, choices=PAYMENTMODES, default='n')
    member_type = models.CharField(max_length=1, choices=MEMBERSHIPTYPES, default='l')
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField('date created', default=timezone.now)
    
    def __str__(self):
        return self.name


class Website(models.Model):
        name = models.CharField(max_length=150)
        verification_key = models.CharField(max_length=100)
        user = models.ForeignKey(User,on_delete=models.DO_NOTHING)        
        category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
        verified = models.BooleanField(default=False)
        created_at = models.DateTimeField('date created', default=timezone.now)
        active = models.BooleanField(default=False)
        deleted = models.BooleanField(default=False)
        
        def __str__(self):
            return self.name


class Business(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    business_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey('Countries',on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    state = models.CharField(max_length=100, default="", blank=True, null=True)
    city =  models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    landline = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.IntegerField(default=0)
    aboutus = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    state_list = models.ManyToManyField('States')
    locations = models.ManyToManyField('Location')
    gst_no = models.CharField(max_length=30, default="", blank=True, null=True)
    rating = models.IntegerField(default=10)
    categories = models.ManyToManyField('Category')
    category_id = models.IntegerField(default=0)
    keywords = models.ManyToManyField('Keyword')
    created_at = models.DateTimeField('date created', default=timezone.now)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
            return self.business_name


class Media(models.Model):
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    default = models.CharField(max_length=10)
    media_type = models.CharField(max_length=200)
    user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True,default=None)
    business = models.ForeignKey('Business',on_delete=models.SET_NULL, null=True,default=None)
    ref_type = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField('date created', default=timezone.now)


class Countries(models.Model):
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=150)
    phonecode = models.IntegerField()
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class States(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey('Countries',on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

# backward compatibility will be removed later
class Cities(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Zones(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# used for search
class BizRefProSearch(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=355)
    address = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255, default="")
    website = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    rank = models.IntegerField(default=0)
    business_id = models.IntegerField(default=0)
    created_at = models.DateTimeField('date created', default=timezone.now)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length = 15)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField('date created', default=timezone.now)
    active = models.BooleanField(default=False)

    def __str__(self):
            return str(self.created_at)+"::"+self.name+"::"+self.email


class Executive(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=120)
    phone = models.CharField(max_length=12)
    role = models.CharField(max_length=120)
    country = models.ForeignKey('Countries',on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    zone = models.ForeignKey('Zones',on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
            return self.first_name+" "+self.last_name


class Otp(models.Model):
    otp  = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    business_id = models.CharField(max_length = 15)
    created_at = models.DateTimeField('date created', default=timezone.now)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
            return str(self.created_at)+"::"+self.otp+"::"+self.email


class Thumsup(models.Model):
    email = models.EmailField(max_length=100)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    business_id = models.CharField(max_length = 15)
    created_at = models.DateTimeField('date created', default=timezone.now)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
            return str(self.created_at)+"::"+self.email


class Referer(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    referer = models.CharField(max_length=80, blank=True, null=True)
    user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True,default=None)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" "+self.email


class IndexQueue(models.Model):
    business = models.ForeignKey('Business', on_delete=models.SET_NULL, null=True, default=None)
    processed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.business.name


class Location(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey('States',on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
