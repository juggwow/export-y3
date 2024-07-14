import pytesseract
from PIL import Image
import mss
import mss.tools
import time
import sys
import autoit
import re
import pygetwindow as gw


sys.stdout.reconfigure(encoding='utf-8')

# กำหนดเส้นทางไปยัง tesseract executable หากไม่ได้ตั้งค่าใน PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_position(text_list,retries=6):
    try:
        attempt = 0
        while attempt < retries:
        # จับภาพหน้าจอ
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # เลือกจอมอนิเตอร์หลัก
                screenshot = sct.grab(monitor)
                
                # บันทึกภาพหน้าจอชั่วคราว
                mss.tools.to_png(screenshot.rgb, screenshot.size, output='screenshot.png')

            # เปิดภาพหน้าจอด้วย Pillow
            image = Image.open('screenshot.png')

            # ใช้ pytesseract เพื่อดึงข้อมูลข้อความและตำแหน่ง
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            # สร้างข้อความที่ต่อเนื่องกันจาก text_list
            concatenated_text = ' '.join(text_list)

            # ค้นหาข้อความที่ต่อเนื่องกันในข้อมูลที่ดึงมา
            for i in range(len(data['text'])):
                current_text = ' '.join(data['text'][i:i+len(text_list)])
                if current_text == concatenated_text:
                    x = min(data['left'][i:i+len(text_list)])
                    y = min(data['top'][i:i+len(text_list)])
                    w = sum(data['width'][i:i+len(text_list)])
                    h = max(data['height'][i:i+len(text_list)])
                    return (x, y, w, h)
                
            attempt += 1

        # ถ้าไม่พบข้อความที่ต่อเนื่องกันตามที่ต้องการ
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def find_texts_on_screen(texts, timeout=30):
    """
    รอข้อความที่ระบุปรากฏบนหน้าจอแล้วค่อยดำเนินการต่อ
    :param texts: รายการข้อความที่ต้องการหา
    :param timeout: เวลาที่จะรอก่อน timeout (วินาที)
    :return: ตำแหน่งของข้อความที่พบ {ข้อความ: (x, y, w, h)} หรือ None ถ้าไม่พบหรือเกิดข้อผิดพลาด
    """
    start_time = time.time()
    while True:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # เลือกจอมอนิเตอร์หลัก
                screenshot = sct.grab(monitor)
                
                # บันทึกภาพหน้าจอชั่วคราว
                mss.tools.to_png(screenshot.rgb, screenshot.size, output='screenshot.png')

            # เปิดภาพหน้าจอด้วย Pillow
            image = Image.open('screenshot.png')

            # ใช้ pytesseract เพื่อดึงข้อมูลข้อความและตำแหน่ง
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            found_texts = {}
            # ค้นหาข้อความที่ต้องการในข้อมูลที่ดึงมา
            for i in range(len(data['text'])):
                for text in texts:
                    if text in data['text'][i]:
                        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        found_texts[text] = (x, y, w, h)
                        if len(found_texts) == len(texts):
                            return found_texts

        except Exception as e:
            print(f"An error occurred: {str(e).encode('utf-8', errors='replace').decode('utf-8')}")
            return None
        # ตรวจสอบว่าเวลาที่รอเกิน timeout หรือยัง
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            break

        # รอ 1 วินาทีก่อนตรวจสอบอีกครั้ง
        time.sleep(1)

    # ถ้าไม่พบข้อความที่ต้องการภายในเวลา timeout
    return None

def find_window_title(pattern,timeout=30):
    try:
        start_time = time.time()
        while True :
            windows = gw.getAllTitles()
            for window in windows:
                if re.match(pattern,window):
                    autoit.win_activate(window)
                    autoit.win_wait_active(window,timeout=3)
                    print(window)
                    return window
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                break

            time.sleep(0.2)
            
        return None
    
    except: 
        return None