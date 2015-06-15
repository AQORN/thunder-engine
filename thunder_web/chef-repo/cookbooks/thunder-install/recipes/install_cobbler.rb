# Cookbook name :: install_cobbler.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# Installs the cobbler in the node
platform_options = node['thunder']['install_setup']
node['thunder']['install_setup']['cobbler_packages'].each do |pkg|
  package pkg do
    options platform_options['package_options']
    action :install
  end
end

# Execute cobbler sync
#execute "cobbler-sync" do
#  command "cobbler sync"
#  action :run
#end