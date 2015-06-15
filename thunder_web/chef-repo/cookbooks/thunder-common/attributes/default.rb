# @author: Geo Varghese
# @create_date: 3-June-2015
# @modified by: Geo Varghese    
# @modified_date: 3-June-2015
# @linking to other page: 
# @description: The default attribute to thunder common

# thunder common options
default['thunder']['common'] = {
  'package_options' => "-o Dpkg::Options::='--force-confold' -o Dpkg::Options::='--force-confdef'"
}