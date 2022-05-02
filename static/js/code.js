pred_btn = document.querySelector('#pred_btn')


model = document.getElementById('models') // current selected model

pred_txt = document.getElementById('pred_txt') // label that show the predicted count
pred_img = document.getElementById('pred_img') // predicted density map

slider = document.getElementById('slider') // slider component
slider_imgs = document.querySelectorAll('#slider img') // current selected dataset images


// ip address
url_address = ''

// dropdown initialization
model.selelectedIndex = 0

// slider initialization
default_img = [url_address, 'static/default.png'].join('/')
default_img_name = 'none'


const predict = () => {
    if (
         !model.value
    ) {
        console.log('Errori nella compilazione!')
        return
    }

    data = {
        model: model.value,
    }

    options = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'post',
        body: JSON.stringify(data)
    }

    url = [url_address, 'predict'].join('/')
    fetch(url, options)
        .then(res => res.json())
        .then(res => {
            let {pred_cnt, pred_time, device} = res
            pred_cnt = parseFloat(pred_cnt).toFixed(4)
            pred_time = parseFloat(pred_time).toFixed(4)

            pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
            pred_img.src = [url_address, 'static/map.jpg'].join('/')
            /*window.location.href = "http://localhost:5000/predict/" + res;*/
        })
        .catch(err => console.log(err))
}


// update images when the page is been loaded
window.addEventListener("load",  () => {
    console.log('loading...')
})


pred_btn.onclick = e => {
    predict()
}