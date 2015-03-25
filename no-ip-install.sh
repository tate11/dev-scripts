#!/bin/sh
# scripto to install no-ip
###################################
sudo apt-get install make
sudo apt-get -y install gcc
cd /usr/local/src/
sudo wget http://www.noip.com/client/linux/noip-duc-linux.tar.gz
sudo tar xf noip-duc-linux.tar.gz
cd noip-2.1.9-1/
sudo make install
#Please enter login/email: jobiols
#Please enter password: veconceR
#contestar preguntas sobre defaults y grupos.
sudo rm /usr/local/src/noip-duc-linux.tar.gz
#Poner el script en init.d
sudo cp /usr/local/src/noip-2.1.9-1/debian.noip2.sh  /etc/init.d/
#Make script executable
sudo chmod +x /etc/init.d/debian.noip2.sh
#hacer que se ejecute al booteo
sudo update-rc.d debian.noip2.sh defaults
#arrancar y parar el demonio
sudo /etc/init.d/debian.noip2.sh restart
