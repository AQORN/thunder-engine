#Thunder - Openstack Deployment Guide Using Chef

## 1. Environment Preparation & Prerequisites

**All openstack installation nodes with OS:** ubuntu-12.04.2-server-amd64.iso
###Workstation
* 64 bit linux OS 
* Chef development toolkit(**Ref:** https://learn.chef.io/ubuntu/configure-a-resource/)

###Controller Nodes: 
* ubuntu-12.04.2-server-amd64.iso
* RabbitMQ-server
* Mysql-server

### Compute Nodes
* ubuntu-12.04.2-server-amd64.iso


## 2. Setup

### workstation

#### * Chef development toolkit

**Ref:** https://learn.chef.io/ubuntu/configure-a-resource/

Use above link and install chef development toolkit.

<pre>
wget https://opscode-omnibus-packages.s3.amazonaws.com/ubuntu/12.04/x86_64/chefdk_0.3.5-1_amd64.deb
dpkg -i chefdk_0.3.5-1_amd64.deb
</pre>

Checkout chef-repo from repository and manage cookbooks from it.

#### * Chef Commands:

**- Change directory to chef-repo before executing any chef commands**

<pre>
cd /root/chef-repo/cookbooks/
</pre>

**- To upload cookbook to chef server.**

<pre>
knife cookbook upload openstack-network
</pre>

The above command will upload cookbook 'openstack-network' to chef-server  

**- To deploy a cookbook recipie to the nodes**

<pre>
knife bootstrap 192.168.122.131 --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 -run-list 'recipe[openstack-image::api]'
</pre>

The above command will deploy recipie 'openstack-image::api' to the node with IP '192.168.122.131' as root user and will add node name as 'node1'. Please replace **USERNAME** and **XXXX** with username and password.

#### * Databags Creation

**Generate a key to create databag**

<pre>
openssl rand -base64 512 | tr -d '\r\n' > /etc/chef/openstack_data_bag_secret
</pre>

Copy this '/etc/chef/openstack_data_bag_secret' file to all nodes to same location


**Create databags using following commands**

**user_passwords ITEM example :** {"id" : "admin", "admin" : "mypass"}

<pre>
knife data bag create user_passwords admin --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create user_passwords guest --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
</pre>

**db_passwords ITEM example :** {"id" : "nova", "nova" : "mypass"}

<pre>
knife data bag create db_passwords nova --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords horizon --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords keystone --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords glance --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords neutron --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords dash --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create db_passwords cinder --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
</pre>

**service_passwords ITEM example :** {"id" : "openstack-image", "openstack-image" : "mypass"}

<pre>
knife data bag create service_passwords openstack-image --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create service_passwords openstack-compute --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create service_passwords openstack-network --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi

</pre>

**secrets ITEM example :** {"id" : "openstack_identity_bootstrap_token", "openstack_identity_bootstrap_token" : "mytoken"}

<pre>
knife data bag create secrets openstack_identity_bootstrap_token --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
knife data bag create secrets neutron_metadata_secret --secret-file /etc/chef/openstack_data_bag_secret --editor /usr/bin/vi
</pre>


### Controller Node

#### * Environment setup

**Openstack packages**

Ref: http://docs.openstack.org/icehouse/install-guide/install/apt/content/basics-packages.html

<pre>
apt-get install python-software-properties
add-apt-repository cloud-archive:icehouse
apt-get update
apt-get install python-pip
pip install oslo.middleware
</pre>

#### * Setup Mysql

Ref: http://docs.openstack.org/icehouse/install-guide/install/apt/content/basics-database-controller.html 

Do all steps in the above link.

Create following databases

<pre>
create database keystone;
grant all privileges on  keystone.* to keystone@'%' identified by 'keystone';

create database nova;
grant all privileges on  nova.* to nova@'%' identified by 'nova';

create database neutron;
grant all privileges on  neutron.* to neutron@'%' identified by 'neutron';

create database glance;
grant all privileges on  glance.* to glance@'%' identified by 'glance';

create database cinder;
grant all privileges on  cinder.* to cinder@'%' identified by 'cinder';
</pre>

#### * Setup Rabbitmq

<pre>
apt-get install rabbitmq-server
</pre>

### Compute Node

#### * Environment setup

**Openstack packages**

Ref: http://docs.openstack.org/icehouse/install-guide/install/apt/content/basics-packages.html

<pre>
apt-get install python-software-properties
add-apt-repository cloud-archive:icehouse
apt-get update
</pre>

## 3. Chef Deployment Details 

### Controller Node

#### * Deploy keystone

**Common Attributes**

**File** cookbooks/openstack-common/attributes/default.rb

- The openstack-common cookbook's default library contains a `secret` routine that looks up the value of encrypted databag values. This routine uses the secret key file located at the following location to decrypt the values in the data bag.

`default['openstack']['secret']['key_path'] = '/etc/chef/openstack_data_bag_secret'`

- The name of the encrypted data bag that stores openstack secrets

`default['openstack']['secret']['secrets_data_bag'] = 'secrets'`

- The name of the encrypted data bag that stores service user passwords, with each key in the data bag corresponding to a named OpenStack service, like  "nova", "cinder", etc.

`default['openstack']['secret']['service_passwords_data_bag'] = 'service_passwords'`

- The name of the encrypted data bag that stores DB passwords, with each key in the data bag corresponding to a named OpenStack database, like "nova", "cinder", etc.

`default['openstack']['secret']['db_passwords_data_bag'] = 'db_passwords'`

- The name of the encrypted data bag that stores Keystone user passwords, with each key in the data bag corresponding to a user (Keystone or otherwise).

`default['openstack']['secret']['user_passwords_data_bag'] = 'user_passwords'`

- OpenStack Identity Endpoint host name as controller. So that we can endpoints like https://controller:5000/v2.0 
We need to controller in /etc/hosts of openstack installation nodes

`default['openstack']['endpoints']['host'] = 'controller'`

- We are giving it as 0.0.0.0 to access the openstack services from different compute nodes

`default['openstack']['endpoints']['bind-host'] = '0.0.0.0'`

**File:** cookbooks/openstack-common/attributes/messaging.rb

The messaging server host as 'controller' to change IP at any time by editing the /ettc/hosts

`default['openstack']['endpoints']['mq']['host'] = 'controller'`

If you are using HA with rabbitmq, then please add HA nodes in the below array and also enable HA
default['openstack']['mq']['servers'] = ['rabbit1', 'rabbit2']
default['openstack']['mq']['ha'] = true

**File:** cookbooks/openstack-common/attributes/database.rb

`default['openstack']['endpoints']['db']['host'] = 'loadbalancer'`

All database specific settings are added in this file. Add /etc/hosts entry for **loadbalancer**. If you have loadbalancer setup give IP of it or give IP of database node.

##### Use following commands to deploy keystone to controller

**Deploy keystone server**

<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-identity::server]'
</pre>

