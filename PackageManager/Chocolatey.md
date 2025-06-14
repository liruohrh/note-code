# 安装
```ps1
#https://docs.chocolatey.org/en-us/choco/setup/#installing-to-a-different-location
$env:ChocolateyInstall = "D:\software\chocolatey"

#https://docs.chocolatey.org/en-us/choco/setup/#install-with-powershellexe
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```