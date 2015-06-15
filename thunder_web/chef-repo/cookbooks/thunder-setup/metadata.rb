name             'thunder-setup'
maintainer       'Aqorn'
maintainer_email 'gvarghese@aqorn.com'
license          'All rights reserved'
description      'Installs/Configures thunder-setup'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.2.0'

depends "database", "= 2.3.0"
depends "mysql", "= 5.6.1"
depends "openstack-identity"
depends "openstack-image"
depends "openstack-compute"
depends "openstack-network"
depends "openstack-block-storage"
depends "openstack-object-storage"
depends "openstack-dashboard"
depends "parted"