**Deploy keystone client**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-identity::client]'
</pre>

**Create required default logins**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-identity::registration]'
</pre>

After successfull deployement we will get following  api end points.

**API End Points**
<pre>
Identity api uri = 'http://Controller:35357/v2.0'
Identity admin uri = 'http://controller:5000/v2.0'
</pre>

**Note:** Replace  SERVERIP, USERNAME, XXXX with node ip, username and password

#### * Deploy Glance

**Default Attributes**

**File:** cookbooks/openstack-image/attributes/default.rb

- The default store of image as 'file' and also store images in the location '/var/lib/glance/images'

`default['openstack']['image']['api']['default_store'] = 'file'`
`default['openstack']['image']['filesystem_store_datadir'] = '/var/lib/glance/images'`

Use following commands to deploy glance to controller

**Install glance api service**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-image::api]'
</pre>

<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-image::registry]'
</pre>

**deploy glance registry services**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-image::identity_registration]'
</pre>

**Upload a os image to glance to use while creating instance**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-image::image_upload]'
</pre>

After successfull deployement we will get following  api end points.

**API End Points**
<pre>
Image api uri = 'http://controller:9292/v2
Image registry uri = http://controller:9191/v2
</pre>

#### * Deploy Compute services

**Default Attributes**

**File:** cookbooks/openstack-compute/attributes/default.rb

- Support multiple network types.  Default network type is 'nova', we need to give other option supported being 'neutron'
`default['openstack']['compute']['network']['service_type'] = 'neutron'`

Use following commands to deploy compute services to controller

**To deploy nova- setup softwares**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::nova-setup]'
</pre>

**To setup api-os-compute service**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::api-os-compute]'
</pre>

**To setup nova compute service**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::conductor]'
</pre>

**To setup nova client**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::client]'
</pre>

**To created required identities and also api endpoints**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::identity_registration]'
</pre>

**To setup nova cert service**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::nova-cert]'
</pre>

**To setup nova scheduler service**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::scheduler]'
</pre>

**To deploy nova console service to access VM through dashboard console**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-compute::vncproxy]'
</pre>


**To fix the issue ImportError: No module named compute_req_id**

