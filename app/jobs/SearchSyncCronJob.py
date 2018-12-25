from django_cron import CronJobBase, Schedule
from app.models import Business, BizRefProSearch, Website
import pysolr
class SearchSyncCronJob(CronJobBase):
    RUN_EVERY_MINS = 15
    # every 15 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.search_cron_job'
    # a unique code
    def do(self):
        solr = pysolr.Solr('http://localhost:8983/solr/collection1/', timeout=10)
        indexData = []
        businesses = Business.objects.all()
        for business in businesses:
            keywordList = []
            keywords = business.keywords.all()
            for keyword in keywords:
                keywordList.append(keyword.name)
            website = ""
            try:
                web = business.objects.get(id=business.website)
                website = web.name
            except:
                pass
            locationList = []
            locations = business.locations.all()
            for location in locations:
                locationList.append(location.name)
            try:
                # How you'd index data.
                indexData.append(
                    {
                        "id": "doc_" + str(business.id),
                        "title": business.title,
                        "description": business.aboutus,
                        "keywords": keywordList,
                        "address": business.address1,
                        "website": website,
                        "locations":locationList,
                        "business_id": business.id,
                        "thumbs_down" : business.thumbs_down,
                        "contact": str(business.contact_number),
                        "rank": str(business.rating + business.thumbs_up)
                    }
                )
            except:
                pass
                #search = BizRefProSearch(title=business.title,description=business.aboutus,keywords=business.keyword, address=business.city ,website=website, contact=business.contact_number, rank=business.rating+business.thumbs_up,business_id=business.id)
                #search.save();
        solr.add(indexData, commit=True)
        print("django cron run complete")