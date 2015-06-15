Description
===========
Installs Codership's MySQL Galera cluster (http://http://www.codership.com/).
Galera Cluster provides synchronous multi-master replication for MySQL (replication plugin).

* No master failover scripting (automatic failover and recovery)
* No slave lag
* Read and write to any node
* Write scalabilty
* WAN Clustering

This cookbook enables you to install a Galera cluster from scratch. At minimum you would probaly only need to change a few attributes like

* ['mysql']['root_password'] = "password"
* ['mysql']['tunable']['buffer_pool_size'] = "256M"

You can also deploy our ClusterControl coookbook with the Galera Cluster which provide additional control and monitoring features.

Requirements
============

Platform
--------
* Debian, Ubuntu
* CentOS, Red Hat, Fedora

Tested on:

* Ubuntu 12.04 w/ Chef-server 10.16.2 and Galera Cluster v2.2
* Ubuntu 11.10/12.04 w/ Chef-solo 0.10.8/0.10.10 and Galera Cluster v2.1

Attributes
==========

* node['mysql']['install_dir'] = "/usr/local"
* node['mysql']['root_password'] = "password"

* node['mysql']['base_dir'] = "/usr/local"
* node['mysql']['data_dir'] = "/var/lib/mysql"
* node['mysql']['run_dir']  = "/var/run/mysqld"
* node['mysql']['pid_file'] = /var/lib/mysql/mysqld.pid"
* node['mysql']['socket']  = /var/run/mysqld/mysqld.sock"
* node['mysql']['port']    = 3306
* node['mysql']['tmp_dir']  = "/tmp"

* node['mysql']['tunable']['buffer_pool_size'] = "256M"
* node['mysql']['tunable']['flush_log_at_trx_commit'] = 2
* node['mysql']['tunable']['file_per_table'] = 1
* node['mysql']['tunable']['doublewrite'] = 0
* node['mysql']['tunable']['log_file_size'] = "512M"
* node['mysql']['tunable']['log_files_in_group'] = 2
* node['mysql']['tunable']['buffer_pool_instances'] = 1
* node['mysql']['tunable']['max_dirty_pages_pct'] = 75
* node['mysql']['tunable']['thread_concurrency'] = 0
* node['mysql']['tunable']['concurrency_tickets'] = 5000
* node['mysql']['tunable']['thread_sleep_delay'] = 10000
* node['mysql']['tunable']['lock_wait_timeout'] = 50
* node['mysql']['tunable']['io_capacity'] = 200
* node['mysql']['tunable']['read_io_threads'] = 4
* node['mysql']['tunable']['write_io_threads'] = 4

* node['mysql']['tunable']['file_format'] = "barracuda"
* node['mysql']['tunable']['flush_method'] = "O_DIRECT"

* node['wsrep']['cluster_name'] = "my_galera_cluster"
* node['wsrep']['slave_threads'] = 1
* node['wsrep']['certify_nonPK'] = 1
* node['wsrep']['max_ws_rows'] = 131072
* node['wsrep']['max_ws_size'] = 1073741824
* node['wsrep']['retry_autocommit'] = 1

and more in attributes/default.rb

Usage
=====

On MySQL Galera Nodes,

		include_recipe "galera:server"

Example cc_galera role:

		name "cc_galera"
		description "MySQL Galera Node"
		run_list "recipe[galera::server]"

