# @author: Geo Varghese
# @create_date: 27-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Mar-2015
# @linking to other page: 
# @description: The recipe to revoke object storage node

# remove swift related packages
platform_options = node['openstack']['object-storage']['platform']
pkg_type_list = [
  'object_packages', 'container_packages', 'account_packages'
]
removePackageList(platform_options, pkg_type_list)