import smbus2
import time

TOF_ADDR = 0x29
REG_RESULT_RANGE_STATUS = 0x04
REG_RESULT_FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 = 0x14

bus = smbus2.SMBus(1)

def get_distance():
    try:
        # Mock for testing without hardware
        return 0.15  # 15cm fixed distance for simulation
        
        # Uncomment for real hardware:
        # bus.write_byte_data(TOF_ADDR, 0x00, 0x00)
        # time.sleep(0.1)
        # bus.write_byte_data(TOF_ADDR, 0x00, 0x01)
        # time.sleep(0.05)
        
        # while True:
        #     status = bus.read_byte_data(TOF_ADDR, REG_RESULT_RANGE_STATUS)
        #     if status & 0x01:
        #         break
        #     time.sleep(0.01)
        
        # low = bus.read_byte_data(TOF_ADDR, REG_RESULT_FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0)
        # high = bus.read_byte_data(TOF_ADDR, REG_RESULT_FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 + 1)
        # distance_mm = (high << 8) | low
        # return distance_mm / 1000.0
    except Exception as e:
        print(f"ToF Error: {e}")
        return None