# @author: Geo Varghese
# @create_date: 27-Mar-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Mar-2015
# @linking to other page: 
# @description: The common thunder functions


# function to remove package list from node
#
# platform_options    The platform options to be used
# pkg_type_list       The package type list to be used
# 
def removePackageList(platform_options, pkg_type_list)
  
  # loop throup package types and remove
  pkg_type_list.each do |pkg_type|
    
    # loop through packages and remove
    platform_options[pkg_type].each do |pkg|
      package pkg do
        options platform_options['package_options']
        action :remove
      end
    end
    
  end
  
end


# function to install a python packages from source
#
# file_name  The name of the sorce file needs to downloaded in tar.gz file
#
def installSourcePythonPackage(file_name)
  
  download_file = node['thunder']['pkg_download_url'] + "/#{file_name}"    
  file_dir = node['thunder']['thunder_package_dir']
  file_path = File.join(file_dir,file_name)
  real_pkg_name = file_name.split(".tar.gz").first 
  uncompressed_file_dir = File.join(file_dir, real_pkg_name)
  
  # create directory
  directory file_dir do
    owner "deploy"
    group "deploy"
    mode "0755"
    recursive true
    action :create
  end
  
  # download source file
  remote_file file_path do
    source download_file
    mode "0644"
    not_if { File.exists?(file_path) }
  end
  
  # unzip file
  execute "gunzip #{file_name}" do
    command "gunzip -c #{file_name} | tar xf -"
    cwd file_dir
    not_if { File.exists?(uncompressed_file_dir) }
  end
  
  installed_file_path = File.join(uncompressed_file_dir, "installed")
  
  # install package
  execute "install python #{real_pkg_name} module" do
    command "python setup.py install"
    cwd uncompressed_file_dir
    not_if { File.exists?(installed_file_path) }
  end
  
  # create file path
  execute "touch #{installed_file_path}" do
    action :run
  end
  
end


# function to to download file in package directory
#
# file_name  The name of the sorce file needs to downloaded
#
def downloadFileInPackageDir(file_name)
  
  # file downloading directory
  file_dir = node['thunder']['thunder_package_dir']
  
  # create directory
  directory file_dir do
    owner "deploy"
    group "deploy"
    mode "0755"
    recursive true
    action :create
  end
  
  # download file
  execute "download file #{file_name}" do
    cwd "#{file_dir}"
    command "wget #{node['thunder']['pkg_download_url']}/#{file_name}"
    action :run
    only_if { !File.exists?("#{file_dir}/#{file_name}") }
  end
  
end

# function to execute command and return output
#
# command       The command to be executed
#
# @return   output of command / false
def executeCmd(command)
  puts "Command executed:::: #{command} ::::\n"
  cmd = Mixlib::ShellOut.new(command)
  cmd.run_command
  Chef::Log.debug "Command executed: #{command}"
  Chef::Log.debug "Command output: #{cmd.stdout}"
  begin
    cmd.error!
    return cmd.stdout.strip
  rescue
    return false
  end
   
end


# function to execute command and return output
#
# nic_name - nic name to be set[eth0.100, eth0 etc]
# nic_device - The physical name of nic[eth0, eth1 etc]
# nic_ip - the ip to set for nic_name
# nic_info - nic information details
# source_file - the source file used to setup nic_name
#
def configureNetworkCard(nic_name, nic_device, nic_ip, nic_info, source_file)
  
  # add interfaces entry
  template "/etc/network/interfaces.d/ifcfg-#{nic_name}" do
    source source_file
    variables(
      nic_name: nic_name,
      nic_device: nic_device,
      nic_ip: nic_ip,
      nic_subnet: nic_info['subnet'],
      nic_gateway: nic_info['gateway'],
      vlan_tag: if nic_info['vlan_tag'].to_s.empty? then false else nic_info['vlan_tag'] end
    )
  end
  
  # down the NIC
  execute "down #{nic_name}" do
    command "ifdown #{nic_name}"
    only_if "ifconfig | grep '#{nic_name} '"
  end
  
  # up the NIC 
  execute "up #{nic_name}" do
    command "ifup #{nic_name}"
    not_if "ifconfig | grep '#{nic_name} '"
  end
  
  ## if enable network
  #ifconfig nic_ip do
  #  action  :enable
  #  device  nic_name
  #end
  
end