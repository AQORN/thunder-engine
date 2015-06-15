# @author: Geo Varghese
# @create_date: 9-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 9-Mar-2015
# @linking to other page: 
# @description: The recipe to setup network

# if valn enabled, install related packages
if node['thunder']['vlan_enabled']
  
  # install valn package
  platform_options = node['thunder']['setup']
  package "vlan" do
    options platform_options['package_options']
    action :upgrade
  end
  
  # add kernal module temporary
  executeCmd("modprobe 8021q")
  
  # add permanently
  template "/etc/modules" do
    source 'etc_modules.erb'
  end
  
end

# file not contains the include option then include it
if File.readlines("/etc/network/interfaces").grep(/source \/etc\/network\/interfaces.d\//).size <= 0
  executeCmd("echo 'source /etc/network/interfaces.d/*' >> /etc/network/interfaces")
end

# create directory
directory "/etc/network/interfaces.d/" do
  action :create
end

# loop through the node nic config and setup it
node['thunder']['node_network'].each do |net_type, nic_info|
  
  # not change admin network configurations
  if net_type != "A"
  
    nic_device = nic_info['nic_name']
    
    # if vlan tag is enabled
    if nic_info['vlan_tag'].to_s.empty? or nic_info['vlan_tag'].to_s.length == 0
      nic_name = nic_info['nic_name'] 
    else
      nic_name = nic_info['nic_name'] + "." + nic_info['vlan_tag'].to_s
    end
    
    # if nic ip is empty
    if nic_info['nic_ip'].to_s.empty?
      nic_ip = ""
    else
      nic_ip = nic_info['nic_ip']
    end
      
    # if public network, use manual configuration 
    if net_type == 'P'
      source_file = 'external_nic_conf.erb'
      configureNetworkCard(nic_name, nic_device, nic_ip, nic_info, source_file)
    
      # loop through the node nic config and setup it
      nic_info['float_net_list'].each do |cidr_val, float_info|
        nic_name = nic_info['nic_name'] + "." + float_info['vlan_tag'].to_s 
        configureNetworkCard(nic_name, nic_device, nic_ip, float_info, source_file)
      end
      
    else
      source_file = 'nic_conf.erb'
      configureNetworkCard(nic_name, nic_device, nic_ip, nic_info, source_file)
    end
            
  end
  
end