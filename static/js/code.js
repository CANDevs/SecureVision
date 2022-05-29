pred_btn = document.querySelector('#pred_btn')
pred_video_btn = document.querySelector('#pred_video_btn')
stop_btn = document.querySelector('#stop_btn')
var stop = 0


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

function get_response(url,options,data){


    var xhr = new XMLHttpRequest();
    xhr.open("POST",url,false);
    xhr.setRequestHeader("Accept","application/json");
    xhr.setRequestHeader("Content-type","application/json");
    xhr.send(JSON.stringify(data))
    if(xhr.status === 200){
    let result = JSON.parse(xhr.responseText)
            let { pred_cnt, pred_time, device ,next_frame} = result
            pred_cnt = parseFloat(pred_cnt).toFixed(4)
            pred_time = parseFloat(pred_time).toFixed(4)
            console.log(next_frame)
         console.log(result)

            pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
            // pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
            /*window.location.href = "http://localhost:5000/predict/" + res;*/
            // console.log(nextFrame)
    // result.new_request = false;
    return result

}}

const predict_video = async () => {
    if (
        !model.value
    ) {
        console.log('error!')
        return
    }


    url = [url_address, 'predict_video'].join('/')
    let result = {next_frame: true, new_request: true}
    let data;
    let options;
    while (result.next_frame && stop===0) {
        data = {
            model: model.value,
            video: true,
            video_url: './static/datasets/video.mp4',
            new_request: result.new_request,
            secs: 1,
        }
        console.log(data)
        options = {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'post',
            body: JSON.stringify(data)
        }
        console.log(options)
        result = await get_response(url, options, data)
        pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
        console.log(result)

        // fetch(url, options)
        //     .then(res => res.json())
        //     .then(res => {
        //         console.log(res)
        //         let { pred_cnt, pred_time, device ,next_frame} = res
        //         pred_cnt = parseFloat(pred_cnt).toFixed(4)
        //         pred_time = parseFloat(pred_time).toFixed(4)
        //         nextFrame = next_frame
        //
        //         pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
        //         pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
        //         /*window.location.href = "http://localhost:5000/predict/" + res;*/
        //         console.log(nextFrame)
        //         data.new_request = false
        //
        //     })
        //     .catch(err => console.log(err))
        //     .finally(console.log(options.body))


    }
}

// update images when the page is been loaded
window.addEventListener("load", () => {
    console.log('loading...')
})

pred_video_btn.onclick = e => {
    stop = 0
    predict_video()
}
pred_btn.onclick = e => {
    predict()
}
stop_btn.onclick = e => {
    stop = 1;
}