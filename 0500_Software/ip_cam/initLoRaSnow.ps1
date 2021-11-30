# Creates credentials for raspi
$Credential = Get-Credential
$Credential.Password | ConvertFrom-SecureString | Out-File -Filepath .\credential.txt

# Installs posh-ssh if not installed
if($(get-installedModule).Name -like 'posh-ssh'){
 echo "Module posh-ssh installed"
}
else{
 echo posh-ssh module installation...
 install-module posh-ssh
}