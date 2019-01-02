from django_cron import CronJobBase, Schedule
from app.models import IndexQueue, Business, User
import pysolr


class SearchSyncCronJob(CronJobBase):
    RUN_EVERY_MINS = 15
    # every 15 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.search_cron_job'

    def do(self):
        solr = pysolr.Solr('http://localhost:8983/solr/collection1/', timeout=10)
        index_data = []
        deindex_data = []
        indexes = IndexQueue.objects.filter(processed=False)
        for index in indexes:
            index.processed = True
            index.save()
            business = index.business
            keyword_list = []
            keywords = business.keywords.all()
            for keyword in keywords:
                keyword_list.append(keyword.name)
            website = ""
            try:
                web = business.objects.get(id=business.website)
                website = web.name
            except:
                pass
            location_list = []
            locations = business.locations.all()
            for location in locations:
                location_list.append(location.name)
            try:
                if business.active is True and business.deleted is False:
                    group_rating = self.calculate_group_rating(business)
                    business_points = business.rating + business.thumbs_up + group_rating
                    index_data.append(
                        {
                            "id": "doc_" + str(business.id),
                            "title": business.title,
                            "description": business.aboutus,
                            "keywords": keyword_list,
                            "address": business.address1,
                            "website": website,
                            "locations":location_list,
                            "business_id": business.id,
                            "thumbs_down": business.thumbs_down,
                            "contact": str(business.contact_number),
                            "rank": str(business_points)
                        })
                else:
                    deindex_data.append("doc_" + str(business.id))
            except:
                pass
        solr.add(index_data, commit=True)
        if len(deindex_data) > 0:
            solr.delete(id=deindex_data, commit=True)
        print("django cron run complete")

    def calculate_group_rating(self, business):
        points = 0
        if business is not None:
            total_thumbs_up =0
            user_id = business.user.id
            object_list = User.objects.filter(reference_id=user_id)
            for object in object_list:
                thumbs_up = 0
                businesses = Business.objects.filter(user=object)
                for business in businesses:
                    if business.active is True:
                        thumbs_up += business.thumbs_up
                        total_thumbs_up = thumbs_up
            points = total_thumbs_up
        return points

