/*
 * This file contains film management code for stuff under the *
<slug>/films URL.
 */


function vivify_selectboxes() {
  // Make the select boxes' spans change when a different item is selected
  $("select").change(function(ev) {
		       var seltext = $(this).find(' :selected').text();
		       $(this).parents("div.filter_drops").children("span").text(seltext);
		     });
}

function vivify_filters() {
    var url = $("input.namesearch").parents("form").attr("action");    
    $("input.namesearch").keyup(function(ev) {
		if (K) {
	    K.abort();
		}
	
	K = $.ajax({
		     type:'GET',
		     success: function(data, text_data) {
		       $("#curationlist").html(data);
		       
		     },
		     error: function(XHR, text_status, error_thrown)   {
		       alert("Error in operation. Please try again.");
		     },
		     url : table_url,
		     data : $("input.namesearch").parents("form").serialize() + "&s=1"
		   });
    });
		
    $("div.filter_drops select").change(function(ev) {
    	if (K) {
    				K.abort();
				}
		var selected_var_url = $("input.namesearch").parents("form").serialize() + "&s=1";
		target_url = submit_url + selected_var_url;
		var form_url = $('#submmisions_form').attr('action');
		$('#submmisions_form').attr('action', target_url);
		var form_url_1 = $('#submmisions_form').attr('action');
		 $('#submmisions_form').submit();
	});
    
}

$(function() {
    // Display fancy loaders on Ajax activity
    $("#submission_loader").ajaxStart(function() {
					$(this).css("display","inline");
				      });
    $("#submission_loader").ajaxComplete(function() {
					   $(this).css("display","none");
					 });


    // Callbacks for flipping through pages
    $("a.submission_numbers").live("click",function(ev) {
				     var url = $(this).attr("href")+"&s=1";
				     // chnaged this for film list page for admin section
				      window.location = url;
				     // $("#curationlist").load(url);
    				     return false;
    });


    // Setup widgets
    vivify_selectboxes();
    vivify_filters();
    K = false; // K is a simple queueing system to prevent too many ajax requests from messing up the interface
  });
  
  
  