Login to controller node and execute following commands

<pre>
cd /usr/lib/python2.7/dist-packages/nova/api/
wget https://raw.githubusercontent.com/openstack/nova/master/nova/api/compute_req_id.py
service nova-api-os-compute restart
</pre>

After successfull deployement we will get following  api end points.

**API End Points**
<pre>
Compute-api uri = 'https://compute.example.com:8774/v2/%(tenant_id)s'
</pre>

#### * Deploy Neutron

**Default Attributes**

**File:** cookbooks/openstack-network/attributes/default.rb

- The location of the Nova Metadata API service to proxy to (nil uses default)

`default['openstack']['network']['metadata']['nova_metadata_ip'] = 'controller'`

- Type of network to allocate for tenant networks.
`default['openstack']['network']['openvswitch']['tenant_network_type'] = 'gre'`

- Set to True in the server and the agents to enable support for GRE
`default['openstack']['network']['openvswitch']['enable_tunneling'] = 'True'`

- The type of tunnel network, if any, supported by the plugin.
`default['openstack']['network']['openvswitch']['tunnel_type'] = 'gre'`

- Firewall driver for realizing neutron security group function
`default['openstack']['network']['openvswitch']['fw_driver'] = 'neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver'`

- Interface to use for external bridge. Given 'eth0' for one network interface setup. Oherwise give it as 'eth1'
`default['openstack']['network']['l3']['external_network_bridge_interface'] = 'eth0'`

##### Use following commands to deploy neutron services to controller

**To deploy neutron server**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::server]'
</pre>

**To deploy neutron client**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::client]'
</pre>

**To deploy DHCP agent for IP allocation to VMs**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::dhcp_agent]'
</pre>

**To deploy metadata agent to setup remote connection between the VMs**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::metadata_agent]'
</pre>

**To create required identities and api end points**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::identity_registration]'
</pre>

**To deploy openvswitch plugin to setup required bridges and ports**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::openvswitch]'
</pre>

**To deploy l3 agent for create required bridges like br-ex**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-network::l3_agent]'
</pre>

**Note:** no module named rootwrap.cmd

Can be fixed by executing following command in controller

`cp -a /usr/lib/python2.7/dist-packages/oslo/rootwrap/ /usr/local/lib/python2.7/dist-packages/oslo`


#### * Deploy Dashboard

**Default Attributes**

**File:** cookbooks/openstack-dashboard/attributes/default.rb

- The hostname of dashbaord to add in apache conf. If not give we can access it through default IP of controller

`default['openstack']['dashboard']['server_hostname'] = nil`

- Set this if you ra eusing https connection

`default['openstack']['dashboard']['use_ssl'] = false`

- The ports use dfor both http an dhttps connection. Currently default ports are added.

`default['openstack']['dashboard']['http_port'] = 80`
`default['openstack']['dashboard']['https_port'] = 443`

##### Use following commands to deploy dashboard services to controller

**To deploy dashboard server**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node1 --run-list 'recipe[openstack-dashboard::server]'
</pre>

After success deployment you can access the dashboard using following link

