# @author: Geo Varghese
# @create_date: 6-May-2015
# @modified by: Geo Varghese    
# @modified_date: 6-May-2015
# @linking to other page: 
# @description: The recipe to reboot node

include Chef::Provider::Reboot

# reboot node
reboot "reboot node" do
  action :request_reboot
  reason "Needs to reboot to continue"
end