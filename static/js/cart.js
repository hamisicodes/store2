var updateBtns = document.getElementsByClassName('update-cart');

for(i = 0 ; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log('ProductId: ',productId , 'Action: ',action)

        console.log('USER:',user)
        if(user == 'AnonymousUser'){
            console.log('User is not auntheticated')
        }else{
            updateUserOrder(productId,action)
        }

    })
}

const updateUserOrder = (productId,action) => {
    console.log('User is authenticated,sending data...')

    let url = '/update_item/'

    fetch(url , {
        method: 'POST',
        headers:{
            'Content-Type': 'application/Json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId':productId ,'action':action})
    })
    .then(response => response.json())
    .then(data => location.reload())
}