[http://controller/](http://controller/)

**username:** admin
**password:** The password given in databag

**Note:** Please set controller IP in you /etc/hosts


### Compute Node

#### * Deploy Compute

##### Use following commands to deploy dashboard services to controller

**To deploy nova compute**
<pre>
knife bootstrap SERVERIP --ssh-user USERNAME --ssh-password 'XXXX' --sudo --use-sudo-password --node-name node2 --run-list 'recipe[openstack-compute::compute]'
</pre>

Once the deployment is success, you can see new hypervisor in Hypervisor list in dashboard.

[http://controller/admin/hypervisors/](http://controller/admin/hypervisors/)


## 4. Deployment & Test Process

### Create Availability Zone

Availability zone is to group the hosts available and create vm in it.

Go to => [http://controller/admin/aggregates/](http://controller/admin/aggregates/)

Create new host aggregate and also give a name for availabilty zone. Add newly deployed compute node to availablity zone.

### Create networks

Create initial networks using following link

[http://docs.openstack.org/icehouse/install-guide/install/apt/content/neutron-initial-networks.html]

**Eg:** Commands executed in controller node to create intitial network

`vi /usr/bin/openstack.sh`

Add following content to the file

<pre>
export OS_USERNAME=admin
export OS_TENANT_NAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://controller:35357/v2.0
</pre>

Execute following command

`source /usr/bin/openstack.sh`

##### Create external network

- Create main network

`neutron net-create ext-net --shared --router:external=True`

- Create subnet. In this case 192.168.122.0 IP range is IP of our controller and compute node networks

`neutron subnet-create ext-net --name ext-subnet --allocation-pool start=192.168.122.122,end=192.168.122.155   --disable-dhcp --gateway 192.168.1.1 192.168.122.0/24`

##### Internal network(tenant network)

- create the tenant network

`neutron net-create demo-net`

- Create subnet

`neutron subnet-create demo-net --name demo-subnet --gateway 192.168.1.1 192.168.1.0/24`

### Router 

- neutron router-create demo-router

`neutron router-create demo-router`

- Attach the router to the demo tenant subnet:

`neutron router-interface-add demo-router demo-subnet`

-  Attach the router to the external network by setting it as the gateway:

`neutron router-gateway-set demo-router ext-net`

### Add rules to the default security group

**Permit ICMP (ping):**

`nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0`

**Permit secure shell (SSH) access:**

`nova secgroup-add-rule default tcp 22 22 0.0.0.0/0`


### Only one interface eth0 available

Comment eth0 entries in **/etc/network/interfaces** and add following content

<pre>
auto eth0
iface eth0 inet manual
  pre-up ifconfig $IFACE up
  post-down ifconfig $IFACE down
  gateway CONTROLLER_IP_GATEWAY
  dns-nameservers 8.8.8.8

auto br-ex
 iface br-ex inet static
 address CONTROLLER_IP
 netmask CONTROLLER_IP_NETMASK
 gateway CONTROLLER_IP_GATEWAY
</pre>

**Note:**
Replace CONTROLLER_IP, CONTROLLER_IP_NETMASK, CONTROLLER_IP_GATEWAY with corresponding values.

### Testing

#### Check all services are up by folowing step

Go to [http://controller/admin/info/](http://controller/admin/info/) and verify all services are up.

#### Create instance by following steps

a) Go to => http://controller/project/instances/ and launch a instance.

b) Associate a floating IP to the instance

3) Try ssh to instance floating IP from controller or compute node.


#### Issues and fixes

**1) No module named keystonemiddleware.auth_token**

Fixed by following commands

<pre>
apt-get install python-pip
pip install keystonemiddleware
</pre>

**2) no module named rootwrap.cmd**

Fixed by following command

<pre>
cp -a /usr/lib/python2.7/dist-packages/oslo/rootwrap/ /usr/local/lib/python2.7/dist-packages/oslo
</pre>

**3) ImportError: No module named compute_req_id**

Fixed by following step

<pre>
create a file /usr/lib/python2.7/dist-packages/nova/api/compute_req_id.py

and copy contents from => https://github.com/openstack/nova/blob/master/nova/api/compute_req_id.py

</pre>

**3) ImportError: No module named middleware**

Fixed by following step

<pre>
pip install oslo.middleware
</pre>


#Openstack High Avialabilty Setup

##Mysql galera cluster setup

Use following link.

###Common settings on all nodes


    **Install required packages**

<pre>
    apt-get update
    apt-get install libaio1 libssl0.9.8 mysql-client libdbd-mysql-perl libdbi-perl
</pre>

   **Download Galera wsrep provider**

<pre>
    wget https://launchpad.net/galera/2.x/23.2.4/+download/galera-23.2.4-amd64.deb
    dpkg -i galera-23.2.4-amd64.deb

</pre>

    **Download MySQL server with wsrep patch**

<pre>
    wget https://launchpad.net/codership-mysql/5.5/5.5.28-23.7/+download/mysql-server-wsrep-5.5.28-23.7-amd64.deb
    dpkg -i mysql-server-wsrep-5.5.28-23.7-amd64.deb
</pre>

    **Create /var/log/mysql if not existing**

<pre>
    mkdir -pv /var/log/mysql
    chown mysql:mysql -R /var/log/mysql
</pre>

    **Secure the mysql installation and assign a good password to root user:**

<pre>
    service mysql restart
    mysql_secure_installation
</pre>

    **Create an user for galera nodes to use for connect/replication**

<pre>
    mysql -p
    mysql> grant all privileges on **.** to galera@'%' identified by 'password';
    Query OK, 0 rows affected (0.00 sec)
</pre>

<pre>
    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)
</pre>

<pre>
    mysql> set global max_connect_errors = 10000;
    Query OK, 0 rows affected (0.01 sec)
</pre>


**Edit /etc/hosts and make sure you add all the nodes and their corresponding IPs**

###Galera setup for each node


####Edit the /etc/mysql/conf.d/wsrep.cnf and change the values for the following variables:

