# @author: Geo Varghese
# @create_date: 27-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Mar-2015
# @linking to other page: 
# @description: The recipe to revoke compute node

# remove compute related packages
platform_options = node['openstack']['compute']['platform']
pkg_type_list = [
  'common_packages', 'memcache_python_packages', 'compute_compute_packages',
  'qemu_compute_packages', 'kvm_compute_packages'
]
removePackageList(platform_options, pkg_type_list)

# remove neutron related packages
platform_options = node['openstack']['network']['platform']
pkg_type_list = [
  'neutron_openvswitch_packages', 'neutron_openvswitch_agent_packages', 'neutron_metadata_agent_packages'
]
removePackageList(platform_options, pkg_type_list)