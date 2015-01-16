$(document).ready(function () { 
    $('#id_train_name').keyup(function (e) {
       //alert(String.fromCharCode(e.keyCode)); 
	   var query;
       query = $(this).val();
       $.get('/entry/suggest_trains/', {suggestion: query}, function(data){
       $('#cats').html(data);
       });
    });
	
	$('#id_train_name').focusout(function (e) {
       //alert($(this).val()); 
	   var query;
       query = $(this).val();
       $.get('/entry/populate_source_destinations/', {suggestion: query}, function(data){
		$('#source').html(data);
	    $('#destinations').html(data);
       });
    });
	
});