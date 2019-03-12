$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    /*$(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    }); */

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});



/*============================================
                top menu toggle
==============================================*/

( function( $ ) {
$( document ).ready(function() {
//$('#panel-menu li.has-sub>a').on('click', function(){
//      $(this).removeAttr('href');
//      var element = $(this).parent('li');
//      if (element.hasClass('open')) {
//          element.removeClass('open');
//          element.find('li').removeClass('open');
//          element.find('ul').slideUp();
//      }
//      else {
//          element.addClass('open');
//          element.children('ul').slideDown();
//          element.siblings('li').children('ul').slideUp();
//          element.siblings('li').removeClass('open');
//          element.siblings('li').find('li').removeClass('open');
//          element.siblings('li').find('ul').slideUp();
//      }
//  });
//
//  $('#panel-menu>ul>li.has-sub>a').append('<span class="holder"></span>');
//
//  (function getColor() {
//      var r, g, b;
//      var textColor = $('#panel-menu').css('color');
//      textColor = textColor.slice(4);
//      r = textColor.slice(0, textColor.indexOf(','));
//      textColor = textColor.slice(textColor.indexOf(' ') + 1);
//      g = textColor.slice(0, textColor.indexOf(','));
//      textColor = textColor.slice(textColor.indexOf(' ') + 1);
//      b = textColor.slice(0, textColor.indexOf(')'));
//      var l = rgbToHsl(r, g, b);
//      if (l > 0.7) {
//          $('#panel-menu>ul>li>a').css('');
//          $('#panel-menu>ul>li>a>span').css('');
//      }
//      else
//      {
//          $('#panel-menu>ul>li>a').css('');
//          $('#panel-menu>ul>li>a>span').css('');
//      }
//  })();
//
//  function rgbToHsl(r, g, b) {
//      r /= 255, g /= 255, b /= 255;
//      var max = Math.max(r, g, b), min = Math.min(r, g, b);
//      var h, s, l = (max + min) / 2;
//
//      if(max == min){
//          h = s = 0;
//      }
//      else {
//          var d = max - min;
//          s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
//          switch(max){
//              case r: h = (g - b) / d + (g < b ? 6 : 0); break;
//              case g: h = (b - r) / d + 2; break;
//              case b: h = (r - g) / d + 4; break;
//          }
//          h /= 6;
//      }
//      return l;
//  }
});
} )( jQuery );


$(document).ready(function(){
	$('#mybtn').click(function(){
	$('.new-adds').show(500);
	});
});

$(document).ready(function(){
	$('#mybtn3').click(function(){
	$('.new-adds1').show(500);
	});
});


$(document).ready(function(){
	$('#mybtn4').click(function(){
	$('.new-adds4').show(500);
	$('.new-adds5').show(500);
	});

	$(document).on("click",".show_referer", function(e){
	e.preventDefault();
	e.preventDefault();
	user_id = $(this).data("id")
    $.ajax({
    url:'/executive/get_reference',
    data:'id='+user_id,
    success:function(res, status, xHr){
    if(res.length > 0){
    $("#refererList").html("")
    $.each(res, function(index, element){
    $("#refererList").append('<tr><td>'+element.name+'</td><td>'+element.email+'</td><td><a class="show_referer" data-id="'+element.id+'">'+element.reference+'</a></td></tr>');
    })

    $("#referarModal").modal("show");
    }
    }
    })


	})

});