#
# Cookbook Name:: thunder-install
# Recipe:: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# thunder network type
default['thunder']['network_type'] = "install"

# thunder installation values
default['thunder']['install_nic'] = "eth0"
default['thunder']['install_ip'] = "192.168.122.31"
default['thunder']['install_subnet_mask'] = "255.255.255.0"
default['thunder']['install_gateway'] = "192.168.122.1"
default['thunder']['install_dns'] = "8.8.8.8"
  
# thunder pxe network values
default['thunder']['pxe_nic'] = "eth1"
default['thunder']['pxe_pool_start'] = "192.168.122.1"
default['thunder']['pxe_pool_end'] = "192.168.122.100"
default['thunder']['pxe_subnet_mask'] = "255.255.255.0"
default['thunder']['pxe_gateway'] = "192.168.122.1"
default['thunder']['pxe_subnet'] = "192.168.122.0/24"
default['thunder']['pxe_ip'] = "192.168.122.31"

# thunder setup packages
default['thunder']['install_setup'] = {
  'cobbler_packages' => ['isc-dhcp-server', 'nfs-common', 'nfs-kernel-server'],
  'zabbix_packages' => ['zabbix-server-mysql'],
  'package_options' => "-o Dpkg::Options::='--force-confold' -o Dpkg::Options::='--force-confdef'"
}

# Set the chef server path
default['thunder']['chef_server_path'] = "/opt/thunder_web/chef-repo"

# Set the deb source folder
default['thunder']['deb_src_path'] = "/opt"