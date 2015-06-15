# Cookbook name :: install_zabbix.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# Installs the zabbix module in the node
dpkg_package 'zabbix' do
    source "#{node['thunder']['deb_src_path']}/zabbix-release_2.2-1+trusty_all.deb"
    action :install
end

# Installs the zabbix mysqldb in the node
platform_options = node['thunder']['install_setup']
node['thunder']['install_setup']['zabbix_packages'].each do |pkg|
  package pkg do
    options platform_options['package_options']
    action :install
  end
end