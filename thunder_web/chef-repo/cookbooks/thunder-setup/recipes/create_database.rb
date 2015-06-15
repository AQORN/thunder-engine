# @author: Geo Varghese
# @create_date: 16-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 16-Mar-2015
# @linking to other page: 
# @description: The recipe to setup database

# include mysql database recipe
include_recipe 'mysql::server'
include_recipe 'database::mysql'

# point at localhost. hard code creds.
connection_info = {
  host: '127.0.0.1',
  username: 'root',
  password: node['mysql']['server_root_password']
}

# service db list
service_db_list = [ "identity", "compute", "image", "network", "block-storage", "dashboard"]

# loop through the service db list and create and grant access to database
for service_db_name in service_db_list
  
  # setup db details
  db_name = node['openstack']['db'][service_db_name]['db_name']
  db_username = node['openstack']['db'][service_db_name]['username']
  db_pass = get_password 'db', node['openstack']['db'][service_db_name]['username']
  
  # create database
  mysql_database db_name do
    connection connection_info
    action :create
  end
  
  # create user
  mysql_database_user db_username  do
    connection connection_info
    action :create
  end
  
  # if service is block storage provide access to other nodes
  if service_db_name == "block-storage"
    
    # grant all privileges to the user
    mysql_database_user db_username do
      connection connection_info
      database_name db_name
      password db_pass
      host '%'
      action :grant
    end
    
  else
  
    # grant all privileges to the user
    mysql_database_user db_username do
      connection connection_info
      database_name db_name
      password db_pass
      host node['thunder']['node_ip']
      action :grant
    end

  end
end