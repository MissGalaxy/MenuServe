$(document).ready(function () {
    init();
});

function init() {
    init_menu();
    init_cart();
}

function init_menu(){
	$('.addtocart').click(function(){
		var menuid = $(this).attr('value');
		$.ajax({
			type: 'GET',
        	url: 'add_to_cart/',
        	dataType: 'json',
        	data: {"menu_id": menuid},
        	success: function(){
        		console.log("success");
        	},
        	error: function() {
        		console.log("error");
        	},
		});
	});
}

function init_cart(){
	$('.removeFromCart').click(function(){
		var itemid=$(this).attr('value');
		$.ajax({
			type: 'GET',
        	url: '/change_cart_item/',
        	dataType: 'json',
        	data: {"remove_item_id": itemid},
        	success: function(data){
        		console.log("success");
        		$('#'+data['item_id']).remove();
        		$('#subtotal').text(data['totalPrice'])
        		$('#totalPrice').text(data['totalPrice'])
        		$('#order-price').text(data['totalPrice'])
        	},
        	error: function() {
        		console.log("error");
        	},
		});
	});
	$('.itemPlus').click(function(){
		var itemid=$(this).attr('value');
		$.ajax({
			type: 'GET',
        	url: '/change_cart_item/',
        	dataType: 'json',
        	data: {"plus_item_id": itemid},
        	success: function(data){
        		console.log("success, num is %d",data['num']);
        		$('#'+data['item_id']+'show').attr('value',data['num']);
        		$('#subtotal').text(data['totalPrice'])
        		$('#totalPrice').text(data['totalPrice'])
        		$('#order-price').text(data['totalPrice'])
        	},
        	error: function() {
        		console.log("error");
        	},
		});
	});
	$('.itemMinus').click(function(){
		var itemid=$(this).attr('value');
		$.ajax({
			type: 'GET',
        	url: '/change_cart_item/',
        	dataType: 'json',
        	data: {"minus_item_id": itemid},
        	success: function(data){
        		console.log("success, num is %d",data['num']);
        		$('#'+data['item_id']+'show').attr("value",data['num']);
        		$('#subtotal').text(data['totalPrice'])
        		$('#totalPrice').text(data['totalPrice'])
        		$('#order-price').text(data['totalPrice'])
        	},
        	error: function() {
        		console.log("error");
        	},
		});
	});

}

