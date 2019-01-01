$.ajax({
    type:'GET',
    url:'/search?q='+qpart1+'&location='+qpart2,
    success:function(result, status, xHr){
        result_counter = 0 ;
        result.response.docs.forEach(function(business, index){
            result_counter++;
            website="";
            if(typeof(business.website) != "undefined"){
                website = business.website[0]
            }


 myvar = '<div class="cl-add-item">'+
'                                        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 col-zero">'+
'                                            <div class="cl-add-item-detail">'+
'                                                <h4><a href="#">'+business.title[0]+'</a></h4>'+
'                                                <p>'+business.description[0]+'</p>'+
'                                                <h6><span><a href="#"><i class="fas fa-map-marker-alt"></i> &nbsp;&nbsp;'+business.address[0]+'</a></span></h6>'+
'                                            </div>'+
'                                            <div class="cl-add-item-icons">'+
'                                                <ul>'+
''+
'                                                   <!-- <li>'+
'                                                        <a href="#">'+
'                                                            business.rank[0]+'+
'                                                        </a>'+
'                                                    </li>-->'+
'                                                    <li class="cont_desktop">'+
'                                                        <a href="tel:'+business.contact[0]+'">'+
'                                                            Call Now : '+business.contact[0]+''+
'                                                        </a>'+
'                                                    </li>'+
'                                                    <li class="cont_mob">'+
'                                                        <a href="tel:'+business.contact[0]+'">'+
'                                                            Call'+
'                                                        </a>'+
'                                                    </li>';

            if(website != ""){
myvar += '                                                    <li>'+
'                                                        <a target= "_blank" href="'+website+'">'+
'                                                            Visit Website'+
'                                                        </a>'+
'                                                    </li>';
}
myvar += '											<li data-id="'+business.business_id[0]+'">'+
'														<a>'+
'															<i class="fas fa-thumbs-up" data-id="'+business.business_id[0]+'"></i> '+
'															<span>'+business.rank[0]+'</span>'+
'														</a>'+					
'                                                    </li>'+
'													<li data-id="'+business.business_id[0]+'">'+
'														<a>'+
'															<i class="fas fa-thumbs-down" data-id="'+business.business_id[0]+'"></i> '+
'															<span>'+business.thumbs_down[0]+'</span>'+
'														</a>'+	
'                                                </ul>'+
'                                            </div>'+
'                                        </div>'+
'                                    </div>';


            $("#searchResult").append(myvar)
        })
        if(result_counter == 0){
        $("#searchResult").append("<p>Your search did not match any Listing. We are building genuine database. Please check back soon.</p>")
        }
    }
})