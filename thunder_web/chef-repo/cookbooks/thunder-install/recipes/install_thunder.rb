# Cookbook name :: install_thunder.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

## Creates the log folder
#directory "/var/log/thunder/" do
#  owner 'deploy'
#  group 'deploy'
#  mode '0755'
#  action :create
#end
#
## Start the detect node logs
#execute "detect-node-logs" do
#  command "/opt/thunder_web/thunder_detect_node > /var/log/thunder/detect.log&"
#  action :run
#end
#
## Start the monitor node logs
#execute "monitor-node-logs" do
#  command "/opt/thunder_web/thunder_monitor_node > /var/log/thunder/monitor.log&"
#  action :run
#end
#
## Start the process job logs
#execute "process-job-logs" do
#  command "/opt/thunder_web/thunder_process_job > /var/log/thunder/job.log&"
#  action :run
#end

# Replace the sources list file
template '/etc/apt/sources.list' do
  source 'sources-list.erb'
end

# Set the timezone for zabbix
bash "set-timezone" do
  code <<-EOH
  timezone=$(cat /etc/timezone)
  
  perl -pi -e "\$str=q{date.timezone = \"$timezone\"}; s/date.timezone
  =/\$str/" /etc/php5/apache2/php.ini
  
  perl -pi -e "\$str=q{php_value date.timezone $timezone}; s/ php_value
  date.timezone Europe\/Riga/\$str/" /etc/apache2/sites-enabled/zabbix.conf
  EOH
end