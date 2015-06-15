#
# Cookbook Name:: thunder-setup
# Recipe:: default
#
# Copyright 2015, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

# setup node for installation
include_recipe 'thunder-setup::setup_node'

# install dependent modules
platform_options = node['thunder']['setup']
node['thunder']['setup']['controller_packages'].each do |pkg|
  package pkg do
    options platform_options['package_options']
    action :upgrade
  end
end

# install oslo middleware
installSourcePythonPackage('pbr-0.10.8.tar.gz')
installSourcePythonPackage('pytz-2015.2.tar.gz')
installSourcePythonPackage('Babel-1.3.tar.gz')
installSourcePythonPackage('six-1.9.0.tar.gz')
installSourcePythonPackage('stevedore-1.3.0.tar.gz')
installSourcePythonPackage('netaddr-0.7.14.tar.gz')
installSourcePythonPackage('oslo.config-1.9.3.tar.gz')
installSourcePythonPackage('oslo.i18n-1.5.0.tar.gz')
installSourcePythonPackage('WebOb-1.4.tar.gz')
installSourcePythonPackage('oslo.context-0.2.0.tar.gz')
installSourcePythonPackage('oslo.middleware-1.0.0.tar.gz')

# commented to replace with above code
#execute 'fix python packages dependency' do
#  command "pip install oslo.middleware"
#  action :run
#end

# download required gem packages
downloadFileInPackageDir("mysql-2.9.1.gem")

# setup mysql server server and create databases
include_recipe 'thunder-setup::create_database'

# setup messaging server
include_recipe 'thunder-setup::setup_messaging_server'