**Configuration for node01:**

<pre>
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_name="galera"
wsrep_cluster_address="gcomm://"
wsrep_sst_method=mysqldump
wsrep_sst_auth=galera:password
</pre>

**Configuration for node02:**

<pre>
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_name="galera"
wsrep_cluster_address="gcomm://node01:4567"
wsrep_sst_method=mysqldump
wsrep_sst_auth=galera:password
</pre>

**Configuration for node03:**

<pre>
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_name="galera"
wsrep_cluster_address="gcomm://node02:4567"
wsrep_sst_method=mysqldump
wsrep_sst_auth=galera:password
</pre>


###Start setup

**Now restart mysql on all the nodes and check out if cluster is working:**

service mysql restart

<pre>
mysql -p
mysql> show status like 'wsrep%';
+----------------------------+-------------------------------------------------------------+
| Variable_name | Value |
+----------------------------+-------------------------------------------------------------+
| wsrep_cluster_size | 3 |
| wsrep_ready | ON |
+----------------------------+-------------------------------------------------------------+
</pre>

**Note:**

<pre>
One more thing before you are done:
Edit node01 wsrep_cluster_address=”gcomm://node3:4567″ and restart mysql server.
</pre>

**Ref:** http://getasysadmin.com/2013/03/how-to-setup-galera-3-node-cluster-on-ubuntu-12-04/

##Rabbitmq cluster setup

###Install RabbitMQ

**execute following command on all nodes**

<pre>
apt-get install rabbitmq-server
</pre>


###Configure RabbitMQ

**We setup on 2 nodes with hostname rabbit1 & rabbit2**


####Copy .erlang.cookie from rabbit1 to rabbit2 into correct place as below section

**rabbit1**

<pre>
rabbitmqctl stop
scp /var/lib/rabbitmq/.erlang.cookie geo@rabbit2:/tmp/
service rabbitmq-server start
rabbitmqctl cluster_status
</pre>

**rabbit2**

<pre>
rabbitmqctl stop
cp /tmp/.erlang.cookie /var/lib/rabbitmq/.erlang.cookie
chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie
chmod 400 /var/lib/rabbitmq/.erlang.cookie
service rabbitmq-server start
rabbitmqctl cluster_status
rabbitmqctl stop_app
rabbitmqctl cluster rabbit@rabbit1
rabbitmqctl start_app
rabbitmqctl cluster_status
</pre>


####We have to configure the OpenStack components to use at least two RabbitMQ nodes.


**Do this configuration on all services using RabbitMQ:** RabbitMQ HA cluster host:port pairs:
    	
<pre>
    rabbit_hosts=rabbit1:5672,rabbit2:5672
</pre>

**How frequently to retry connecting with RabbitMQ:**
    	
<pre>
    rabbit_retry_interval=1
</pre>

**How long to back-off for between retries when connecting to RabbitMQ:**
    	
<pre>
    rabbit_retry_backoff=2
</pre>

**Maximum retries with trying to connect to RabbitMQ (infinite by default):**
    	
<pre>
    rabbit_max_retries=0
</pre>

**Use durable queues in RabbitMQ:**
    	
<pre>
    rabbit_durable_queues=false
</pre>

**Use HA queues in RabbitMQ (x-ha-policy: all):**
    	
<pre>
    rabbit_ha_queues=true
</pre>


####Cookbook configuratiosn for openstack Rabbitmq HA

**cookbooks/openstack-common/attributes/messaging.rb**

<pre>
default['openstack']['mq']['servers'] = ['rabbit1', 'rabbit2']
default['openstack']['mq']['ha'] = true
</pre>

**cookbooks/openstack-compute/attributes/default.rb**

<pre>
# the high availability service setup
# true to enable the service, false to disable the service
default['openstack']['mq']["compute"]["rabbit"]["ha"] = node['openstack']['mq']['ha']
</pre>

**cookbooks/openstack-compute/templates/default/nova.conf.erb**

<pre>
rabbit_retry_interval=1
rabbit_retry_backoff=2
rabbit_max_retries=0
rabbit_durable_queues=false
</pre>

**cookbooks/openstack-network/attributes/default.rb**

<pre>
# the high availability service setup
# true to enable the service, false to disable the service
default['openstack']['mq']["network"]["rabbit"]["ha"] = node['openstack']['mq']['ha'] 
</pre>

**cookbooks/openstack-network/templates/default/neutron.conf.erb**

<pre>
rabbit_retry_interval=1
rabbit_retry_backoff=2
rabbit_max_retries=0
rabbit_durable_queues=false
</pre>


