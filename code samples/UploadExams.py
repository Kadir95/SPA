from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#Login to Google Drive and create drive object
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
# Importing os and glob to find all PDFs inside subfolder
import glob, os, cv2

os.chdir("C:\Python27\GDrive\Exams")
for file in glob.glob("*.pdf"):
    print file
    print os.path.splitext(file)[0]
    
    with open(file,"r") as f:
        fn = os.path.basename(f.name)
        file_drive = drive.CreateFile()  
        file_drive.SetContentFile(fn) 
        file_drive.Upload()

        emailaddres=os.path.splitext(file)[0]

        permission = file_drive.InsertPermission({
                        'type': 'user',
                        'value': emailaddres,
                        'role': 'reader'})
   
        print "The file: " + fn + " has been uploaded"

print "All files have been uploaded"
