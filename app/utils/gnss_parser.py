import serial
import pynmea2
import config

def get_location():
    # Mock for testing without hardware
    return 25.7617, -80.1918  # Miami Beach coordinates
    
    # Uncomment for real hardware:
    # ser = serial.Serial(config.GNSS_PORT, config.GNSS_BAUD, timeout=1)
    # for _ in range(20):
    #     line = ser.readline().decode('ascii', errors='replace').strip()
    #     if line.startswith('$GPGGA'):
    #         try:
    #             msg = pynmea2.parse(line)
    #             if msg.latitude and msg.longitude:
    #                 return float(msg.latitude), float(msg.longitude)
    #         except Exception:
    #             continue
    #     time.sleep(0.1)
    # return None, None