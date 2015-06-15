#
# Cookbook Name:: galera
# Recipe:: first_run
#
rs = node.run_state
init_host = false
unless rs['galera'].nil? || rs['galera']['init_host'].nil?
  init_host = rs['galera']['init_host']
end

# rubocop:disable LineLength
bash 'wait-until-synced' do
  user 'root'
  code <<-EOH
    state=0
    cnt=0
    until [[ "$state" == "4" || "$cnt" > 5 ]]
    do
      state=$(#{node['galera']['mysql_bin']} -uroot -h127.0.0.1 -e "SET wsrep_on=0; SHOW GLOBAL STATUS LIKE 'wsrep_local_state'")
      state=$(echo "$state"  | tr '\n' ' ' | awk '{print $4}')
      cnt=$(($cnt + 1))
      sleep 1
    done
  EOH
  only_if { init_host }
end

bash 'set-wsrep-grants-mysqldump' do
  user 'root'
  code <<-EOH
    #{node['galera']['mysql_bin']} -uroot -h127.0.0.1 -e "GRANT ALL ON *.* TO '#{node['wsrep']['user']}'@'%' IDENTIFIED BY '#{node['wsrep']['password']}'"
    #{node['galera']['mysql_bin']} -uroot -h127.0.0.1 -e "SET wsrep_on=0; GRANT ALL ON *.* TO '#{node['wsrep']['user']}'@'127.0.0.1' IDENTIFIED BY '#{node['wsrep']['password']}'"
  EOH
  only_if do
    init_host && (node['galera']['sst_method'] == 'mysqldump')
  end
end

bash 'secure-mysql' do
  user 'root'
  code <<-EOH
    #{node['galera']['mysql_bin']} -uroot -h127.0.0.1 -e "DROP DATABASE IF EXISTS test; DELETE FROM mysql.db WHERE DB='test' OR DB='test\\_%'"
    #{node['galera']['mysql_bin']} -uroot -h127.0.0.1 -e "UPDATE mysql.user SET Password=PASSWORD('#{node['mysql']['server_root_password']}') WHERE User='root'; DELETE FROM mysql.user WHERE User=''; DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1'); GRANT ALL ON *.* TO 'root'@'%' IDENTIFIED BY '#{node['mysql']['server_root_password']}' WITH GRANT OPTION; FLUSH PRIVILEGES;"
  EOH
  only_if do
    init_host && (node['galera']['secure'] == 'yes')
  end
end

execute 'galera-installed' do
  command "touch #{node['galera']['install_flag']}"
  action :run
end
