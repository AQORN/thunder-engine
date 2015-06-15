# Cookbook name :: common.rb
# Recipe :: default
#
# Copyright 2015, AQORN
#
# All rights reserved - Do Not Redistribute
#

# Function to comment the nic info from the n/w interface file
#
# nic           The nic info to be commented
#
# @return       status
def updateNicInfo(nic)
  
  # Initialise the data variables
  file_content = []
  found = false
  
  # Read the file and comments the nic info, if found
  File.open('/etc/network/interfaces') do |f|
    f.lines.each do |line|
      line = line.gsub("\n", "")
      line = line.gsub('"', "")
  
      # To check whether a nic block is ended
      if (found == true) && (not(line.include? "auto")) && (not(line.include? "source"))
          line = "#".concat(line)
      end
  
      # To unset flag
      if (line.include? "auto") || (line.include? "source")
          found = false
      end
  
      # To check the nic block - start
      if line == "auto #{nic}"
        line = "#".concat(line)
        found = true
      end
      
      # Add the line to file content array
      file_content << line
    end
  end
  
  # To write the content to the destination file with updated data
  File.open("/etc/network/interfaces", "w+") do |f|
    f.puts(file_content)
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
# nic_info - nic information details
# source_file - the source file used to setup nic_name
#
def configureNetworkCard(nic_info, source_file)
  
  # add interfaces entry
  template "/etc/network/interfaces.d/ifcfg-#{nic_info['nic_name']}" do
    source source_file
    variables(
      nic_name: nic_info['nic_name'],
      nic_ip: nic_info['nic_ip'],
      nic_subnet: nic_info['nic_subnet'],
      nic_gateway: nic_info['nic_gateway'],
      nic_dns: nic_info['nic_dns']
    )
  end
  
  # down the NIC
  execute "down #{nic_info['nic_name']}" do
    command "ifdown #{nic_info['nic_name']}"
    #only_if "ifconfig | grep '#{nic_info['nic_name']}'"
  end
  
  # up the NIC 
  execute "up #{nic_info['nic_name']}" do
    command "ifup #{nic_info['nic_name']}"
    #not_if "ifconfig | grep '#{nic_info['nic_name']}'"
  end
  
  # setup ip temporarly
  execute "setup ip #{nic_info['nic_ip']} in #{nic_info['nic_name']} #{nic_info['nic_subnet']}" do
    command "ifconfig #{nic_info['nic_name']} #{nic_info['nic_ip']} netmask #{nic_info['nic_subnet']} down"
    action :run
  end
  
  # setup ip temporarly
  execute "setup ip #{nic_info['nic_ip']} in #{nic_info['nic_name']} #{nic_info['nic_subnet']}" do
    command "ifconfig #{nic_info['nic_name']} #{nic_info['nic_ip']} netmask #{nic_info['nic_subnet']} up"
    action :run
  end
  
  ## if enable network
  #ifconfig nic_ip do
  #  action  :enable
  #  device  nic_name
  #end
  
end