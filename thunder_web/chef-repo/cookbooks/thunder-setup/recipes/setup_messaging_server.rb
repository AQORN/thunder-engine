# @author: Geo Varghese
# @create_date: 18-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 18-Mar-2015
# @linking to other page: 
# @description: The recipe to setup messaging server

platform_options = node['thunder']['setup']
  
# install rabbitmq-server
package 'rabbitmq-server' do
  options platform_options['package_options']
  action :upgrade
end

# find username and password
user_name = node['openstack']['mq']['user']
user_pass = get_password 'user', user_name

# change password of user
cmd = "rabbitmqctl change_password #{user_name} #{user_pass}"
execute cmd do
  Chef::Log.debug "rabbitmq_user_change_password: #{cmd}"
  Chef::Log.info "Editing RabbitMQ user '#{user_name}'."
end
  
# commented due to taking external links and that links not working
## include rabbitmq install server recipe
#include_recipe 'rabbitmq::default'
#
## loop through rabbitmq users to be created
#node['rabbitmq']['enabled_users'].each do |user|
#  
#  # get user password
#  user_pass = get_password 'user', user['name']
#  
#  # create user
#  rabbitmq_user user['name'] do
#    password user_pass
#    action :add
#  end
#  
#  # set tags
#  rabbitmq_user user['name'] do
#    tag user['tag']
#    action :set_tags
#  end
#  
#  # set permissions
#  user['rights'].each  do |r|
#    rabbitmq_user user['name'] do
#      vhost r['vhost']
#      permissions "#{r['conf']} #{r['write']} #{r['read']}"
#      action :set_permissions
#    end
#  end
#end