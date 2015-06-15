# Cookbook name :: install_chef_server.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# Installs the chef server in the node
#dpkg_package 'chef-server' do
#    source "#{node['thunder']['deb_src_path']}/chef-server-core_12.0.7-1_amd64.deb"
#    action :install
#end

# Command to reconfigure request for chef-server
execute "chef-reconfigure" do
  command "chef-server-ctl reconfigure"
  action :run
end

# Configuring the chef server
execute "chef-server-user-create" do
  command "chef-server-ctl user-create deployment Aqorn Deployment deployment@aqorn.com test@123 --filename #{node['thunder']['chef_server_path']}/.chef/deployment.pem"
  action :run
  not_if "chef-server-ctl user-list | grep deployment"
end

# Configuring the chef server
execute "chef-server-org-create" do
  command "chef-server-ctl org-create aqorn Aqorn Inc  --association_user deployment --filename #{node['thunder']['chef_server_path']}/.chef/aqorn-validator.pem"
  action :run
  notifies :run, 'execute[chef-reconfigure]', :immediately
  not_if "chef-server-ctl org-list | grep aqorn"
end

# Command to fetch knife ssl
execute "fetch-ssl" do
  command "knife ssl fetch"
end

# Command to upload the cookbooks
execute "upload-cookbook" do
  cwd '/opt/thunder_web/chef-repo'
  command "knife upload cookbooks"
  action :run
end