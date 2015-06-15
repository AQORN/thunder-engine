# @author: Geo Varghese
# @create_date: 10-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 10-Apr-2015
# @linking to other page: 
# @description: The common matching functions

# actions defined
actions :create_network, :create_subnet, :create_router, :create_router_attach

# In earlier versions of Chef the LWRP DSL doesn't support specifying
# a default action, so you need to drop into Ruby.
def initialize(*args)
  super
  @action = :create
end

attribute :name, kind_of: String
attribute :type, kind_of: String
attribute :network, kind_of: String
attribute :cidr, kind_of: String
attribute :start_ip, kind_of: String
attribute :end_ip, kind_of: String
attribute :identity_user, kind_of: String
attribute :identity_pass, kind_of: String
attribute :identity_tenant, kind_of: String
attribute :identity_uri, kind_of: String
attribute :tenant_id, kind_of: String
attribute :vlan_tag, kind_of: String
attribute :ext_net_name, kind_of: String
attribute :allocation_pool, kind_of: String