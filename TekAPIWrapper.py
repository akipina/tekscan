import clr
from System import Array, String, Int32, Int64, Byte
from ctypes import c_char_p
import os, time

CALIBRATION_FILE = String(r"C:\Users\alex.kipina\Desktop\python\tekscan\calibration\SampleCal.cal")
EQ_FILE = String(r"C:\Users\alex.kipina\Desktop\python\tekscan\equilibriation\sampleEQ.equ")
MAP_FILE = String(r"C:\Users\alex.kipina\Desktop\python\tekscan\map\5512HT.mp")
MAP_FILE_DIRECTORY = String(r"C:\Users\alex.kipina\Desktop\python\tekscan\map")
RECORDING_DIRECTORY = String(r"C:\Users\alex.kipina\Desktop\python\tekscan\recordings")
DLL_PATH = r"C:\Tekscan\TekAPI\TekAPI.dll"


def n2p(netstring):
    return [str(item) for item in netstring]

class TekAPIWrapper:
    def __init__(self):
        dll_path = DLL_PATH
        clr.AddReference(dll_path)

        from System import Array, Byte
        from TekAPI import CTekAPI, CTekCalibration, CTekEquilibration, CTekFile

        self.tekapi = CTekAPI()

    def initialize_hardware(self):
        self.tekapi.TekInitializeHardware()

    def enumerate_handles(self):
        #serial_numbers = Array[str]([""])
        serial_numbers = [""]
        errorcode, serial_numbers = self.tekapi.TekEnumerateHandles(serial_numbers)
        
        pyserials = n2p(serial_numbers)
        
        if errorcode != self.tekapi.TEK_OK:
            raise Exception(f"Error enumerating handles: {self.get_last_error()}")
        print(f"[INFO] Found serial numbers: {pyserials}")
        return pyserials

    def claim_sensor(self, available_serials, map_file=MAP_FILE):
        if not os.path.exists(map_file):
            raise FileNotFoundError(f"Map file not found {map_file}")
        else:
            print(f"[INFO] Found map file {map_file}")
            if isinstance(map_file, str):
                print("[INFO] Converting map file input to System.String")
                map_file = String(map_file)

        # Convert available_serials to System.String[] if it's a single string
        if isinstance(available_serials, str):
            available_serials = [available_serials]
        available_serials_array = Array[String](available_serials)

        errorcode, other_output = self.tekapi.TekClaimSensor(available_serials_array, map_file)
        if errorcode != self.tekapi.TEK_OK:
            error = self.get_last_error()
            raise Exception(f"Error claiming sensor: {error}")
  
    def set_map_file_directory(self,mapfilepath=MAP_FILE_DIRECTORY):
        self.tekapi.TekSetMapFileDirectory(mapfilepath)
    
    def load_equilibration(self, eq=EQ_FILE):
        result = self.tekapi.TekLoadEquilibration(eq)
        if result:
            print(f"[INFO] Successfully loaded equilibriation file {eq}")
        else:
            raise Exception(f"Error loading equilibriation: {self.get_last_error()}")
    
    def load_calibration(self, cal=CALIBRATION_FILE):
        result = self.tekapi.TekLoadCalibration(cal)
        if result:
            print(f"[INFO] Successfully loaded calibration file {cal}")
        else:
            raise Exception(f"Error loading calibration: {self.get_last_error()}")
        
    def set_sensitivity_level(self,serial,lvl):
        error = self.tekapi.TekSetSensitivityLevel(serial,lvl)
        if error != self.tekapi.TEK_OK:
            raise Exception(f"Error setting sensitivity level!")
        
    def get_sensor_rows(self,serial):
        error, rows = self.tekapi.TekGetSensorRows(serial)
        if error !=0:
            raise Exception(f"Error: could not get sensor rows!")
        else:
            print(f"[INFO] Founds {rows} rows!")
            return rows
        
    def get_sensor_columns(self,serial):
        error, columns = self.tekapi.TekGetSensorColumns(serial)
        if error !=0:
            raise Exception(f"Error: could not get sensor rows!")
        else:
            print(f"[INFO] Founds {columns} columns!")
            return columns
    def get_sensor_row_spacing(self,serial):
        error, row_spacing = self.tekapi.TekGetSensorRowSpacing(serial)
        if error !=0:
            raise Exception(f"Error: could not get sensor rows!")
        else:
            print(f"[INFO] Found row spacing: {row_spacing}")
            return row_spacing
    def get_sensor_column_spacing(self,serial):
        error, column_spacing = self.tekapi.TekGetSensorColumnSpacing(serial)
        if error !=0:
            raise Exception(f"Error: could not get sensor rows!")
        else:
            print(f"[INFO] Found column spacing: {column_spacing}")
            return column_spacing
    
    
    #errorCode = CTekAPI.TekGetSensorRows(serialNumber, out rows);
    #errorCode = CTekAPI.TekGetSensorColumns(serialNumber, out columns);
    #rowSpacing = CTekAPI.TekGetSensorRowSpacing(serialNumber, out rowSpacing);
    #columnSpacing = CTekAPI.TekGetSensorColumnSpacing(serialNumber, out columnSpacing);

    def initialize_sensor(self, serial_number, frame_period_us):
        result = self.tekapi.TekInitializeSensor(serial_number, frame_period_us)
        if result != self.tekapi.TEK_OK:
            raise Exception(f"Error initializing sensor: {self.get_last_error()}")
        else:
            print(f"[INFO] Sensor {serial_number} initialized")

    def set_sensitivity_level(self, serial_number, level):
        result = self.tekapi.TekSetSensitivityLevel(serial_number, level)
        if result != self.tekapi.TEK_OK:
            raise Exception(f"Error setting sensitivity level: {self.get_last_error()}")
        else:
            print(f"[INFO] Successfully set sensitivity level {level}")

    def capture_data_frame(self, serial_number, timeout_ms=100):
        timeout_ms = Int32(timeout_ms)
        data_frame = Array[Byte]([0] * 1024)
        error, data_frame = self.tekapi.TekCaptureDataFrame(serial_number, timeout_ms, data_frame)
        if error != self.tekapi.TEK_OK:
            raise Exception(f"Error capturing frame data: {self.get_last_error()}")
        else:
            print(f"[INFO] Found data frame: {len(data_frame)}")
            return data_frame
    
    #test me
    def start_recording(self, serial_number, duration_seconds):
        duration_seconds = Int32(duration_seconds)
        error = self.tekapi.TekStartRecording(serial_number, duration_seconds)
        if error != self.tekapi.TEK_OK:
            raise Exception(f"Error starting recording: {self.get_last_error()}")
        else:
            print(f"[INFO] Recording successfully started for {duration_seconds} seconds!")
    
    #test me
    def stop_recording(self):
        error = self.tekapi.TekStopRecording()
        if error != self.tekapi.TEK_OK:
            raise Exception(f"Error stopping recording: {self.get_last_error()}")
        else:
            print("[INFO] Recording successfully stopped!")
    
    #test me
    def save_recording(self, serial_number, filename=None, calibration=CALIBRATION_FILE, equilibration=EQ_FILE):
        if not filename:
            filename = String("recording" + time.strftime("%Y%m%d-%H%M%S") + ".fsx")
        file_path = RECORDING_DIRECTORY + filename
        
        if calibration and equilibration:
            result = self.tekapi.TekSaveRecording(serial_number, file_path, equilibration, calibration)
        elif calibration:
            result = self.tekapi.TekSaveRecording(serial_number, file_path, calibration)
        elif equilibration:
            result = self.tekapi.TekSaveRecording(serial_number, file_path, equilibration)
        else:
            result = self.tekapi.TekSaveRecording(serial_number, file_path)
        
        
        if result != self.tekapi.TEK_OK:
            raise Exception(f"Error saving recording: {self.get_last_error()}")
        else:
            print("[INFO] Recording saved.")
        
   #test me
    def getFramesToRecord(self, serial):
        frames = Int32(0)
        
        error, frames = self.tekapi.TekGetFramesToRecord(serial,frames)
        if error!= 0:
            raise Exception(f"Error getting frames! {self.get_last_error()}")
        else:
            print(f"[INFO] {frames} frames receieved!")
            return frames
    
    #test me
    def isRecording(self):
        return self.tekapi.TekIsRecording()
    
    #test me
    def waitUntilRecordingComplete(self, time=.5):
        while self.isRecording(self):
            time.sleep(.5)
        return True

    def release_sensor(self, serial_number):
        result = self.tekapi.TekReleaseSensor(serial_number)
        if result != self.tekapi.TEK_OK:
            raise Exception(f"Error releasing sensor: {self.get_last_error()}")

    def deinitialize_hardware(self):
        self.tekapi.TekDeinitializeHardware()

    def get_last_error(self):
        return self.tekapi.TekGetLastError()
    
    
