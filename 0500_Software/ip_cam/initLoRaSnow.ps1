# ---- ATTENTION ----#
#Run first the last commented line in command line area
#It modifies this script context execution policy to
#allow for installation of powershell modules
#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted

#You also must generate ssh key pairs and store the row
#in the public (id_ras.pub) key in the destination computer
#at the end of the file /home/lorasnow/.ssh/authorized_keys
#or send me the key so i can store it myself
#to generate you can simply use :
#ssh-keygen
#leave default location (C:\Users\username/.ssh/id_rsa)
#give passPhrase
#
#then run this on source computer :
#ssh-keygen -p -P "" -N "" -m pem -f C:\Users\username\.ssh\privateKeyFileName -P passPhrase
#to convert the key to correct format

# Creates credentials for raspi
$Credential = Get-Credential
$Credential.Password | ConvertFrom-SecureString | Out-File -Filepath .\credential.txt

# Installs posh-ssh if not installed
if($(get-installedModule).Name -like 'posh-ssh'){
 Write-Output "Module posh-ssh installed"
}
else{
 Write-Output posh-ssh module installation...
 install-module posh-ssh
}