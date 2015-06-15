# @author: Geo Varghese
# @create_date: 10-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 10-Apr-2015
# @linking to other page: 
# @description: The recipe to create openstack networks

# rubocop:disable Documentation
class ::Chef::Recipe
  include ::Openstack
end

# get required variables
service_pass = get_password 'service', 'openstack-network'
service_tenant_name = node['openstack']['network']['service_tenant_name']
service_user = node['openstack']['network']['service_user']
identity_endpoint = endpoint 'identity-api'
auth_uri = identity_endpoint.to_s

# find admin tenant id
admin_tenant = node['openstack']['identity']['admin_tenant_name']  
admin_user = node['openstack']['identity']['admin_user']
is_insecure = node['openstack']['network']['api']['auth']['insecure']
cafile = node['openstack']['network']['api']['auth']['cafile']
args = {}
is_insecure && args['insecure'] = ''
cafile && args['os-cacert'] = cafile
env = openstack_command_env admin_user, admin_tenant
tenant_id = identity_uuid 'tenant', 'name', admin_tenant, env, args
Chef::Log.error('service tenant UUID for nova_admin_tenant_id not found.') if tenant_id.nil?

index = 1
router_name = node['thunder']['router'] + index.to_s
      
# create router
thunder_setup_network "Create router #{router_name}" do
  name router_name
  tenant_id tenant_id
  identity_user service_user
  identity_pass service_pass
  identity_tenant service_tenant_name
  identity_uri auth_uri
  action :create_router
end


# if floating ip list is not empty
if not node['thunder']['floatingip_list'].nil?
  
  # loop through floating IP list and create network
  node['thunder']['floatingip_list'].each_pair do |net_cidr, range_list|
  
    ip_info = range_list[0]
    extnet_name = node['thunder']['external_network'] + index.to_s
    
    # if not the first netowrk  
    if index != 1
      router_name = node['thunder']['router'] + index.to_s
        
      # create router
      thunder_setup_network "Create router #{router_name}" do
        name router_name
        tenant_id tenant_id
        identity_user service_user
        identity_pass service_pass
        identity_tenant service_tenant_name
        identity_uri auth_uri
        action :create_router
      end
    end
    
    # create external network
    thunder_setup_network "Create external network #{extnet_name}" do
      name extnet_name
      type "external"
      vlan_tag ip_info['vlan_tag']
      ext_net_name ip_info['ext_net_name']
      identity_user service_user
      identity_pass service_pass
      identity_tenant service_tenant_name
      identity_uri auth_uri
      action :create_network
    end
    
    # initialize and loop to find allocation pool string
    allocation_pool = ""
    for ip_info in range_list
      allocation_pool += " --allocation-pool start=#{ip_info['ip_range_from']},end=#{ip_info['ip_range_to']}"
    end
    
    subnet_name = extnet_name + "-" + node['thunder']['external_sub_network'] 
    
    # create public subnet
    thunder_setup_network "Create public subnet #{subnet_name}" do
      name subnet_name
      network extnet_name
      type "external"
      allocation_pool allocation_pool
      cidr  net_cidr
      identity_user service_user
      identity_pass service_pass
      identity_tenant service_tenant_name
      identity_uri auth_uri
      action :create_subnet
    end
    
    # create router gateway attachment
    thunder_setup_network "Create router gateway attachment" do
      name router_name
      network extnet_name
      type "gateway"
      tenant_id tenant_id
      identity_user service_user
      identity_pass service_pass
      identity_tenant service_tenant_name
      identity_uri auth_uri
      action :create_router_attach
    end
    
    index = index + 1
        
  end 
  
end

# create private network
thunder_setup_network "Create private network #{node['thunder']['private_network']}" do
  name node['thunder']['private_network']
  type "private"
  identity_user service_user
  identity_pass service_pass
  identity_tenant service_tenant_name
  identity_uri auth_uri
  action :create_network
end

index = 1

# if private net list is not empty
if not node['thunder']['private_netlist'].nil?

  # loop through private net list and create subnets
  node['thunder']['private_netlist'].each_pair do |net_id, ip_info|
  
    subnet_name = node['thunder']['private_sub_network'] + index.to_s
    index = index + 1
  
    # create private subnet
    thunder_setup_network "Create private subnet #{subnet_name}" do
      name subnet_name
      network node['thunder']['private_network']
      type "private"
      cidr ip_info['ip_cidr']
      identity_user service_user
      identity_pass service_pass
      identity_tenant service_tenant_name
      identity_uri auth_uri
      action :create_subnet
    end
    
    # create router interface attachment
    thunder_setup_network "Create router interface attachment" do
      name router_name
      network subnet_name
      type "interface"
      tenant_id tenant_id
      identity_user service_user
      identity_pass service_pass
      identity_tenant service_tenant_name
      identity_uri auth_uri
      action :create_router_attach
    end
    
  end
end

# get required variables to edit default security group
admin_pass = get_password 'user', node['openstack']['identity']['admin_user']
nova_cmd = "nova --os-username #{admin_user} --os-password #{admin_pass} --os-tenant-name #{admin_tenant} --os-auth-url #{auth_uri}"

# add icmp rules in default security group
if node['thunder']['security_group']['ping']
  executeCmd("#{nova_cmd} secgroup-add-rule default icmp -1 -1 0.0.0.0/0")
end

# add ssh rules in default security group
if node['thunder']['security_group']['ssh']
  executeCmd("#{nova_cmd} secgroup-add-rule default tcp 22 22 0.0.0.0/0")
end

# add public ip to public network bridge
if node['thunder']['role_code'] == 'controller' and !node['thunder']['pub_net_bridge'].to_s.empty?
  nic_info = node['thunder']['node_network']['P']
  source_file = 'nic_conf_without_vlan.erb'
  nic_name = node['thunder']['pub_net_bridge']
  nic_ip = nic_info['nic_ip']
  configureNetworkCard(nic_name, "", nic_ip, nic_info, source_file)
  
  # restart network
  execute "restart network" do
    command "/etc/init.d/networking restart"
    action :run
  end
  
end

# customize openstack for thunder
include_recipe 'thunder-setup::customize_dashboard'