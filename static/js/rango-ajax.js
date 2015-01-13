$(document).ready(function () { 
    $('#id_train_name').keyup(function (e) {
       //alert(String.fromCharCode(e.keyCode)); 
	   var query;
       query = $(this).val();
       $.get('/entry/suggest_trains/', {suggestion: query}, function(data){
       $('#cats').html(data);
       });
    });
});