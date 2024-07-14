import subprocess
import os
import re

def delete_file(folderPath,filePrefix):
   # สร้างคำสั่ง PowerShell สำหรับลบไฟล์ที่ตรงกับเงื่อนไข
    powershell_cmd = fr'''
        $folderPath = "{folderPath}"
        $filePrefix = "{filePrefix}"
        Get-ChildItem -Path $folderPath -Filter "$filePrefix*" | Remove-Item -Force -ErrorAction SilentlyContinue
    '''
    
    # เรียกใช้ PowerShell ด้วย subprocess
    try:
        subprocess.run(["powershell", "-Command", powershell_cmd], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell command: {e}")

def check_file_in_folder(folderPath,fileName):
    """
    ตรวจสอบไฟล์ในโฟลเดอร์ที่กำหนด
    :param folderPath: เส้นทางไปยังโฟลเดอร์ที่ต้องการตรวจสอบ
    :return: รายการชื่อไฟล์ทั้งหมดในโฟลเดอร์หากมี หรือ None ถ้าไม่พบไฟล์
    """
    # ตรวจสอบว่าโฟลเดอร์ที่กำหนดมีอยู่จริงหรือไม่
    try: 
        if not os.path.exists(folderPath):
            return None
    
        # หาไฟล์ทั้งหมดในโฟลเดอร์
        files = os.listdir(folderPath)
        
        # ตรวจสอบว่ามีไฟล์ในโฟลเดอร์หรือไม่
        if not files:
            return None
        
        # คืนค่ารายการชื่อไฟล์ทั้งหมด
        for file in files:
            print(file)
            if re.search(fileName,file):
                return file
            
        return None
    
    except:
        return None