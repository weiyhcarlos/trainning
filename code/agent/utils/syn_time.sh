#! /bin/bash
chmod +x ./utils/ntpdate_amd64.deb
chmod +x ./utils/ntpdate_i386.deb
inf=$(cat /etc/crontab | grep ntpdate |wc -l)
is_x64=$(uname --m| grep 64|wc -l)
if [ "$inf" -eq 0 ];then
	if [ `whoami` = "root" ];then
		if [ "$is_x64" -eq 1 ];then
			dpkg -i ./utils/ntpdate_amd64.deb
		else
			dpkg -i ./utils/ntpdate_i386.deb
		fi
   		echo "0 2 * * * root   ntpdate ntp.ubuntu.com" >> /etc/crontab
		ntpdate ntp.ubuntu.com
   	else
		if [ "$is_x64" -eq 1 ];then
                        sudo dpkg -i ./utils/ntpdate_amd64.deb
                else
                        sudo dpkg -i ./utils/ntpdate_i386.deb
		fi
    		sudo echo "0 2 * * * root   ntpdate ntp.ubuntu.com" >> /etc/crontab
		sudo ntpdate ntp.ubuntu.com
    fi
fi
#ntpdate ntp.ubuntu.com
