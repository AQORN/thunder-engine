# @author: Geo Varghese
# @create_date: 21-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 21-Apr-2015
# @linking to other page: 
# @description: The recipe to check ping

# up network ip temporarly
include_recipe 'thunder-common::setup_network_ip_temp'

ip_address = node['thunder']['attach_ip']
  
# check ping
execute "check ping to ip #{ip_address}" do
  command "ping -c 1 #{ip_address}"
  action :run
end

# down network ip
include_recipe 'thunder-common::down_network_ip'
