# @author: Geo Varghese
# @create_date: 10-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 10-Apr-2015
# @linking to other page: 
# @description: The common matching functions

# check for defined or not
if defined?(ChefSpec)
  
  # matcher function to create the network
  #
  # resource_name   The name of the resource 
  def create_network_thunder_setup_network(resource_name)
    ChefSpec::Matchers::ResourceMatcher.new(:thunder_setup_network, :create_network, resource_name)
  end
  
  # matcher function to create the subnet
  #
  # resource_name   The name of the resource 
  def create_subnet_thunder_setup_network(resource_name)
    ChefSpec::Matchers::ResourceMatcher.new(:thunder_setup_network, :create_subnet, resource_name)
  end
  
  # matcher function to create the router
  #
  # resource_name   The name of the resource 
  def create_router_thunder_setup_network(resource_name)
    ChefSpec::Matchers::ResourceMatcher.new(:thunder_setup_network, :create_router, resource_name)
  end
  
  # matcher function to create the router attachment
  #
  # resource_name   The name of the resource 
  def create_router_attach_thunder_setup_network(resource_name)
    ChefSpec::Matchers::ResourceMatcher.new(:thunder_setup_network, :create_router_attach, resource_name)
  end
  
end
