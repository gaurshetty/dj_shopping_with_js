
var updateBtns = document.getElementsByClassName('update-wishlist')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if (user == 'AnonymousUser') {
            addCookieWishlist(productId, action)
        }else{
            updateUserWishlist(productId, action)
        }
    })
}


function addCookieWishlist(productId, action) {
    console.log('User is not authenticated..')
    if (action == 'add') {
        if(wishlist[productId]  == undefined){
            wishlist[productId] = {'quantity': 1}
        }
    }
    if (action == 'remove') {
        wishlist[productId]['quantity'] -= 1
        if(wishlist[productId]['quantity'] <= 0){
            console.log('Item got deleted')
            delete wishlist[productId];
        }
    }
    if (action == 'clear') {
        console.log('Delete wishlist')
        wishlist = {}
    }
    console.log('wishlist:', wishlist)
    document.cookie = 'wishlist=' + JSON.stringify(wishlist) + ";domain=;path=/"
    location.reload()
}


function updateUserWishlist(productId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_wishlist/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    });
}