# @author: Geo Varghese
# @create_date: 27-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Mar-2015
# @linking to other page: 
# @description: The recipe to revoke block storage

# remove cinder related packages
platform_options = node['openstack']['block-storage']['platform']
pkg_type_list = [
  'cinder_volume_packages', 'cinder_ceph_packages',
]
removePackageList(platform_options, pkg_type_list)
