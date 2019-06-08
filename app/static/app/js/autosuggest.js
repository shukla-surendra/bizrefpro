 $( "#searchQ" ).autocomplete({
      source: "/autocomplete",
      minLength: 2
    });

  $( "#locationQ" ).autocomplete({
      source: "/location_autocomplete",
      minLength: 2
    });