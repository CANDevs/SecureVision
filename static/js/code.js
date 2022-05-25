pred_btn = document.querySelector('#pred_btn')
pred_video_btn = document.querySelector('#pred_video_btn')


model = document.getElementById('models') // current selected model

pred_txt = document.getElementById('pred_txt') // label that show the predicted count
pred_img = document.getElementById('pred_img') // predicted density map

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
        console.log('error!')
        return
    }

    data = {
        model: model.value,
        image: './static/datasets/SHHB/2.jpg',
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
            console.log(res)
            let { pred_cnt, pred_time, device } = res
            pred_cnt = parseFloat(pred_cnt).toFixed(4)
            pred_time = parseFloat(pred_time).toFixed(4)

            pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
            pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
            /*window.location.href = "http://localhost:5000/predict/" + res;*/
        })
        .catch(err => console.log(err))
}
const predict_video = () => {
    if (
        !model.value
    ) {
        console.log('error!')
        return
    }

    data = {
        model: model.value,
        video: true,
        video_url: './static/datasets/video.mp4',
        new_request: true,
        secs: 1,
    }

    options = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'post',
        body: JSON.stringify(data)
    }

    url = [url_address, 'predict_video'].join('/')
    let nextFrame = true
    // while(nextFrame){
    fetch(url, options)
        .then(res => res.json())
        .then(res => {
            console.log(res)
            let { pred_cnt, pred_time, device ,next_frame} = res
            pred_cnt = parseFloat(pred_cnt).toFixed(4)
            pred_time = parseFloat(pred_time).toFixed(4)
            nextFrame = next_frame

            pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
            pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
            /*window.location.href = "http://localhost:5000/predict/" + res;*/
            console.log(nextFrame)
            options.data.new_request = false

        })
        .catch(err => console.log(err))

// }
}

// update images when the page is been loaded
window.addEventListener("load", () => {
    console.log('loading...')
})

pred_video_btn.onclick = e => {
    predict_video()
}
pred_btn.onclick = e => {
    predict()
}
