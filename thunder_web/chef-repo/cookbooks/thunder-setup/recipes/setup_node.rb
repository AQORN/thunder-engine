# @author: Geo Varghese
# @create_date: 20-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 20-Mar-2015
# @linking to other page: 
# @description: The recipe to setup node

# set hostname
hostname = node['thunder']['node_hostname']
file '/etc/hostname' do
  content "#{hostname}\n"
  mode '0644'
end

# execute hostname
execute "hostname #{hostname}" do
  only_if { node['hostname'] != hostname }
end

# etc hosts entry
template '/etc/hosts' do
  source 'etc_hosts.erb'
  variables(
    thunder_ip: node['thunder']['ip'],
    chef_server_ip: node['thunder']['chef_server_ip'],
    controller_ip: node['thunder']['controller_ip'] 
  )  
end

# setup network configuration
include_recipe 'thunder-setup::setup_network_configuration'

# disk partition
include_recipe 'thunder-setup::disk_partition'
