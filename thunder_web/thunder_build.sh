#!/bin/bash
# Initial env build script for Thunder v1.0.0
# 

THUNDER_REPO=http://svn.inhouse.net/usvn/svn/Leon/branches/thunderv1 
#svn --username varghese export $THUNDER_REPO
# Download ubuntu-12.04.2-server-amd64.iso  to  $THUNDER_TMP/thunder/system/
#################

# Begin setup 
HOSTNAME=thunder
THUNDER_BASE=$(dirname $(dirname  $0))

echo "127.0.0.1       $HOSTNAME" >> /etc/hosts
echo $HOSTNAME > /etc/hostname
hostname $HOSTNAME

rm -f /var/crash/*
perl -pi -e 's/enabled=1/enabled=0/' /etc/default/apport 

cat << 'EOF' > /etc/apt/apt.conf.d/90forceyes
APT::Get::force-yes "true";
APT::Get::Assume-Yes "true";
APT::Get::AllowUnauthenticated "true";
EOF

echo 'deb file:/usr/local/mydebs ./' > /etc/apt/sources.list

# dpkg -i $THUNDER_TMP/thunder/system/mydebs/dpkg-dev_1.17.5ubuntu5.4_all.deb
cat << 'EOF' > /usr/local/bin/update-mydebs
#! /bin/bash
cd /usr/local/mydebs
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
apt-get update
EOF
chmod u+x /usr/local/bin/update-mydebs

# update-mydebs 

cp -r $THUNDER_BASE/system/mydebs /usr/local/
cp -r $THUNDER_BASE/system/mydebs_ubuntu12 /usr/local/

apt-get update

cp -r $THUNDER_BASE/system/pylibs /usr/local/
mkdir -p /usr/local/src/isoimages/
cp $THUNDER_BASE/system/bootstrap.iso /usr/local/src/isoimages/
cp $THUNDER_BASE/system/ubuntu-12.04.2-server-amd64.iso /usr/local/src/isoimages/

apt-get install python-pip
apt-get install python-mysqldb
apt-get install python-pycurl
apt-get install python-lxml
apt-get install python-apt

pip install --no-index --find-links=file:///usr/local/pylibs  -r  $THUNDER_BASE/thunder_web/requirements.txt

apt-get install zabbix-release
perl -pi -e 's/^/#/g' /etc/apt/sources.list.d/zabbix.list 
# update-mydebs 
zabbix_pass=$(date | md5sum | head -c 16)

export DEBIAN_FRONTEND=noninteractive
echo 'mysql-server-5.5 mysql-server/root_passwd password ' | debconf-set-selections
echo 'mysql-server-5.5 mysql-server/root_passwd_again password ' | debconf-set-selections
echo 'mysql-server-5.5 mysql-server/root_passwd seen true ' | debconf-set-selections
echo 'mysql-server-5.5 mysql-server/root_passwd_again seen true ' | debconf-set-selections
echo "zabbix-server-mysql zabbix-server-mysql/mysql/app-pass password $zabbix_pass" | debconf-set-selections
echo 'zabbix-server-mysql zabbix-server-mysql/app-password-confirm password $zabbix_pass' | debconf-set-selections
echo 'zabbix-server-mysql zabbix-server-mysql/password-confirm password ' | debconf-set-selections
echo 'zabbix-server-mysql zabbix-server-mysql/mysql/admin-pass password ' | debconf-set-selections

apt-get install zabbix-server-mysql  zabbix-frontend-php

cp /etc/zabbix/apache.conf /etc/apache2/sites-enabled/zabbix.conf
a2enconf zabbix.conf
a2enmod alias

cp $THUNDER_BASE/system/zabbix.conf.php /etc/zabbix/web/

/etc/init.d/zabbix-server stop
mysql zabbix < $THUNDER_BASE/thunder_web/db/zabbix.sql
/etc/init.d/zabbix-server start

timezone=$(cat /etc/timezone)
perl -pi -e "\$str=q{date.timezone = \"$timezone\"}; s/;date.timezone =/\$str/" /etc/php5/apache2/php.ini
perl -pi -e "\$str=q{php_value date.timezone $timezone}; s/# php_value date.timezone .*/\$str/" /etc/apache2/sites-enabled/zabbix.conf
perl -pi -e 's/Listen 80/Listen 8080/'  /etc/apache2/ports.conf
perl -pi -e 's/Listen 443/Listen 8443/' /etc/apache2/ports.conf
sed -i "57i ServerName thunder" /etc/apache2/apache2.conf
ln -s /usr/local/mydebs_ubuntu12 /var/www/
service apache2 restart


