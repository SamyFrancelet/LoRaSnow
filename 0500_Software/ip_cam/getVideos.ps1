#---- FYI ----#
#Example on how to get a file from remote host
#get-SFTPFile -SessionId $sessionID -RemoteFile $remoteFileFullPath -LocalPath $localPath

# ------------------------- inital jobs to be done ----------------------
# ---- ATTENTION ----#
#Run first the last commented line in command line area
#It modifies this script context execution policy to
#allow for installation of powershell modules
#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted



#---- ATTENTION ----#
#Then, if the module "posh-ssh" as not been installed,
#run this command to install the sftp capable module
#to be able to interact with the sftp server
#if($(get-installedModule).Name -like 'posh-ssh'){
# echo Module posh-ssh installed
#}
#else{
# echo posh-ssh module installation...
# install-module posh-ssh
#}



#---- ATTENTION ----#
#Generate usual ssh key pairs and store the row
#in the public key in the destination computer
#at the end of the file /home/user/.ssh/authorized_keys
#or in C:\Users\usrname\.ssh\authorized_keys for windows
#cmd and run in the source (!=destination) computer the following :
#ssh-keygen -p -P "" -N "" -m pem -f C:\Users\username\.ssh\privateKeyFileName -P passPhrase
#This converts the key's format from --OPENSSH to --RSA

# ------------------------- start of the script -------------------------

#uncomment following line if script running on NUC
#$videoFolderPath = "C:\Users\NUC3\Desktop\ip_cam\"
#use following line for test purpose
$videoFolderPath = "C:\work\ip_cam\test"
$HexPass = Get-Content "C:\work\LoRaSnow\0500_Software\ip_cam\creds.txt"
$creds = New-Object -TypeName PSCredential -ArgumentList "lorasnow", ($HexPass | ConvertTo-SecureString)

clear
$error.clear()
echo "Script to upload videos started"

#remote information
$pgaURL = "homedrive.crabdance.com"
$pgaPort = 10022
$serverVideosPath = "/media/homeDrive/ip_cam/"

#################################################################################################################################
#set the private key path for the ssh communication #############################################################################
$keyFullPath = "$($env:HOMEDRIVE)$env:HOMEPATH\.ssh\id_rsa"


#################################################################################################################################
#Create connection ##############################################################################################################
$sessionID = $(New-SFTPSession -computerName $pgaURL -Credential $creds -keyFile $keyFullPath -Port "$pgaPort").sessionId

#################################################################################################################################
#Search for the new created video folder ########################################################################################

#change the addDays parameter to -1 for transfer of last day records
$requiredFolderDate = $(get-date).AddDays(0).toString("dd-MM-yyyy")
echo "requiredFolderDate is $($requiredFolderDate)"
$folderToSend = Get-ChildItem -Path $videoFolderPath | where-object {$_.CreationTime.ToString("dd-MM-yyyy") -eq $requiredFolderDate}

#################################################################################################################################
#Upload the folder ##############################################################################################################
try{
    set-SFTPItem -SessionId $sessionID -Destination $serverVideosPath -Path "$videoFolderPath" -verbose -ErrorAction Stop
    #set-SFTPItem -SessionId $sessionID -Destination $serverVideosPath -Path "$rootVideosPath\$videoFolder" -verbose -ErrorAction Stop
#################################################################################################################################
#Delete the folder ##############################################################################################################
    #remove-item -Path $videoFolderPath\$folderToSend -Recurse
}catch{
    Write-Warning -Message "No folder send\nProbably due to the call to set-SFTPItem."
    Write-Error $Error[0]
}