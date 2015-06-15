# @author: Geo Varghese
# @create_date: 27-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Mar-2015
# @linking to other page: 
# @description: The recipe to revoke controller node

# remove keystone related packages
platform_options = node['openstack']['identity']['platform']
pkg_type_list = ['keystone_packages', 'keystone_client_packages', 'memcache_python_packages']
removePackageList(platform_options, pkg_type_list)

# remove glance related packages
platform_options = node['openstack']['image']['platform']
pkg_type_list = ['image_packages', 'image_client_packages', 'ceph_packages']
removePackageList(platform_options, pkg_type_list)

# remove compute related packages
platform_options = node['openstack']['compute']['platform']
pkg_type_list = [
  'api_ec2_packages', 'api_os_compute_packages', 'compute_api_metadata_packages',
  'compute_client_packages', 'compute_scheduler_packages', 'compute_conductor_packages',
  'compute_vncproxy_packages', 'compute_vncproxy_consoleauth_packages', 'libvirt_packages',
  'libvirt_ceph_packages', 'compute_cert_packages', 'common_packages'
]
removePackageList(platform_options, pkg_type_list)

# remove neutron related packages
platform_options = node['openstack']['network']['platform']
pkg_type_list = [
  'neutron_packages', 'nova_network_packages', 'neutron_client_packages',
  'neutron_dhcp_packages', 'neutron_l3_packages', 'neutron_vpn_packages',
  'neutron_openvswitch_packages', 'neutron_openvswitch_agent_packages', 
  'neutron_metadata_agent_packages', 'neutron_server_packages'
]
removePackageList(platform_options, pkg_type_list)

# remove cinder related packages
platform_options = node['openstack']['block-storage']['platform']
pkg_type_list = [
  'cinder_common_packages', 'cinder_api_packages',
  'cinder_client_packages', 'cinder_scheduler_packages'
]
removePackageList(platform_options, pkg_type_list)

# remove swift related packages
platform_options = node['openstack']['object-storage']['platform']
pkg_type_list = [
  'proxy_packages', 'swift_packages', 'swift_client_packages'
]
removePackageList(platform_options, pkg_type_list)

# remove dashborad related packages
platform_options = node['openstack']['dashboard']['platform']
pkg_type_list = ['horizon_packages']
removePackageList(platform_options, pkg_type_list)