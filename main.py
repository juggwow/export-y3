from accesssap import close_sap
from accesssap import sap_login
from accesssap import get_export_zcsr181

businessCodes = ['L00','L01','L02','L03','L04','L13','L05','L06','L07','L08','L09','L10','L11','L12']
zcsr181Path = "C:\\Users\\patna\\Y3data\\ZCSR181\\"

close_sap()
sap_login('S3GMDXX01','pea1111')

retries = 1

for businessCode in businessCodes:
    attemp = 0
    while attemp < retries:
        if get_export_zcsr181(zcsr181Path,businessCode) == None:
            close_sap()
            sap_login('S3GMDXX01','pea1111')
            attemp +=1
        else:
            break

print("suceess")









