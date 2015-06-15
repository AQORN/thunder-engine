#
# vim: set ft=ruby:
#

chef_api "https://chefdev.mkd2.ktc", node_name: "cookbook", client_key: ".cookbook.pem"

site :opscode

metadata

group "integration" do
  cookbook "etcd"
  cookbook "galera-test", path: "test/integration/cookbooks/galera-test"
  cookbook "ktc-testing"
end
