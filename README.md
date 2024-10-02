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

- **Python 3.x** (32 bit python, specifically)
- **Flask** (`pip install flask`)
- **TekAPIWrapper** (Custom Python wrapper for TekAPI using `pythonnet` to interact with the .NET assembly)
- **pythonnet** (`pip install pythonnet`)
- Tekscan SDK is installed at C:\Tekscan\TekAPI\TekAPI.dll or modify script.

## Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/akipina/tekscan.git
   ```
2. **Set Up a Python Virtual Environment**
```bash
cd tekscan
python -m venv tekscan_venv
```
3. **Activate the virtual environment and install**
```bash
venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
```
4. **Install python32**

This program requires a 32 bit version of python to run it. In your virtual environment, run:
```bash
curl -o python-32bit.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5.exe
```
This will download python32. Download it and run it. The actual executable will likely be installed in C:\Users\<user>\AppData\Local\Programs\Python\Python311-32. You wll need to call python from this path. Replace user with your username.
## Usage
Once installation is complete, the application can be started by simply running
```bash
C:\Users\<user>\AppData\Local\Programs\Python\Python311-32\python.exe tekscan.py

Then going to http://localhost:5000




   

