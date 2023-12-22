$(document).ready(function() {

    // var price_id = 1;
    // // Loop through each checked checkbox
    // $('.price-input:checked').each(function() {
    //     price_id = $(this).val();
    // });
    // $('.price-input').on('change', function() {
    //     price_id = $(this).val();
    // });
    // console.log("Get Price selected", price_id)


    $(".cart-icon").on("click", function(e) {
        $(".cart-bar").toggleClass('active');
    });


    //add to cart
    $(".add-to-cart").on("click", function(e) {
        const room_id = $(this).attr('room_id');
        const token = $(this).attr('token');
        const food_id = $(this).attr('id');
        const qunatity = $("#quantity-" + food_id).val();
        // const price_id = $("#price-" + food_id).attr('id');
        var selectedData = [];

        // Loop through each checked checkbox input
        $(".price-input-" + food_id + ":checked").each(function() {
            var value = $(this).val();
            var price = $(this).attr('price');
            var sell_price = $(this).attr('sell_price');
            selectedData.push({ id: value, price: price, sell_price: sell_price });
        });
        // console.log("The prices", selectedData)
        $.ajax({
            headers: {
                "X-CSRFToken": token
            },
            url: '/cart/',
            type: 'POST',
            data: {
                room: room_id,
                item: food_id,
                price: selectedData[0].id,
                quantity: qunatity,
            },
            dataType: 'json',
            success: function(response) {
                $('#add-to-cart-' + food_id).modal('hide');
                const cart_id = response.id;
                const image = $(".item-" + food_id).find(".image img").attr("src");
                const name = $(".item-" + food_id).find(".product_name").text();
                // const price = $(".item-" + food_id).find(".product_price strong").text();
                $(".cart-bar .cart-list").append('<li id="cart-item-' + cart_id + '" cart_id="' + cart_id + '" class="cart">' +
                    '<div class="product-box">' +
                    '<img src="' + image + '"/>' +
                    '<div class="content">' +
                    '<p class="name">' + name + '</p>' +
                    '<strong class="price">Price: ₹ ' + (selectedData[0].sell_price != "None" ? selectedData[0].sell_price : selectedData[0].price) + '  </strong>' +
                    '<span class="quantity"> Qty: ' + qunatity + '</span>' +
                    '</div>' +
                    '</div>' +
                    '<span class="close delete-cart-item" id="' + cart_id + '" token="' + token + '"><i class="bi bi-x-lg"></i></span>' +
                    '</li>');
                $(".total_price").text("₹ " + response.total_price);
                $(".cart-icon span").text(response.total_items);
            },
            error: function(error) {
                console.log("The error", error.responseJSON)
                $('#add-to-cart-' + food_id).modal('hide');
                if (error.responseJSON.non_field_errors[0] == "The fields room, item must make a unique set.") {
                    $('.response').empty().show().html('<div class="alert alert-danger" role="alert">The item already added to your cart.</div>').delay(2000).fadeOut(500);
                } else {
                    alert('An error occurred while adding the product to cart');
                }
            }
        });
    });
    //delete item from to cart
    $(document).on("click", ".delete-cart-item", function(e) {
        const cartId = $(this).attr("id");
        const token = $(this).attr("token");
        $.ajax({
            headers: {
                "X-CSRFToken": token
            },
            url: "/cart/" + cartId + "/",
            type: "DELETE",
            data: {
                id: cartId
            },
            success: function(response) {
                $("#cart-item-" + cartId).remove();
                $(".total_price").text("₹ " + response.total_price);
                $(".cart-icon span").text(response.total_items);
            },
            error: function(xhr, status, error) {
                // Handle the error case
                console.log(error);
            }
        });
    });


    //place order
    $(document).on("click", ".place-order", function(e) {
        e.preventDefault();
        const roomId = $(this).attr("room_id");
        const token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            headers: {
                "X-CSRFToken": token
            },
            type: "POST",
            url: "/order/",
            contentType: 'application/json',
            data: JSON.stringify({
                room: roomId,
            }),
            success: function(response) {
                $('.response').empty().show().html('<div class="alert alert-success" role="alert">Your order has been placed.</div>').delay(2000).fadeOut(500);
                $(".cart-icon span").text("0");
                $(".cart").remove();
                $(".total_price").text("₹ 0");
                console.log("Get data", response)
                location.href = "/order_status/" + response.room_id + "/" + response.order_id + "/";
            },
            error: function(error) {
                $('.response').empty().show().html('<div class="alert alert-danger">' + error + '</div>').delay(1500).fadeOut(3000);
            }
        });
    });

});