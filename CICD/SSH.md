# OpenSSH Server
- [windows安装](https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell&pivots=windows-10)
	- 不要手动创建C:\ProgramData\ssh，或者`ssh-keygen -A`
	- 如果有sshd运行不了，将client和server都卸载再重装，先装server