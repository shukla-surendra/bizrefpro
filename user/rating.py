from app.models import Business, Media
def calculate_rating(business_id=0):
    rating = 0
    if business_id == 0:
        return
    business = Business.objects.get(id=business_id)
    try:
        medias = Media.objects.filter(user=business.user, ref_type="user")
        for media in medias:
            if media.title == "pancard":
                rating+=5
            if media.title == "dl":
                rating+=2
            if media.title == "aadhar":
                rating+=2
            if media.title == "voterid":
                rating+=2
            if media.title == "electricity":
                rating+=2
            if media.title == "passport":
                rating+=10
    except:
        None

    if business.gst_no not in ["", None]:
       rating += 20
    medias = Media.objects.filter(business=business, ref_type="business")
    for media in medias:
        if media.title == "pancard":
            rating+=5
        if media.title == "registration_certificate":
            rating+=10
        if media.title == "bankstatement":
            rating+=3
        if media.title == "utilitybill":
            rating+=3
        if media.title == "rentagreement":
            rating+=3
    business.rating = rating
    business.save()

def get_calculate_rating(business_id=0):
    rating = 0
    if business_id == 0:
        return
    business = Business.objects.get(id=business_id)
    try:
        medias = Media.objects.filter(user=business.user, ref_type="user")
        for media in medias:
            if media.title == "pancard":
                rating+=5
            if media.title == "dl":
                rating+=2
            if media.title == "aadhar":
                rating+=2
            if media.title == "voterid":
                rating+=2
            if media.title == "electricity":
                rating+=2
            if media.title == "passport":
                rating+=10
    except:
        None
    if business.gst_no not in ["", None]:
       rating += 20
    medias = Media.objects.filter(business=business, ref_type="business")
    for media in medias:
        if media.title == "pancard":
            rating+=5
        if media.title == "registration_certificate":
            rating+=10
        if media.title == "bankstatement":
            rating+=3
        if media.title == "utilitybill":
            rating+=3
        if media.title == "rentagreement":
            rating+=3
    return rating