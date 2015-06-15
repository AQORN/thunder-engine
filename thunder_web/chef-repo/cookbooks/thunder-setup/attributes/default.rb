# @author: Geo Varghese
# @create_date: 23-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 23-Mar-2015
# @linking to other page: 
# @description: The default attribute to thunder setups

# the thunder package directories
default['thunder']['thunder_package_dir'] = '/var/lib/thunder_packages/'

# thunder setup packages
default['thunder']['setup'] = {
  'controller_packages' => [
    'gcc', 'python-dev', 'python-pip', 'python-oslo.config'
  ],
  'compute_packages' => ['python-dev'],
  'block_storage_packages' => ['python-dev'],
  'object_storage_packages' => ['python-dev'],
  'package_options' => "-o Dpkg::Options::='--force-confold' -o Dpkg::Options::='--force-confdef'"
}

# openstack network default values
default['thunder']['external_network'] = "ext-net"
default['thunder']['external_sub_network'] = "subnet"
default['thunder']['private_network'] = "private-net"
default['thunder']['private_sub_network'] = "private-subnet"
default['thunder']['router'] = "op-router"
  
# enable access to instances
default['thunder']['security_group']['ping'] = true
default['thunder']['security_group']['ssh'] = true