**Ref:** http://docs.openstack.org/high-availability-guide/content/_configure_rabbitmq.html

##HA proxy setup

###Installation

**On the HAProxy server install the package.**

<pre>
root@haproxy# apt-get install haproxy
</pre>

**Enable HAProxy to be started by the init script.**

<pre>
root@haproxy# sed -i "s/ENABLED=0/ENABLED=1/" /etc/default/haproxy
</pre>

**To check if this change is done properly execute the init script of HAProxy without any parameters.**

<pre>
root@haproxy:~# service haproxy
Usage: /etc/init.d/haproxy {start|stop|reload|restart|status}
</pre>

###Prepare MySQL Servers

We need to prepare the MySQL servers by creating two additional users for HAProxy. The first user will be used by HAProxy to check the status of a server.

<pre>
mysql -u root -p -e "INSERT INTO mysql.user (Host,User) values ('10.0.0.100','haproxy_check'); FLUSH PRIVILEGES;"
</pre>

A MySQL user is needed with root privileges when accessing the MySQL cluster from HAProxy. The default root user on all the servers are allowed to login only locally. While this can be fixed by granting additional privileges to the root user, it is better to have a separate user with root privileges.

<pre>
mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO 'haproxy_root'@'10.0.0.100' IDENTIFIED BY 'password' WITH GRANT OPTION; FLUSH PRIVILEGES"
</pre>

Replace **10.0.0.100** with HA proxy IP.

Replace **haproxy_root** and **password** with your own secure values. It is enough to execute these queries on one MySQL master as changes will replicate to others.

###Configuring HAProxy

**Rename the original configuration file**

<pre>
mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.old
</pre>

**Create and edit a new one**

<pre>
vi /etc/haproxy/haproxy.cfg
</pre>

**Copy following content to teh file and replace 192.168.122.61 with HA proxy IP**

<pre>
global
    log 127.0.0.1 local0 notice
    user haproxy
    group haproxy

defaults
    log global
    retries 2
    timeout connect 3000
    timeout server 5000
    timeout client 5000
    maxconn  8000
    timeout  http-request 10s
    timeout  queue 1m
    timeout  check 10s

listen mysql-cluster
    bind 192.168.122.91:3306
    mode tcp
    option mysql-check user haproxy_check
    balance roundrobin
    server mysql-1 node01:3306 check
    server mysql-2 node02:3306 check

listen dashboard_cluster
  bind 192.168.122.91:80
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:80 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:80 check inter 2000 rise 2 fall 5

listen glance_api_cluster
  bind 192.168.122.91:9292
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:9292 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:9292 check inter 2000 rise 2 fall 5

listen glance_registry_cluster
  bind 192.168.122.91:9191
  balance  source
  option  tcpka
  option  tcplog
  server ctrl-1 controller1:9191 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:9191 check inter 2000 rise 2 fall 5

listen keystone_admin_cluster
  bind 192.168.122.91:35357
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:35357 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:35357 check inter 2000 rise 2 fall 5

listen keystone_public_internal_cluster
  bind 192.168.122.91:5000
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:5000 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:5000 check inter 2000 rise 2 fall 5

listen nova_compute_api_cluster
  bind 192.168.122.91:8774
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:8774 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:8774 check inter 2000 rise 2 fall 5

listen nova_metadata_api_cluster
  bind 192.168.122.91:8775
  balance  source
  option  tcpka
  option  tcplog
  server ctrl-1 controller1:8775 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:8775 check inter 2000 rise 2 fall 5

listen neutron_api_cluster
  bind 192.168.122.91:9696
  balance  source
  option  tcpka
  option  httpchk
  option  tcplog
  server ctrl-1 controller1:9696 check inter 2000 rise 2 fall 5
  server ctrl-2 controller2:9696 check inter 2000 rise 2 fall 5
</pre>

**Once you're done configuring start the HAProxy service.**

<pre>
service haproxy start
</pre>


###Configure Logging for HAProxy

When we began configuring HAProxy, we added a line: log 127.0.0.1 local0 notice which sends syslog messages to the localhost IP address. But by default, rsyslog on Ubuntu doesn't listen on any address. So we have to make it do so.

**Edit the config file of rsyslog.**

<pre>
vi /etc/rsyslog.conf
</pre>

**Add/Edit/Uncomment the following lines:**

<pre>
$ModLoad imudp
$UDPServerAddress 127.0.0.1
$UDPServerRun 514
</pre>


Now rsyslog will work on UDP port 514 on address 127.0.0.1 but all HAProxy messages will go to /var/log/syslog so we have to separate them.

