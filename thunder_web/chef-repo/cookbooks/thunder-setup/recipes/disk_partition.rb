# @author: Geo Varghese
# @create_date: 8-May-2015
# @modified by: Geo Varghese    
# @modified_date: 8-May-2015
# @linking to other page: 
# @description: The recipe to setup database

# install format required package
platform_options = node['thunder']['setup']
package "xfsprogs" do
  options platform_options['package_options']
  action :upgrade
end

parted_label = "msdos"

# loop through the node disk config and setup it
node['thunder']['node_disk_list'].each do |disk_info|

  # if disk is not used for os installation
  if disk_info['device'] != node['thunder']['os_installation_disk']
    
    # create label for disk
    parted_disk 'making label' do
      device disk_info['device']
      label_type parted_label
      action :mklabel
    end
    
    parted_disk 'making part' do
      device disk_info['device']
      action :mkpart
      part_start disk_info['part_start']
      part_end disk_info['part_end']
      part_type disk_info['part_type']
    end
    
    # if role is object-storage
    if node['thunder']['role_code'] == 'object_storage'
      parted_disk 'making fs' do
        device disk_info['part_name']
        action :mkfs
      end
    end
    
  end
    
end
