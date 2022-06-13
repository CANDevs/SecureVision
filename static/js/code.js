pred_video_btn = document.querySelector('#pred_video_btn')
alert_label = document.getElementById("alert_msg")
stop_btn = document.querySelector('#stop_btn')
var stop_exe = 0


model = document.getElementById('models') // current selected model

pred_txt = document.getElementById('pred_txt') // label that show the predicted count
pred_label = document.getElementById('pred_label') // label that show the predicted count
pred_img = document.getElementById('pred_img') // predicted density map

// ip address
url_address = ''

// dropdown initialization
model.selelectedIndex = 0

// slider initialization
default_img = [url_address, 'static/default.png'].join('/')
default_img_name = 'none'
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");

function get_response(url, options, data) {


    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JSON.stringify(data))
    if (xhr.status === 200) {
        let result = JSON.parse(xhr.responseText)
        let { pred_cnt, pred_time, device, next_frame } = result
        pred_cnt = Math.ceil(parseFloat(pred_cnt).toFixed(4))
        pred_time = parseFloat(pred_time).toFixed(4)
        pred_txt.innerHTML = `${pred_cnt}, took ${pred_time} seconds on ${device}`
        
        if(parseInt(pred_cnt) > parseInt(output.innerHTML)) {pred_txt.style.color = "red"; pred_label.style.color = "red"; alert_label.style.display = "block"}
        else {pred_txt.style.color = "green"; pred_label.style.color = "green"; alert_label.style.display = "none"}
        return result

    }
}

const predict_video = async () => {
    if (
        !model.value
    ) {
        console.log('error!')
        return
    }


    url = [url_address, 'predict_video'].join('/')
    let result = { next_frame: true, new_request: true }
    let data;
    let options;
    while (result.next_frame && stop_exe === 0) {
        data = {
            model: model.value,
            video: true,
            video_url: './static/datasets/video.mp4',
            new_request: result.new_request,
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
        result = await get_response(url, options, data)
        pred_img.src = [url_address, 'static/map.jpg?'].join('/') + new Date().getTime()
    }
}

// update images when the page is been loaded
window.addEventListener("load", () => {
    console.log('loading...')
})

pred_video_btn.onclick = e => {
    e.preventDefault()
    stop_exe = 0
    predict_video()
}
stop_btn.onclick = e => {
    stop_exe = 1;
}

output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
} 