**Create a rule for HAProxy logs.**

<pre>
vi /etc/rsyslog.d/haproxy.conf
</pre>

**Add the following line to it.**

<pre>
if ($programname == 'haproxy') then -/var/log/haproxy.log
</pre>

**Now restart the rsyslog service:**

<pre>
service rsyslog restart
</pre>

This writes all HAProxy messages and access logs to **/var/log/haproxy.log**


**refs:**

https://www.digitalocean.com/community/tutorials/how-to-use-haproxy-to-set-up-mysql-load-balancing--3

https://www.digitalocean.com/community/tutorials/how-to-use-haproxy-to-set-up-http-load-balancing-on-an-ubuntu-vps

http://docs.openstack.org/high-availability-guide/content/ha-aa-haproxy.html


##Pacemaker setup

###Installation


All examples assume two nodes that are reachable by their short name and IP address:

  node1 - 192.168.1.1
  node2 - 192.168.1.2

The convention followed is that 

[ALL] # denotes a command that needs to be run on all cluster machines
[ONE] # indicates a command that only needs to be run on one cluster host. 

Install required packages.

<pre>
[ALL] # apt-get install pacemaker cman fence-agents
</pre>

####Configure Cluster Membership and Messaging

Since the ccs tool from RHEL does not exist on Ubuntu, we well create the CMAN configuration file on both machines manually: 

<pre>
[ALL] # vi /etc/cluster/cluster.conf
</pre>

With following content

`<?xml version="1.0"?><cluster config_version="1" name="pacemaker1"> <logging debug="off"/> <clusternodes> <clusternode name="node1" nodeid="1"> <fence> <method name="pcmk-redirect"> <device name="pcmk" port="node1"/> </method> </fence> </clusternode> <clusternode name="node2" nodeid="2"> <fence> <method name="pcmk-redirect"> <device name="pcmk" port="node2"/> </method> </fence> </clusternode> </clusternodes> <fencedevices> <fencedevice name="pcmk" agent="fence_pcmk"/> </fencedevices> </cluster>`


**Note:** Add corresponding entries for node1 and node2 in /etc/hosts


CMAN was originally written for rgmanager and assumes the cluster should not start until the node has quorum, so before we try to start the cluster, we need to disable this behavior:

<pre>
[ALL] # echo "CMAN_QUORUM_TIMEOUT=0" >> /etc/default/cman
</pre> 


####Start the Cluster

On each machine, run:

<pre>
[ALL] # service cman start 
[ALL] # service pacemaker start
</pre>

####Set Cluster Options

With so many devices and possible topologies, it is nearly impossible to include Fencing in a document like this. For now we will disable it.

<pre>
[ONE] # crm configure property stonith-enabled=false
</pre>

One of the most common ways to deploy Pacemaker is in a 2-node configuration. However quorum as a concept makes no sense in this scenario (because you only have it when more than half the nodes are available), so we'll disable it too.

<pre>
[ONE] # crm configure property no-quorum-policy=ignore
</pre>

For demonstration purposes, we will force the cluster to move services after a single failure:

<pre>
[ONE] # crm configure property migration-threshold=1
</pre> 

**Refer:** http://clusterlabs.org/quickstart-ubuntu.html


####Starting Corosync

service corosync start

The **corosync-cfgtool** utility, when invoked with the -s option, gives a summary of the health of the communication rings:

<pre>
# corosync-cfgtool -s
    Printing ring status.
Local node ID 435324542
RING ID 0
        id      = 192.168.42.82
        status  = ring 0 active with no faults
RING ID 1
        id      = 10.0.42.100
        status  = ring 1 active with no faults
</pre>


The **corosync-objctl** utility can be used to dump the Corosync cluster member list:

<pre>
# corosync-objctl runtime.totem.pg.mrp.srp.members
    runtime.totem.pg.mrp.srp.435324542.ip=r(0) ip(192.168.42.82) r(1) ip(10.0.42.100)
runtime.totem.pg.mrp.srp.435324542.join_count=1
runtime.totem.pg.mrp.srp.435324542.status=joined
runtime.totem.pg.mrp.srp.983895584.ip=r(0) ip(192.168.42.87) r(1) ip(10.0.42.254)
runtime.totem.pg.mrp.srp.983895584.join_count=1
runtime.totem.pg.mrp.srp.983895584.status=joined
</pre>


####Start Pacemaker

service pacemaker start

Once Pacemaker services have started, Pacemaker will create a default empty cluster configuration with no resources. You may observe Pacemaker's status with the **crm_mon** utility:

