# Cookbook name :: network_change.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# Command to restart nsfd
execute "nsfd-restart" do
  command "/etc/init.d/nfs-kernel-server restart"
  action :run
end


# Check whether the the nic already exists in the main file. If found, comment it
updateNicInfo(node['thunder']["#{node['thunder']['network_type']}_nic"])

# file not contains the include option then include it
if File.readlines("/etc/network/interfaces").grep(/source \/etc\/network\/interfaces.d\//).size <= 0
  open('/etc/network/interfaces', 'a') { |f|
    f << 'source /etc/network/interfaces.d/*'
  }
end

# create directory
directory "/etc/network/interfaces.d/" do
  action :create
end

# Set the source file
source_file = "nic_conf.erb"

# Sets the nic info 
nic_info = {
  'nic_name' => node['thunder']["#{node['thunder']['network_type']}_nic"],
  'nic_ip' => node['thunder']["#{node['thunder']['network_type']}_ip"],
  'nic_subnet' => node['thunder']["#{node['thunder']['network_type']}_subnet_mask"],
  'nic_gateway' => node['thunder']["#{node['thunder']['network_type']}_gateway"],
  'nic_dns' => node['thunder']["#{node['thunder']['network_type']}_dns"],
}
           
# Calls the configuration function for network
configureNetworkCard(nic_info, source_file)