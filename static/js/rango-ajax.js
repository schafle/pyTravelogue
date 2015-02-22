$(document).ready(function () { 
	var id1 = 0;
	var id2 = 0; 
    $('#id_train_name').keyup(function (e) {
       //alert(String.fromCharCode(e.keyCode)); 
	   var query;
       query = $(this).val();
       $.get('/entry/suggest_trains/', {suggestion: query}, function(data){
       $('#cats').html(data);
       });
    });
	
	$('#id_train_name').focusout(function (e) {
       //alert($('#id_train_name').val()); 
	   var query;
       query = $(this).val();
       $.get('/entry/populate_source_destinations/', {suggestion: query}, function(data){
		$('#source').html(data);
	    $('#destinations').html(data);
		});
    });
	
	$('#id_to_station').focusout(function (e) {
	    var g=$(this).val();  
		//alert(g);
		id1 = $('#destinations').find('option').filter(function() { return $.trim( $(this).val() ) === g; }).attr('id');
		//alert(id1);
	});
	
	$('#id_from_station').focusout(function (e) {
	    var g=$(this).val();  
		//alert(g);
		id2 = $('#source').find('option').filter(function() { return $.trim( $(this).val() ) === g; }).attr('id');
		//alert(id2);
	});
	
	$('#entry_form').submit(function() {
		//alert(id1-id2);
		var s = document.getElementById("id_distance_covered");
        s.value = id1-id2;
		return true
	});
	
});