<pre>
============
Last updated: Sun Oct  7 21:07:52 2012
Last change: Sun Oct  7 20:46:00 2012 via cibadmin on node2
Stack: openais
Current DC: node2 - partition with quorum
Version: 1.1.6-9971ebba4494012a93c03b40a2c58ec0eb60f50c
2 Nodes configured, 2 expected votes
0 Resources configured.
============

Online: [ node2 node1 ]
</pre>

####Set basic cluster properties

Once your Pacemaker cluster is set up, it is recommended to set a few basic cluster properties. To do so, start the crm shell and change into the configuration menu by entering configure. Alternatively, you may jump straight into the Pacemaker configuration menu by typing crm configure directly from a shell prompt.

Then, set the following properties:

<pre>
property no-quorum-policy="ignore" pe-warn-series-max="1000" pe-input-series-max="1000" pe-error-series-max="1000" cluster-recheck-interval="5min"
</pre>

###Network controller cluster stack

####Highly available neutron L3 agent

Add neutron L3 agent resource to Pacemaker

First of all, you need to download the resource agent to your system:


<pre>
# cd /usr/lib/ocf/resource.d/openstack
# wget https://raw.github.com/madkiss/openstack-resource-agents/master/ocf/neutron-agent-l3
# chmod a+rx neutron-l3-agent
</pre>

You may now proceed with adding the Pacemaker configuration for neutron L3 agent resource. Connect to the Pacemaker cluster with crm configure, and add the following cluster resources:

Execute

<pre>
crm configure
</pre>

Then execute following command

<pre>
primitive p_neutron-l3-agent ocf:openstack:neutron-agent-l3 params config="/etc/neutron/neutron.conf" plugin_config="/etc/neutron/l3_agent.ini" op monitor interval="30s" timeout="30s"
</pre>

This configuration creates

    p_neutron-l3-agent, a resource for manage Neutron L3 Agent service 

crm configure supports batch input, so you may copy and paste the above into your live pacemaker configuration, and then make changes as required.

Once completed, commit your configuration changes by entering commit from the crm configure menu. Pacemaker will then start the neutron L3 agent service, and its dependent resources, on one of your nodes.

<pre>
commit
</pre>


####Highly available neutron DHCP agent


Add neutron DHCP agent resource to Pacemaker

First of all, you need to download the resource agent to your system:

<pre>
# cd /usr/lib/ocf/resource.d/openstack
# wget https://raw.github.com/madkiss/openstack-resource-agents/master/ocf/neutron-agent-dhcp
# chmod a+rx neutron-agent-dhcp
</pre>


You may now proceed with adding the Pacemaker configuration for neutron DHCP agent resource. Connect to the Pacemaker cluster with crm configure, and add the following cluster resources:

Execute

<pre>
crm configure
</pre>

Then execute following command

<pre>
primitive p_neutron-dhcp-agent ocf:openstack:neutron-agent-dhcp params config="/etc/neutron/neutron.conf" plugin_config="/etc/neutron/dhcp_agent.ini" op monitor interval="30s" timeout="30s"
</pre>

commit the changes.

<pre>
commit
</pre>

####Highly available neutron metadata agent

Add neutron metadata agent resource to Pacemaker

First of all, you need to download the resource agent to your system:

<pre>
# cd /usr/lib/ocf/resource.d/openstack
# wget https://raw.github.com/madkiss/openstack-resource-agents/master/ocf/neutron-metadata-agent
# chmod a+rx neutron-metadata-agent
</pre>

You may now proceed with adding the Pacemaker configuration for neutron metadata agent resource. Connect to the Pacemaker cluster with crm configure, and add the following cluster resources:

Execute

<pre>
crm configure
</pre>

Then execute following command

<pre>
primitive p_neutron-metadata-agent ocf:openstack:neutron-metadata-agent params config="/etc/neutron/neutron.conf" agent_config="/etc/neutron/metadata_agent.ini" op monitor interval="30s" timeout="30s"
</pre>

commit the changes.

<pre>
commit
</pre>

####Manage network resources

You can now add the Pacemaker configuration for managing all network resources together with a group. Connect to the Pacemaker cluster with crm configure, and add the following cluster resources:

Execute

<pre>
crm configure
</pre>

Then execute following command

<pre>
group g_services_network p_neutron-l3-agent p_neutron-dhcp-agent p_neutron-metadata_agent
</pre>

commit the changes.

<pre>
commit
</pre>

**Refer:** http://docs.openstack.org/high-availability-guide/content/ch-pacemaker.html
