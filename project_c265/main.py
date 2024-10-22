import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('static/', filename))

    # OpenCV video capture initialization
    source = cv2.VideoCapture('static/' + filename)

    # Check if the video file opened successfully
    if not source.isOpened():
        return "Error: Could not open video file."

    # Define video frame width and height
    frame_width = int(source.get(3))  # width of video frame
    frame_height = int(source.get(4))  # height of video frame

    size = (frame_width, frame_height)

    # Create the output video file for grayscale video
    result = cv2.VideoWriter('static/blackandwhite.mp4',
                             cv2.VideoWriter_fourcc(*'mp4v'),
                             30, size, 0)  # 0 means grayscale

    # Read and process video frames
    while True:
        status, frame_image = source.read()
        if not status:  # If the frame is not read correctly, exit the loop
            break
        if frame_image is None:  # Handle cases where the frame is empty
            continue
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame_image, cv2.COLOR_RGB2GRAY)
        result.write(gray)

    # Release the video resources after processing
    source.release()
    result.release()

    # Return the upload form with the processed filename
    return render_template('upload.html', filename=filename)
@app.route('/download')
def download_file():
    converted_video_path = "static/blackandwhite.mp4"
    return send_file(converted_video_path, as_attachment=True)
@app.route('/display/<filename>')
def display_video(filename):
    return redirect(url_for('static', filename=filename))


if __name__ == "__main__":
    app.run(debug=True)
