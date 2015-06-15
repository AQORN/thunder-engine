#
# Cookbook Name:: galera
# Recipe:: server
#
# rubocop:disable LineLength

include_recipe 'ktc-package'
include_recipe 'ktc-utils'

install_flag = node['galera']['install_flag']

group 'mysql' do
end

user 'mysql' do
  gid 'mysql'
  comment 'MySQL server'
  system true
  shell '/bin/false'
end

remote_file "#{Chef::Config[:file_cache_path]}/#{node['galera']['mysql_tgz']}" do
  source "#{node['galera']['uri']}/#{node['galera']['mysql_tgz']}"
  action :create_if_missing
end

# strip .tar.gz
mysql_package = node['galera']['mysql_tgz'][0..-8]
bash 'install-mysql-package' do
  user 'root'
  code <<-EOH
    zcat #{Chef::Config[:file_cache_path]}/#{node['galera']['mysql_tgz']} | tar xf - -C #{node['mysql']['install_dir']}
    ln -sf #{node['mysql']['install_dir']}/#{mysql_package} #{node['mysql']['base_dir']}
  EOH
  not_if { File.directory?("#{node['mysql']['install_dir']}/#{mysql_package}") }
end

case node['platform']
when 'centos', 'redhat', 'fedora', 'suse', 'scientific', 'amazon'
  bash 'purge-mysql-galera' do
    user 'root'
    code <<-EOH
      killall -9 mysqld_safe mysqld &> /dev/null
      yum remove mysql mysql-libs mysql-devel mysql-server mysql-bench
      cd #{node['mysql']['data_dir']}
      [ $? -eq 0 ] && rm -rf #{node['mysql']['data_dir']}/*
      rm -rf /etc/my.cnf /etc/mysql
      rm -f /root/#{install_flag}
    EOH
    not_if { FileTest.exists?(install_flag) }
  end
else
  bash 'purge-mysql-galera' do
    user 'root'
    code <<-EOH
      killall -9 mysqld_safe mysqld &> /dev/null
      apt-get -y remove --purge mysql-server mysql-client mysql-common
      apt-get -y autoremove
      apt-get -y autoclean
      cd #{node['mysql']['data_dir']}
      [ $? -eq 0 ] && rm -rf #{node['mysql']['data_dir']}/*
      cd #{node['mysql']['conf_dir']}
      [ $? -eq 0 ] && rm -rf #{node['mysql']['conf_dir']}/*
      rm -f /root/#{install_flag}
    EOH
    not_if { FileTest.exists?(install_flag) }
  end
end

case node['platform']
when 'centos', 'redhat', 'fedora', 'suse', 'scientific', 'amazon'
  bash 'install-galera' do
    user 'root'
    code <<-EOH
      yum -y localinstall #{node['xtra']['packages']}
      yum -y install galera
    EOH
    not_if { FileTest.exists?(node['wsrep']['provider']) }
  end
else
  bash 'install-galera' do
    user 'root'
    code <<-EOH
      apt-get -y --force-yes install -o Dpkg::Options::="--force-confold" #{node['xtra']['packages']}
      apt-get -y --force-yes install -o Dpkg::Options::="--force-confold" galera
      apt-get -f install
    EOH
    not_if { FileTest.exists?(node['wsrep']['provider']) }
  end
end

[
  node['mysql']['conf_dir'],
  node['mysql']['data_dir'],
  node['mysql']['run_dir']
].each do |d|
  directory d do
    owner 'mysql'
    group 'mysql'
    mode '0755'
    action :create
    recursive true
  end
end

# install db to the data directory
dd_cmd = "#{node['mysql']['base_dir']}/scripts/mysql_install_db "
dd_cmd << '--force --user=mysql '
dd_cmd << "--basedir=#{node['mysql']['base_dir']} "
dd_cmd << "--datadir=#{node['mysql']['data_dir']}"
execute 'setup-mysql-datadir' do
  command dd_cmd
  not_if { FileTest.exists?("#{node['mysql']['data_dir']}/mysql/user.frm") }
end

service_cmd = 'cp '
service_cmd << "#{node['mysql']['base_dir']}/support-files/mysql.server "
service_cmd << "/etc/init.d/#{node['mysql']['servicename']}"

execute 'setup-init.d-mysql-service' do
  command service_cmd
  not_if { FileTest.exists?(install_flag) }
end

mysql_service = Services::Service.new 'mysql'
hosts = mysql_service.members.map { |m| m.ip }

wsrep_cluster_address = ''

ip = KTC::Network.address 'management'
# Assume that this mysql host has already been registered by ktc-database cook.
if hosts.length == 1 && hosts.sort.first == ip
  Chef::Log.info("I've got the galera init position.")
  node.run_state['galera'] ||= {}
  node.run_state['galera']['init_host'] = true
  wsrep_cluster_address = 'gcomm://'
else
  hosts.each do |h|
    unless h.eql? ip
      wsrep_cluster_address += "gcomm://#{h}:#{node['wsrep']['port']},"
    end
  end
  wsrep_cluster_address = wsrep_cluster_address[0..-2]
end

template 'my.cnf' do
  path "#{node['mysql']['conf_dir']}/my.cnf"
  source 'my.cnf.erb'
  owner 'mysql'
  group 'mysql'
  mode '0644'
  variables(
    wsrep_urls: wsrep_cluster_address,
    management_ip: ip
  )
  notifies :restart, 'service[mysql]', :immediately
end

include_recipe 'galera::first_run' unless FileTest.exists?(install_flag)

service 'mysql' do
  supports restart: true, start: true, stop: true
  service_name node['mysql']['servicename']
  action :enable
end
