# borrowed from https://gist.github.com/2050259
# rubocop:disable FileName

provide 'ipaddress'
require_plugin "#{os}::network"
network['interfaces']['eth1']['addresses'].each do |ip, params|
  ipaddress ip if params['family'] == ('inet')
end
