# @author: Geo Varghese
# @create_date: 10-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 10-Apr-2015
# @linking to other page: 
# @description: The common openstack network provider functions to create external, internal, router

# create network provider 
action :create_network do
  @user = new_resource.identity_user
  @pass = new_resource.identity_pass
  @tenant = new_resource.identity_tenant
  @ks_uri = new_resource.identity_uri
  name = new_resource.name
  type = new_resource.type
  neutron_cmd = "neutron --os-username #{@user} --os-password #{@pass} --os-tenant-name #{@tenant} --os-auth-url #{@ks_uri}"
  
  # if type is external network
  if type == 'external'
  
    vlan_tag = new_resource.vlan_tag
    ext_net_name = new_resource.ext_net_name
    command_str = "#{neutron_cmd} net-create #{name} --shared --router:external=True"
    command_str << " --provider:physical_network #{ext_net_name} --provider:network_type flat"
    
    # create network if not existing
    execute "create external network #{name}" do
      command command_str
      not_if "#{neutron_cmd} net-show #{name.to_s} | grep '| #{name.to_s}'"
    end
    
  else
    
    # create network if not existing
    execute "create private network #{name}" do
      command "#{neutron_cmd} net-create #{name} --shared"
      not_if "#{neutron_cmd} net-show #{name.to_s} | grep '| #{name.to_s}'"
    end
    
  end
  
end

# create subnet provider 
action :create_subnet do
  @user = new_resource.identity_user
  @pass = new_resource.identity_pass
  @tenant = new_resource.identity_tenant
  @ks_uri = new_resource.identity_uri
  name = new_resource.name
  type = new_resource.type
  cidr = new_resource.cidr
  network = new_resource.network
  neutron_cmd = "neutron --os-username #{@user} --os-password #{@pass} --os-tenant-name #{@tenant} --os-auth-url #{@ks_uri}"
  
  # if type is external network
  if type == 'external'
    
    allocation_pool = new_resource.allocation_pool
    
    # create external sub net
    execute "create external sub net #{name}" do
      command "#{neutron_cmd} subnet-create #{network} --name #{name} #{allocation_pool} --disable-dhcp #{cidr}"
      not_if "#{neutron_cmd} subnet-show #{name.to_s} | grep '| #{name.to_s}'"
    end
    
  else
    
    # create private sub net 
    execute "create private sub net #{name}" do
      command "#{neutron_cmd} subnet-create #{network} --name #{name} #{cidr}"
      not_if "#{neutron_cmd} subnet-show #{name.to_s} | grep '| #{name.to_s}'"
    end
    
  end
  
end

# create router 
action :create_router do
  @user = new_resource.identity_user
  @pass = new_resource.identity_pass
  @tenant = new_resource.identity_tenant
  @ks_uri = new_resource.identity_uri
  name = new_resource.name
  tenant_id = new_resource.tenant_id
  neutron_cmd = "neutron --os-username #{@user} --os-password #{@pass} --os-tenant-name #{@tenant} --os-auth-url #{@ks_uri}"
  
  # create router
  execute "create router #{name}" do
    command "#{neutron_cmd} router-create #{name} --tenant-id #{tenant_id}"
    not_if "#{neutron_cmd} router-show #{name.to_s} | grep '| #{name.to_s}'"
  end
    
end

# create router attachment 
action :create_router_attach do
  @user = new_resource.identity_user
  @pass = new_resource.identity_pass
  @tenant = new_resource.identity_tenant
  @ks_uri = new_resource.identity_uri
  name = new_resource.name
  type = new_resource.type
  network = new_resource.network
  neutron_cmd = "neutron --os-username #{@user} --os-password #{@pass} --os-tenant-name #{@tenant} --os-auth-url #{@ks_uri}"
  
  # check type of attachment
  if type == 'gateway'
    attach_option = "router-gateway-set"
    network_id = executeCmd("#{neutron_cmd} net-list | awk '/ #{network} / {print $2}'")
  else
    attach_option = "router-interface-add"
    network_id = executeCmd("#{neutron_cmd} subnet-list | awk '/ #{network} / {print $2}'")
  end
  
  # create router attachment
  execute "create router attachment" do
    command "#{neutron_cmd} #{attach_option} #{name} #{network}"
    not_if "#{neutron_cmd} router-port-list #{name} | grep '#{network_id}'"
  end
    
end