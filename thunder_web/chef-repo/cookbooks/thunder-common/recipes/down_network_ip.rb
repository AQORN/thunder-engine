# @author: Geo Varghese
# @create_date: 9-june-2015
# @modified by: Geo Varghese    
# @modified_date: 9-June-2015
# @linking to other page: 
# @description: The recipe to down ip temporarly in nic

nic_name = node['thunder']['attach_nic']

# if vlan enabled, install related packages
if !node['thunder']['vlan_tag'].to_s.empty?
  nic_name = nic_name + "." + node['thunder']['vlan_tag'].to_s
    
  # remove vlan device
  execute "remove vlan device" do
    command "vconfig rem #{nic_name}"
    only_if "cat /proc/net/vlan/config | grep #{nic_name}"
  end
   
else
  
  ip_address = if node['thunder']['from_node'] then node['thunder']['from_ip'] else node['thunder']['attach_ip'] end
  netmask = if node['thunder']['netmask'] then node['thunder']['netmask'] else "255.255.255.0" end 
  
  # down ip 
  execute "down ip #{ip_address} in #{nic_name}" do
    command "/etc/init.d/networking restart"
    action :run
  end
  
  # down ip 
  execute "down ip #{ip_address} in #{nic_name}" do
    command "ifconfig #{nic_name} #{ip_address} netmask #{netmask} down"
    action :run
  end
  
end