def main():
    tekapi = TekAPIWrapper()  # Initialize the TekAPIWrapper class
    
    
    tekapi.set_map_file_directory()
    tekapi.load_calibration()
    tekapi.load_equilibration()
    
    tekapi.initialize_hardware()
    available_serials = tekapi.enumerate_handles()
    serial = available_serials[0]
    
    tekapi.claim_sensor(available_serials)
    
    tekapi.initialize_sensor(serial,Int64(10000))
    tekapi.set_sensitivity_level(serial,Int32(20))
    
    tekapi.get_sensor_rows(serial)
    tekapi.get_sensor_columns(serial)
    tekapi.get_sensor_row_spacing(serial)
    tekapi.get_sensor_column_spacing(serial)
    
    data = tekapi.capture_data_frame(serial)
    
    
    """
    Things left to do to complete the TekAPIWrapper class
    
    Test and fix the recording methods.
    StartRecording()
    isRecording()
    getFramesToRecord()
    waitUntilRecordingComplete()
    StopRecording()
    save_recording()
    
    
    When these work, we have all the logic to save data to a file.
    
    Our next steps would be to get together and decide what we want the front end logic to look like
    --IE: what acceptance criteria for our program
    -- At a minimum, it needs to be able to read out maximum, average pressures, show center of force at rest, and be able to identify if machine is coming down weird.
    
    """
    
    
    
    tekapi.deinitialize_hardware()

if __name__ == '__main__':
    main()