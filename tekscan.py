from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
import threading
import time
from TekAPIWrapper import TekAPIWrapper  # Import the TekAPIWrapper class

app = Flask(__name__)

# Global variables to manage recording status
is_recording = False
sensor_connected = False
recording_thread = None
tekapi = TekAPIWrapper()  # Initialize the TekAPIWrapper class

DEFAULT_RECORDING_SEGMENT = 60  # Default recording segment size in seconds
MAX_FILE_SIZE = 1000 * 1024 * 1024  # Default maximum file size (1GB)
RECORDING_PATH = os.getcwd()

# Check if the sensor is connected
def check_sensor_status():
    global sensor_connected
    try:
        # Use TekAPIWrapper to check for sensor availability
        available_serial_numbers = tekapi.enumerate_handles()
        if available_serial_numbers:
            sensor_connected = True
        else:
            sensor_connected = False
    except Exception as e:
        print(f"Error checking sensor status: {e}")
        sensor_connected = False
    return sensor_connected

# Start the recording, continuously until stopped or max file size reached
def start_recording(segment_size, max_file_size):
    global is_recording
    is_recording = True
    try:
        # Get the first available sensor's serial number
        serial_number = tekapi.enumerate_handles()[0]
        tekapi.initialize_sensor(serial_number, 10000)  # Example frame period

        # Start recording segments continuously until stopped or max file size is reached
        while is_recording:
            tekapi.start_recording(segment_size)  # Record for the specified segment size
            monitor_recording_size(serial_number, max_file_size)

    except Exception as e:
        print(f"Error starting recording: {e}")
        is_recording = False

# Stop the recording
def stop_recording():
    global is_recording
    try:
        tekapi.stop_recording()
        is_recording = False
    except Exception as e:
        print(f"Error stopping recording: {e}")

# Monitor file size and stop recording when limit is reached
def monitor_recording_size(serial_number, max_file_size):
    recording_path = os.path.join(RECORDING_PATH,"recordings","recording.fsx")
    while is_recording:
        try:
            if os.path.exists(recording_path):
                file_size = os.path.getsize(recording_path)
                if file_size >= max_file_size:
                    stop_recording()
            time.sleep(1)
        except Exception as e:
            print(f"Error monitoring recording size: {e}")
            stop_recording()

@app.route('/')
def index():
    sensor_connected = check_sensor_status()
    return render_template('index.html', sensor_connected=sensor_connected)

@app.route('/start_recording', methods=['POST'])
def start():
    if not sensor_connected:
        return jsonify({"status": "Sensor not connected"})

    if sensor_connected and not is_recording:
        global recording_thread

        # Get user-specified max file size and segment size from the form data
        max_file_size = int(request.form.get('max_file_size', MAX_FILE_SIZE)) * 1024 * 1024  # Convert MB to bytes
        segment_size = int(request.form.get('segment_size', DEFAULT_RECORDING_SEGMENT))

        # Start the recording in a separate thread
        recording_thread = threading.Thread(target=start_recording, args=(segment_size, max_file_size))
        recording_thread.start()
        return redirect(url_for('index', status="Recording started"))

    return jsonify({"status": "Sensor not connected or already recording"})

@app.route('/stop_recording', methods=['POST'])
def stop():
    if is_recording:
        stop_recording()
        return redirect(url_for('index', status="Recording stopped"))

    return jsonify({"status": "No recording in progress"})

if __name__ == '__main__':
    app.run(debug=True)
