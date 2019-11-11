$(document).ready(function () {
    manageOrder();
});

function manageOrder() {
    setInterval(function(){
    	refreshOnTime()
    }, 5000);
    // init_order();
}

function refreshOnTime(){
	$.ajax({
		type: 'GET',
        url: '/refresh_order/',
        dataType: 'json',
        data: {},
        success: function(data){
        	console.log("refresh success");
        	var table=$(".mytbody");
        	table.empty();
        	if(data){
        		$.each(data,function(index,obj){
        			// console.log(obj.address);
        			var test="<tr>" +
        			"<td>" + obj.id+ "</td>" +
        			"<td>" + obj.address+ "</td>" +
        			"<td>" + obj.store+ "</td>" +
        			"<td>" + obj.price+ "</td>" +
        			"<td>" + obj.description+ "</td>" +
        			"<td>" + obj.status+ "</td>" +
        			"<td>"+"<button class=\"btn btn-primary\" type=\"submit\" name=\"fulfill\" value="+obj.id+">Fulfill</button>"+"</td>"
        			+"</tr>";
        			table.append(test);
        		});
        	}
        },
        error: function() {
        	console.log("error");
        },
	});
}