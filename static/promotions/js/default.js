  /*====================================================================
	               topbar-scroll
====================================================================*/
 
        $(window).scroll(function() {
            //After scrolling 100px from the top...
            if ( $(window).scrollTop() >= 100 )
            {
                $('.neo-head-topbar').css('display', 'none');
                $('.neo-head-navbar').css('background-color', '#000;');
              
            }
            else
            {
                $('.neo-head-topbar').css('display', 'block');
                $('.neo-head-navbar').css('background-color', 'rgba(255, 255, 255, 0.20);');
               
            }
        });
        
         /*====================================================================
	             nav-menu
====================================================================*/
  $(document).ready(function(e) {
    $(".hamburger").click(function(){
		
		$(".menu").toggle(1000);
		});
});
  
  
  /*============================================
                back to top
==============================================*/

if ($('#back-to-top').length) {
    var scrollTrigger = 100, // px
        backToTop = function () {
            var scrollTop = $(window).scrollTop();
            if (scrollTop > scrollTrigger) {
                $('#back-to-top').addClass('show');
            } else {
                $('#back-to-top').removeClass('show');
            }
        };
    backToTop();
    $(window).on('scroll', function () {
        backToTop();
    });
    $('#back-to-top').on('click', function (e) {
        e.preventDefault();
        $('html,body').animate({
            scrollTop: 0
        }, 700);
    });
}
