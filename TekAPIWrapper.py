import clr
import System
from System import Array

class TekAPIWrapper:
    def __init__(self):
        # Hardcoded .NET DLL path
        dll_path = r"C:\Tekscan\TekAPI\TekAPI.dll"
        
        # Load the TekAPI .NET assembly
        clr.AddReference(dll_path)

        # Import TekAPI classes from the .NET assembly
        from TekAPI import CTekAPI, CTekCalibration, CTekEquilibration, CTekFile

        # Initialize CTekAPI class for future method calls
        self.tekapi = CTekAPI()

    def initialize_hardware(self):
        # Call TekInitializeHardware
        result = self.tekapi.InitializeHardware()
        if result != 0:
            raise Exception(f"Failed to initialize hardware. Error code: {result}")
        return result

    def enumerate_handles(self):
        # Call TekEnumerateHandles to get sensor serial numbers
        serial_numbers = self.tekapi.EnumerateHandles()
        if serial_numbers is None or len(serial_numbers) == 0:
            raise Exception("No available handles found.")
        
        # Convert the serial numbers from .NET array to Python list
        sensor_list = [str(sn) for sn in serial_numbers]
        return sensor_list

    def claim_sensor(self, serial_number, map_file_path):
        # Call TekClaimSensor to claim the sensor
        result = self.tekapi.ClaimSensor(serial_number, map_file_path)
        if result != 0:
            raise Exception(f"Error claiming sensor. Error code: {result}")
        return result

    def initialize_sensor(self, serial_number, frame_period):
        # Call TekInitializeSensor to initialize the sensor
        result = self.tekapi.InitializeSensor(serial_number, frame_period)
        if result != 0:
            raise Exception(f"Error initializing sensor. Error code: {result}")
        return result

    def set_sensitivity(self, serial_number, level):
        # Call TekSetSensitivityLevel to set the sensitivity level
        result = self.tekapi.SetSensitivityLevel(serial_number, level)
        if result != 0:
            raise Exception(f"Error setting sensitivity. Error code: {result}")
        return result

    def capture_frame(self, serial_number, timeout_ms):
        # Prepare a buffer for the frame data
        frame_data = Array[System.Byte]([0] * 1024)  # Adjust size as needed
        result = self.tekapi.CaptureDataFrame(serial_number, timeout_ms, frame_data)
        if result != 0:
            raise Exception(f"Error capturing frame data. Error code: {result}")
        return list(frame_data)

    def start_recording(self, duration):
        # Call TekStartRecording to start the recording
        result = self.tekapi.StartRecording(duration)
        if result != 0:
            raise Exception(f"Error starting recording. Error code: {result}")
        return result

    def stop_recording(self):
        # Call TekStopRecording to stop the recording
        result = self.tekapi.StopRecording()
        if result != 0:
            raise Exception(f"Error stopping recording. Error code: {result}")
        return result

    def save_recording(self, serial_number, recording_path):
        # Call TekSaveRecording to save the recording
        result = self.tekapi.SaveRecording(serial_number, recording_path)
        if result != 0:
            raise Exception(f"Error saving recording. Error code: {result}")
        return result

    def release_sensor(self, serial_number):
        # Call TekReleaseSensor to release the sensor
        result = self.tekapi.ReleaseSensor(serial_number)
        if result != 0:
            raise Exception(f"Error releasing sensor. Error code: {result}")
        return result

    def deinitialize_hardware(self):
        # Call TekDeinitializeHardware to deinitialize hardware
        result = self.tekapi.DeinitializeHardware()
        if result != 0:
            raise Exception(f"Error deinitializing hardware. Error code: {result}")
        return result
