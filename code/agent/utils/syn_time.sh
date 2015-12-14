#! /bin/bash
chmod +x ./utils/ntpdate_amd64.deb
inf=$(cat /etc/crontab | grep ntpdate |wc -l)
if [ "$inf" -eq 0 ];then
	if [ `whoami` = "root" ];then
		dpkg -i ./ntpdate_amd64.deb
   		echo "0 2 * * * root   ntpdate ntp.ubuntu.com" >> /etc/crontab
   	else
		sudo dpkg -i ./ntpdate_amd64.deb
    		sudo echo "0 2 * * * root   ntpdate ntp.ubuntu.com" >> /etc/crontab
    fi
fi
ntpdate ntp.ubuntu.com
