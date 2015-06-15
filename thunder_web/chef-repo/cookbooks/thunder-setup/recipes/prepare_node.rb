# @author: Geo Varghese
# @create_date: 24-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 24-Mar-2015
# @linking to other page: 
# @description: The recipe to prepare a node for openstack component installation

# add local repo entry
template '/etc/apt/sources.list' do
  source 'sources-list.erb'
  variables(
    local_repo_ip: node['thunder']['local_repo_ip']
  )
end

# to fix authorization issue of packages
template '/etc/apt/apt.conf.d/99myown' do
  source '99myown.erb'
end

# execute apt-get update
execute "apt-get update" do
  command "apt-get update"
end

# install packages
platform_options = node['thunder']['setup']
package 'python-software-properties' do
  options platform_options['package_options']
  action :upgrade
end

# install keyring packages
package 'ubuntu-cloud-keyring' do
  options platform_options['package_options']
  action :upgrade
end

# install zabbix agent
package 'zabbix-agent' do
  options platform_options['package_options']
  action :upgrade
end