var paymentbtn = document.getElementsByClassName('payment-done')
var orderComplete = '{{order.complete}}'

paymentbtn[0].addEventListener('click',function(){
        console.log('USER:', user)

        if (user == 'AnonymousUser') {
            paymentProcess()
        }
    })


function paymentProcess() {
    console.log('order:', orderComplete)
    if (orderComplete == 'True') {
        console.log('Delete cart')
        cart = {}
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

