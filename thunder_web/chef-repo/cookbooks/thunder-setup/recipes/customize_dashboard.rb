# @author: Geo Varghese
# @create_date: 9-June-2015
# @modified by: Geo Varghese    
# @modified_date: 9-June-2015
# @linking to other page: 
# @description: The recipe to customize openstack dashboard

# rubocop:disable Documentation
class ::Chef::Recipe
  include ::Openstack
end

# change main title of dash board
ruby_block "Change the main title of dashboard" do
  block do
    fe = Chef::Util::FileEdit.new("/usr/share/openstack-dashboard/openstack_dashboard/settings.py")
    fe.search_file_replace(
      /SITE_BRANDING = 'OpenStack Dashboard'/,
      "SITE_BRANDING = 'AQORN Thunder - Horizon'"
    )
    fe.write_file
  end
end

# change splash logo
cookbook_file "/usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/img/logo-splash.png" do
  source 'dashboard_logo-splash.png'
  mode   00755
  action :create
end

# change main logo
cookbook_file "/usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/img/logo.png" do
  source 'dashboard_logo.png'
  mode   00755
  action :create
end

# get details for the localrc file
identity_endpoint = endpoint 'identity-api'
auth_uri = identity_endpoint.to_s
admin_tenant = node['openstack']['identity']['admin_tenant_name']  
admin_user = node['openstack']['identity']['admin_user']
admin_pass = get_password 'user', node['openstack']['identity']['admin_user']

# add localrc entry
template '/usr/bin/localrc' do
  source 'localrc.erb'
  variables(
    os_username: admin_user,
    os_tenant_name: admin_tenant,
    os_password: admin_pass,
    os_auth_uri: auth_uri
  )  
end

# restart apache after changes
service "apache2" do
  action :restart
end