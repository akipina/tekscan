# Flask-Based Sensor Recording Application with TekAPI .NET Integration

This project is a Flask web application that interacts with a sensor via the `TekAPIWrapper` class, which wraps around a .NET API (`TekAPI.dll`). The application allows users to start and stop recording sensor data in real-time and monitor the file size to ensure the recording stops when a specified limit is reached.

## Features

- **Check Sensor Connection:** The application checks whether the sensor is connected before allowing recordings to start.
- **Continuous Recording:** Record data continuously until either the user presses "Stop" or a maximum file size is reached.
- **Configurable Recording Parameters:** Users can set custom values for the recording segment size and maximum file size.
- **Real-time Monitoring:** The application monitors the recording file size and automatically stops when the limit is reached.
- **Threaded Execution:** Recording is handled in a separate thread to keep the web interface responsive.
- **TekAPIWrapper Integration:** The application uses a custom Python wrapper (`TekAPIWrapper`) around the TekAPI .NET assembly to communicate with the sensor.

## Requirements

To run this application, you need the following:

- **Python 3.x**
- **Flask** (`pip install flask`)
- **TekAPIWrapper** (Custom Python wrapper for TekAPI using `pythonnet` to interact with the .NET assembly)
- **pythonnet** (`pip install pythonnet`)

### Install Python Dependencies

You may want to create a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install flask pythonnet
