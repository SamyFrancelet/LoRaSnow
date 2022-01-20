# LoRaSnow - Video getter
Those scripts are made to be run on a Windows source machine.
To use, first **run powershell as administrator**.

First you need to generate RSA keys, to do this simply run :
```powershell
ssh-keygen
```
Press enter to leave default name and location (C:/Users/username/.ssh/id_rsa)
and enter a passPhrase.
When the key is generated, you can add the public key
(located at : C:/Users/username/.ssh/id_rsa.pub) to the 
/home/user/.ssh/authorized_keys file,
or asks destination admin to do it for you (samy.francelet@ik.me).
When done, you must convert you private key to correct format by using :
```powershell
ssh-keygen -p -P "" -N "" -m pem -f C:\Users\username\.ssh\id_rsa -P passPhrase
```

If everything went alright, we can start using the scripts

To allow custom script usage you first must run :
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted
```

Then, we can run the initLoRaSnow.ps1 script :
```powershell
cd \directory\where\the\folder\is\ip_cam
.\initLoRaSnow
```
You will probably get a log prompt, or being asked credentials in the terminal,
enter destination credentials (asks admin for it (samy.francelet@ik.me)).
This script will generate credentials, so you won't need to type them everytime.
It will also install possh if you don't already have it : simply say Yes to All.

Then you are ready to use the main script :
```powershell
.\getVideos.ps1
```
This script transfers video files from source computer to destination,
then deletes them.
Usage can be customized :

This part defines where the videos are :
```powershell
#uncomment following line if script running on NUC
#$videoFolderPath = "C:\Users\NUC3\Desktop\ip_cam\"
#use following line for test purpose
$videoFolderPath = "D:\work\LoRaSnow\0500_Software\ip_cam\test"
```
This part sends either the whole folder and deletes it, or sends each file with
correct date :
```powershell
#uploads and delete file
try{
    #uncomment accordingly to your usage

    # transmits and deletes files
    foreach ($fileToSend in $validFiles) {
        #sends file
        set-SFTPItem -SessionId $sessionID -Destination $serverVideosPath -Path $videoFolderPath\$fileToSend -verbose -ErrorAction Stop
        #deletes file
        remove-item -Path $videoFolderPath\$fileToSend -Recurse
    }
    # transmits and deletes folder
    #set-SFTPItem -SessionId $sessionID -Destination $serverVideosPath -Path $videoFolderPath -verbose -ErrorAction Stop
    #remove-item -Path $videoFolderPath -Recurse

}catch{
    Write-Warning -Message "No folder send\nProbably due to the call to set-SFTPItem."
    Write-Error $Error[0]
}
```
If the configuration has been done correctly, it will work flawlessly.