thunder_pass=$(date | md5sum | head -c 16)
mysql -e 'create database thunder'
mysql -e "grant all privileges on thunder.* to thunder@localhost identified by '$thunder_pass'"
mysql -e 'flush privileges'
mysql thunder < $THUNDER_BASE/thunder_web/db/thunder_v.1.0.sql 

cp -r $THUNDER_BASE/thunder_web /opt/thunder_web

perl -pi -e 's/THUNDER_DB_NAME = ".*"/THUNDER_DB_NAME = "thunder"/' /opt/thunder_web/thunder/settings.py
perl -pi -e 's/THUNDER_DB_USER = ".*"/THUNDER_DB_USER = "thunder"/' /opt/thunder_web/thunder/settings.py
perl -pi -e "\$str=q{THUNDER_DB_PASS = \"$thunder_pass\"}; s/THUNDER_DB_PASS = \".*\"/\$str/"   /opt/thunder_web/thunder/settings.py

perl -pi -e 's/THUNDER_DB_NAME = ".*"/THUNDER_DB_NAME = "thunder"/' /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src
perl -pi -e 's/THUNDER_DB_USER = ".*"/THUNDER_DB_USER = "thunder"/' /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src
perl -pi -e "\$str=q{THUNDER_DB_PASS = \"$thunder_pass\"}; s/THUNDER_DB_PASS = \".*\"/\$str/"  /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src

perl -pi -e 's/ZABBIX_DB_NAME = ".*"/ZABBIX_DB_NAME = "zabbix"/' /opt/thunder_web/thunder/settings.py
perl -pi -e 's/ZABBIX_DB_USER = ".*"/ZABBIX_DB_USER = "zabbix"/' /opt/thunder_web/thunder/settings.py
perl -pi -e "\$str=q{ZABBIX_DB_PASS = \"$zabbix_pass\"}; s/ZABBIX_DB_PASS = \".*\"/\$str/"   /opt/thunder_web/thunder/settings.py

perl -pi -e 's/ZABBIX_DB_NAME = ".*"/ZABBIX_DB_NAME = "thunder"/' /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src
perl -pi -e 's/ZABBIX_DB_USER = ".*"/ZABBIX_DB_USER = "thunder"/' /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src
perl -pi -e "\$str=q{ZABBIX_DB_PASS = \"$zabbix_pass\"}; s/ZABBIX_DB_PASS = \".*\"/\$str/"  /opt/thunder_web/cloud/templates/thunderadmin/sources/thunder_settings.src

export DEBIAN_FRONTEND=noninteractive
apt-get install openssh-server
apt-get install chef
apt-get install debmirror
apt-get install bind9

apt-get install cobbler

cp $THUNDER_BASE/system/cobbler_loaders/* /var/lib/cobbler/loaders/

perl -pi -e 's/http_port: 80/http_port: 8080/' /etc/cobbler/settings

cp $THUNDER_BASE/system/ubuntu1204-custom.preseed /var/lib/cobbler/kickstarts/

ln -s /var/www/cobbler /var/www/cblr
perl -pi -e 's/^server: .*/server: localhost/' /etc/cobbler/settings
perl -pi -e 's/^next_server: .*/next_server: localhost/' /etc/cobbler/settings 

service cobbler restart
cobbler check

# apt-get install isc-dhcp-server
# apt-get install nfs-common
# apt-get install nfs-kernel-server
apt-get install chef-server-core 


mkdir /var/log/thunder

sed -i '/exit 0/i  \
python /opt/thunder_web/manage.py runserver 0.0.0.0:9000  >> /var/log/thunder/engine.log  & \
/opt/thunder_web/thunder_detect_node    >> /var/log/thunder/detect.log  & \
/opt/thunder_web/thunder_monitor_node >> /var/log/thunder/monitor.log   & \
/opt/thunder_web/thunder_process_job    >> /var/log/thunder/job.log    &'   /etc/rc.local
 

python /opt/thunder_web/manage.py runserver 0.0.0.0:9000  >> /var/log/thunder/engine.log  & 
/opt/thunder_web/thunder_detect_node    >> /var/log/thunder/detect.log  & 
/opt/thunder_web/thunder_monitor_node >> /var/log/thunder/monitor.log   & 
/opt/thunder_web/thunder_process_job    >> /var/log/thunder/job.log    &


