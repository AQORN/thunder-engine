# @author: Geo Varghese
# @create_date: 24-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 24-Mar-2015
# @linking to other page: 
# @description: The recipe to setup compute node

# setup node for installation
include_recipe 'thunder-setup::setup_node'

# install dependent modules
platform_options = node['thunder']['setup']
node['thunder']['setup']['compute_packages'].each do |pkg|
  package pkg do
    options platform_options['package_options']
    action :upgrade
  end
end