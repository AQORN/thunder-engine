# @author: Binoy M V
# @create_date: 20-May-2015
# @modified by: Binoy M V
# @modified_date: 20-May-2015
# @linking to other page: 
# @description: The recipe to up the service cobbler

# Command to restart cobbler
execute "cobbler-restart" do
  command "/etc/init.d/cobbler restart"
  action :run
end