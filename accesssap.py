import autoit
import subprocess
import time
import pygetwindow as gw
import re
from findtext import find_text_position
from findtext import find_texts_on_screen
from findtext import find_window_title
from sendkey import sendkey
from datetime import datetime
from accessfile import delete_file
from accessfile import check_file_in_folder


def sap_login(username,password):
    try:
        # พาธไปยังไฟล์ saplogon.exe
        saplogon_path = r"C:\Program Files (x86)\SAP\FrontEnd\SapGui\saplogon.exe"

        # รัน saplogon.exe
        subprocess.Popen(saplogon_path)

        window_title = "SAP Logon 750"

        autoit.win_wait_active(window_title, timeout=10)

        autoit.control_click(window_title,"[CLASS:SysListView32; INSTANCE:1]",x=20, y=20,clicks=2)
        autoit.send(send_text="{ENTER}")
        time.sleep(3)
        autoit.win_close(window_title)
        time.sleep(3)

        #ใส่รหัสผ่าน
        autoit.send(send_text=username)
        autoit.send('{TAB}')
        autoit.send(send_text=password)
        autoit.send('{TAB}')
        autoit.send(send_text="en")
        autoit.send(send_text="{ENTER}")
        time.sleep(3)

        windows = gw.getAllTitles()
        for window in windows:
            if re.search(r'Multiple\s*Logons',window):
                autoit.win_activate(window)
                position = find_text_position(['with','this','logon'])
                autoit.mouse_click("left",x=position[0],y=position[1])
                autoit.send(send_text="{ENTER}")
                break

        autoit.send(send_text="{ENTER}")
        time.sleep(1)
        autoit.send(send_text="{F12}")
        time.sleep(1)
        autoit.send(send_text="{ENTER}")
        time.sleep(1)
        autoit.send(send_text="{F12}")
        time.sleep(1)

        windows = gw.getAllTitles()
        for window in windows:
            if re.match(r'SAP\s*Easy\s*Access\s*PEA',window):
                autoit.win_activate(window)
                autoit.win_wait_active(window,timeout=3)
                autoit.send('{ESC}')
                time.sleep(1)
                return "isLoggined"
        return None
    
    except Exception as e:
        print(e)
        return None
    

def close_sap():
    try:
        powershell_cmd = 'Get-Process -Name "sap*" | Stop-Process -Force'
        subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, text=True)
        return "sapIsClosed"
    
    except Exception as e:
        print(e)
        return None


def get_export_zcsr181(zcsr181Path,businessCode):
    endDate = f"31.12.{datetime.now().year}"
    startDate = f"01.01.{datetime.now().year - 1}"
    try: 
        if find_window_title(r'SAP\s*Easy\s*Access\s*PEA') == None:
            print("No title SAP Easy Access PEA")
            return None
        
        delete_file(zcsr181Path,businessCode)
        sendkey('{ESC}')
        sendkey('ZCSR181')
        sendkey('{ENTER}',stoke=1)
        sendkey(f"{businessCode}*")
        sendkey('{TAB}',times=6)
        sendkey("Y3")
        sendkey('{TAB}',times=6)
        sendkey(startDate)
        sendkey('{TAB}')
        sendkey(endDate)
        sendkey('{TAB}',times=5)
        sendkey('{DOWN}',times=2)
        sendkey('{F8}')

        if find_texts_on_screen(["ZCSR181","PED-400"],timeout=180) == None :
            return None

        sendkey('{CTRLDOWN}{SHIFTDOWN}{F7}{SHIFTUP}{CTRLUP}',stoke=2)
        sendkey('{ENTER}',stoke=2)

        if find_window_title("บันทึกเป็น",timeout=180) == None:
            return None

        sendkey('{TAB}')
        sendkey('^+{TAB}')
        path = f"{zcsr181Path}{businessCode}"
        sendkey('{CTRLDOWN}a{CTRLUP}')
        sendkey(path)
        sendkey('{ENTER}',stoke=2)

        sendkey('{ALTDOWN}A{ALTUP}',stoke=2)

        sendkey('{ALTDOWN}D{ALTUP}',stoke=2)

        if check_file_in_folder(zcsr181Path,businessCode) == None:
            return None
        
        sendkey('{ENTER}',stoke=1)
        sendkey('{F3}',times=2,stoke=1)

        return 'gotZCSR181Excel'
    
    except:
        return None