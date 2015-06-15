SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
`id` int(11) NOT NULL,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
`id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
`id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add server error', 7, 'add_servererror'),
(20, 'Can change server error', 7, 'change_servererror'),
(21, 'Can delete server error', 7, 'delete_servererror'),
(22, 'Can add cloud', 8, 'add_cloud'),
(23, 'Can change cloud', 8, 'change_cloud'),
(24, 'Can delete cloud', 8, 'delete_cloud'),
(25, 'Can add nodelist', 9, 'add_nodelist'),
(26, 'Can change nodelist', 9, 'change_nodelist'),
(27, 'Can delete nodelist', 9, 'delete_nodelist'),
(28, 'Can add nodelog', 10, 'add_nodelog'),
(29, 'Can change nodelog', 10, 'change_nodelog'),
(30, 'Can delete nodelog', 10, 'delete_nodelog'),
(31, 'Can add job', 11, 'add_job'),
(32, 'Can change job', 11, 'change_job'),
(33, 'Can delete job', 11, 'delete_job'),
(34, 'Can add roletype', 12, 'add_roletype'),
(35, 'Can change roletype', 12, 'change_roletype'),
(36, 'Can delete roletype', 12, 'delete_roletype'),
(37, 'Can add cloud specification', 13, 'add_cloudspecification'),
(38, 'Can change cloud specification', 13, 'change_cloudspecification'),
(39, 'Can delete cloud specification', 13, 'delete_cloudspecification'),
(40, 'Can add cloud spec value', 14, 'add_cloudspecvalue'),
(41, 'Can change cloud spec value', 14, 'change_cloudspecvalue'),
(42, 'Can delete cloud spec value', 14, 'delete_cloudspecvalue'),
(43, 'Can add recipe', 15, 'add_recipe'),
(44, 'Can change recipe', 15, 'change_recipe'),
(45, 'Can delete recipe', 15, 'delete_recipe'),
(46, 'Can add node spec', 16, 'add_nodespec'),
(47, 'Can change node spec', 16, 'change_nodespec'),
(48, 'Can delete node spec', 16, 'delete_nodespec'),
(49, 'Can add node role', 17, 'add_noderole'),
(50, 'Can change node role', 17, 'change_noderole'),
(51, 'Can delete node role', 17, 'delete_noderole'),
(52, 'Can add scope', 18, 'add_scope'),
(53, 'Can change scope', 18, 'change_scope'),
(54, 'Can delete scope', 18, 'delete_scope'),
(55, 'Can add domain', 19, 'add_domain'),
(56, 'Can change domain', 19, 'change_domain'),
(57, 'Can delete domain', 19, 'delete_domain'),
(58, 'Can add user role type', 20, 'add_userroletype'),
(59, 'Can change user role type', 20, 'change_userroletype'),
(60, 'Can delete user role type', 20, 'delete_userroletype'),
(61, 'Can add permission', 21, 'add_permission'),
(62, 'Can change permission', 21, 'change_permission'),
(63, 'Can delete permission', 21, 'delete_permission'),
(64, 'Can add user role', 22, 'add_userrole'),
(65, 'Can change user role', 22, 'change_userrole'),
(66, 'Can delete user role', 22, 'delete_userrole'),
(67, 'Can add log', 23, 'add_log'),
(68, 'Can change log', 23, 'change_log'),
(69, 'Can delete log', 23, 'delete_log'),
(70, 'Can add manage addons', 24, 'add_manageaddons'),
(71, 'Can change manage addons', 24, 'change_manageaddons'),
(72, 'Can delete manage addons', 24, 'delete_manageaddons'),
(73, 'Can add data bag item', 25, 'add_databagitem'),
(74, 'Can change data bag item', 25, 'change_databagitem'),
(75, 'Can delete data bag item', 25, 'delete_databagitem'),
(76, 'Can add data bag', 26, 'add_databag'),
(77, 'Can change data bag', 26, 'change_databag'),
(78, 'Can delete data bag', 26, 'delete_databag'),
(79, 'Can add cloud domain', 27, 'add_clouddomain'),
(80, 'Can change cloud domain', 27, 'change_clouddomain'),
(81, 'Can delete cloud domain', 27, 'delete_clouddomain'),
(82, 'Can add cloud domain map', 28, 'add_clouddomainmap'),
(83, 'Can change cloud domain map', 28, 'change_clouddomainmap'),
(84, 'Can delete cloud domain map', 28, 'delete_clouddomainmap'),
(85, 'Can add domain role permission', 29, 'add_domainrolepermission'),
(86, 'Can change domain role permission', 29, 'change_domainrolepermission'),
(87, 'Can delete domain role permission', 29, 'delete_domainrolepermission'),
(88, 'Can add domain role', 30, 'add_domainrole'),
(89, 'Can change domain role', 30, 'change_domainrole'),
(90, 'Can delete domain role', 30, 'delete_domainrole'),
(91, 'Can add user role map', 31, 'add_userrolemap'),
(92, 'Can change user role map', 31, 'change_userrolemap'),
(93, 'Can delete user role map', 31, 'delete_userrolemap'),
(94, 'Can add thunder option', 32, 'add_thunderoption'),
(95, 'Can change thunder option', 32, 'change_thunderoption'),
(96, 'Can delete thunder option', 32, 'delete_thunderoption'),
(97, 'Can add thunder option value', 33, 'add_thunderoptionvalue'),
(98, 'Can change thunder option value', 33, 'change_thunderoptionvalue'),
(99, 'Can delete thunder option value', 33, 'delete_thunderoptionvalue'),
(100, 'Can add alert', 34, 'add_alert'),
(101, 'Can change alert', 34, 'change_alert'),
(102, 'Can delete alert', 34, 'delete_alert'),
(103, 'Can add patch update', 35, 'add_patchupdate'),
(104, 'Can change patch update', 35, 'change_patchupdate'),
(105, 'Can delete patch update', 35, 'delete_patchupdate'),
(106, 'Can add upgrade log', 36, 'add_upgradelog'),
(107, 'Can change upgrade log', 36, 'change_upgradelog'),
(108, 'Can delete upgrade log', 36, 'delete_upgradelog'),
(109, 'Can add network interface', 37, 'add_networkinterface'),
(110, 'Can change network interface', 37, 'change_networkinterface'),
(111, 'Can delete network interface', 37, 'delete_networkinterface'),
(112, 'Can add network interface mapping', 38, 'add_networkinterfacemapping'),
(113, 'Can change network interface mapping', 38, 'change_networkinterfacemapping'),
(114, 'Can delete network interface mapping', 38, 'delete_networkinterfacemapping'),
(115, 'Can add disk drive', 39, 'add_diskdrive'),
(116, 'Can change disk drive', 39, 'change_diskdrive'),
(117, 'Can delete disk drive', 39, 'delete_diskdrive'),
(118, 'Can add monitor service', 40, 'add_monitorservice'),
(119, 'Can change monitor service', 40, 'change_monitorservice'),
(120, 'Can delete monitor service', 40, 'delete_monitorservice'),
(121, 'Can add task', 41, 'add_task'),
(122, 'Can change task', 41, 'change_task'),
(123, 'Can delete task', 41, 'delete_task'),
(124, 'Can add network details', 42, 'add_networkdetails'),
(125, 'Can change network details', 42, 'change_networkdetails'),
(126, 'Can delete network details', 42, 'delete_networkdetails'),
(127, 'Can add floating network', 43, 'add_floatingnetwork'),
(128, 'Can change floating network', 43, 'change_floatingnetwork'),
(129, 'Can delete floating network', 43, 'delete_floatingnetwork'),
(130, 'Can add public network', 44, 'add_publicnetwork'),
(131, 'Can change public network', 44, 'change_publicnetwork'),
(132, 'Can delete public network', 44, 'delete_publicnetwork'),
(133, 'Can add dns server', 45, 'add_dnsserver'),
(134, 'Can change dns server', 45, 'change_dnsserver'),
(135, 'Can delete dns server', 45, 'delete_dnsserver'),
(136, 'Can add private network', 46, 'add_privatenetwork'),
(137, 'Can change private network', 46, 'change_privatenetwork'),
(138, 'Can delete private network', 46, 'delete_privatenetwork'),
(139, 'Can add network card', 47, 'add_networkcard'),
(140, 'Can change network card', 47, 'change_networkcard'),
(141, 'Can delete network card', 47, 'delete_networkcard'),
(142, 'Can add pxe network', 48, 'add_pxenetwork'),
(143, 'Can change pxe network', 48, 'change_pxenetwork'),
(144, 'Can delete pxe network', 48, 'delete_pxenetwork'),
(145, 'Can add thunder acces', 49, 'add_thunderacces'),
(146, 'Can change thunder acces', 49, 'change_thunderacces'),
(147, 'Can delete thunder acces', 49, 'delete_thunderacces'),
(148, 'Can add installation status', 50, 'add_installationstatus'),
(149, 'Can change installation status', 50, 'change_installationstatus'),
(150, 'Can delete installation status', 50, 'delete_installationstatus');

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
`id` int(11) NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(75) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$12000$wY8QM10V6CU7$CZ/9TuqqI0KNRjeGyUBt6j1uI2RAhGlpkSIk2v4b5gE=', '2015-06-12 15:37:04', 1, 'admin', '', '', '', 1, 1, '2015-06-12 15:37:04');

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
`id` int(11) NOT NULL,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
`id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'log entry', 'admin', 'logentry'),
(2, 'permission', 'auth', 'permission'),
(3, 'group', 'auth', 'group'),
(4, 'user', 'auth', 'user'),
(5, 'content type', 'contenttypes', 'contenttype'),
(6, 'session', 'sessions', 'session'),
(7, 'server error', 'shoogie', 'servererror'),
(8, 'cloud', 'cloud', 'cloud'),
(9, 'nodelist', 'cloud', 'nodelist'),
(10, 'nodelog', 'cloud', 'nodelog'),
(11, 'job', 'cloud', 'job'),
(12, 'roletype', 'cloud', 'roletype'),
(13, 'cloud specification', 'cloud', 'cloudspecification'),
(14, 'cloud spec value', 'cloud', 'cloudspecvalue'),
(15, 'recipe', 'cloud', 'recipe'),
(16, 'node spec', 'cloud', 'nodespec'),
(17, 'node role', 'cloud', 'noderole'),
(18, 'scope', 'cloud', 'scope'),
(19, 'domain', 'cloud', 'domain'),
(20, 'user role type', 'cloud', 'userroletype'),
(21, 'permission', 'cloud', 'permission'),
(22, 'user role', 'cloud', 'userrole'),
(23, 'log', 'cloud', 'log'),
(24, 'manage addons', 'cloud', 'manageaddons'),
(25, 'data bag item', 'cloud', 'databagitem'),
(26, 'data bag', 'cloud', 'databag'),
(27, 'cloud domain', 'cloud', 'clouddomain'),
(28, 'cloud domain map', 'cloud', 'clouddomainmap'),
(29, 'domain role permission', 'cloud', 'domainrolepermission'),
(30, 'domain role', 'cloud', 'domainrole'),
(31, 'user role map', 'cloud', 'userrolemap'),
(32, 'thunder option', 'cloud', 'thunderoption'),
(33, 'thunder option value', 'cloud', 'thunderoptionvalue'),
(34, 'alert', 'cloud', 'alert'),
(35, 'patch update', 'cloud', 'patchupdate'),
(36, 'upgrade log', 'cloud', 'upgradelog'),
(37, 'network interface', 'cloud', 'networkinterface'),
(38, 'network interface mapping', 'cloud', 'networkinterfacemapping'),
(39, 'disk drive', 'cloud', 'diskdrive'),
(40, 'monitor service', 'cloud', 'monitorservice'),
(41, 'task', 'task', 'task'),
(42, 'network details', 'network', 'networkdetails'),
(43, 'floating network', 'network', 'floatingnetwork'),
(44, 'public network', 'network', 'publicnetwork'),
(45, 'dns server', 'network', 'dnsserver'),
(46, 'private network', 'network', 'privatenetwork'),
(47, 'network card', 'thunderadmin', 'networkcard'),
(48, 'pxe network', 'thunderadmin', 'pxenetwork'),
(49, 'thunder acces', 'thunderadmin', 'thunderacces'),
(50, 'installation status', 'thunderadmin', 'installationstatus');

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `install_installation_status`;
CREATE TABLE IF NOT EXISTS `install_installation_status` (
`id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL,
  `progress` int(11) NOT NULL,
  `state` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `reason` varchar(500) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `install_installation_status` (`id`, `name`, `status`, `progress`, `state`, `reason`) VALUES
(1, 'Configure PXE Network', 0, 0, '', ''),
(2, 'Configure IP Address', 0, 0, '', ''),
(3, 'Installation Status', 0, 0, '', '');

DROP TABLE IF EXISTS `install_network_card`;
CREATE TABLE IF NOT EXISTS `install_network_card` (
`id` int(11) NOT NULL,
  `name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `mac_address` varchar(60) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `install_pxe_network`;
CREATE TABLE IF NOT EXISTS `install_pxe_network` (
`id` int(11) NOT NULL,
  `nic_id` int(11) NOT NULL,
  `pool_start` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `pool_end` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `subnet_mask` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `gateway` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `subnet` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` char(15) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `install_thunder_access`;
CREATE TABLE IF NOT EXISTS `install_thunder_access` (
`id` int(11) NOT NULL,
  `nic_id` int(11) NOT NULL,
  `ip_address` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `subnet_mask` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `gateway` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `dns_ip` char(15) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `shoogie_servererror`;
CREATE TABLE IF NOT EXISTS `shoogie_servererror` (
`id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `hostname` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `request_method` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `request_path` varchar(1024) COLLATE utf8_unicode_ci NOT NULL,
  `query_string` longtext COLLATE utf8_unicode_ci NOT NULL,
  `post_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `cookie_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `session_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `exception_type` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `exception_str` longtext COLLATE utf8_unicode_ci NOT NULL,
  `source_file` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `source_line_num` int(11) NOT NULL,
  `source_function` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `source_text` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `technical_response` longtext COLLATE utf8_unicode_ci NOT NULL,
  `issue` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `resolved` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_alert`;
CREATE TABLE IF NOT EXISTS `thunder_alert` (
`id` int(11) NOT NULL,
  `alert_type` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `referece_id` int(11) NOT NULL,
  `alert_content` longtext COLLATE utf8_unicode_ci NOT NULL,
  `visited` tinyint(1) NOT NULL,
  `updated_time` datetime NOT NULL,
  `alert_status` varchar(1) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_cloud`;
CREATE TABLE IF NOT EXISTS `thunder_cloud` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cloud_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `created_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_cloud_databag`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_databag` (
`id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `databag_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_cloud_databag_item`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_databag_item` (
`id` int(11) NOT NULL,
  `databag_category` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `item_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `item_column` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `default_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `thunder_cloud_databag_item` (`id`, `databag_category`, `item_name`, `item_column`, `default_value`) VALUES
(1, 'db_passwords', 'nova', 'nova', 'ThunDer'),
(2, 'db_passwords', 'horizon', 'horizon', 'ThunDer'),
(3, 'db_passwords', 'keystone', 'keystone', 'ThunDer'),
(4, 'db_passwords', 'glance', 'glance', 'ThunDer'),
(5, 'db_passwords', 'neutron', 'neutron', 'ThunDer'),
(6, 'db_passwords', 'dash', 'dash', 'ThunDer'),
(7, 'db_passwords', 'cinder', 'cinder', 'ThunDer'),
(8, 'service_passwords', 'openstack image', 'openstack-image', 'ThunDer'),
(9, 'service_passwords', 'openstack compute', 'openstack-compute', 'ThunDer'),
(10, 'service_passwords', 'openstack network', 'openstack-network', 'ThunDer'),
(11, 'service_passwords', 'openstack block storage', 'openstack-block-storage', 'ThunDer'),
(12, 'secrets', 'openstack identity bootstrap token', 'openstack_identity_bootstrap_token', 'ThunDer'),
(13, 'secrets', 'neutron metadata secret', 'neutron_metadata_secret', 'ThunDer'),
(14, 'service_passwords', 'openstack object storage', 'openstack-object-storage', 'ThunDer'),
(15, 'secrets', 'swift hash path prefix', 'swift_hash_path_prefix', 'ThunDer'),
(16, 'secrets', 'swift hash path suffix', 'swift_hash_path_suffix', 'ThunDer'),
(17, 'secrets', 'dispersion auth user', 'dispersion_auth_user', 'ThunDer'),
(18, 'secrets', 'dispersion auth key', 'dispersion_auth_key', 'ThunDer'),
(19, 'secrets', 'swift authkey', 'swift_authkey', 'ThunDer'),
(20, 'user_passwords', 'guest(Messaging Server)', 'guest', 'guest');

DROP TABLE IF EXISTS `thunder_cloud_domain`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_domain` (
`id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_cloud_domain` (`id`, `name`, `status`) VALUES
(1, 'Everything', 1);

DROP TABLE IF EXISTS `thunder_cloud_domain_map`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_domain_map` (
`id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `thunder_cloud_specification`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_specification` (
`id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `spec_category` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `spec_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `spec_column` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `default_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `thunder_cloud_specification` (`id`, `role_id`, `spec_category`, `spec_name`, `spec_column`, `default_value`) VALUES
(1, 1, 'keystone', 'Openstack Endpoint Host', 'openstack::endpoints::host', 'controller'),
(2, 1, 'messaging_server', 'Messaging Server Endpoint Host', 'openstack::endpoints::mq::host', 'controller'),
(3, 1, 'database', 'Database Server Endpoint Host', 'openstack::endpoints::db::host', 'loadbalancer'),
(4, 1, 'compute', 'Network Service Type', 'openstack::compute::network::service_type', 'neutron'),
(5, 1, 'cinder', 'The Default Store of Image', 'openstack::image::api::default_store', 'file'),
(6, 1, 'Neutron', 'Nova Metadata API Service IP', 'openstack::network::metadata::nova_metadata_ip', 'controller'),
(7, 1, 'Neutron', 'Type of Network to Allocate for Tenant Networks', 'openstack::network::openvswitch::tenant_network_type', 'gre'),
(8, 1, 'Neutron', 'Interface to use for external bridge', 'openstack::network::l3::external_network_bridge_interface', 'eth1'),
(9, 1, 'common', 'Set to True in the Server and the Agents to Enable Support for GRE', 'openstack::network::openvswitch::enable_tunneling', 'True'),
(10, 1, 'Neutron', 'The Type of Tunnel Network', 'openstack::network::openvswitch::tunnel_type', 'gre'),
(11, 3, 'cinder', 'Volume Driver', 'openstack::block-storage::volume::driver', 'cinder.volume.drivers.lvm.LVMISCSIDriver'),
(12, 1, 'dashborad', 'The hostname of dashbaord to add in apache conf. If not give we can access it through default IP of controller', 'openstack::dashboard::server_hostname', 'nil'),
(13, 3, 'cinder', 'Block Device Disk Name', 'openstack::block-storage::volume::block_devices', '/dev/sdb1'),
(14, 4, 'swift', 'Git Repository Creation Server IP', 'openstack::object-storage::git_builder_ip', 'controller'),
(15, 1, 'database', 'Mysql Root Password', 'mysql::server_root_password', 'ThunDer'),
(16, 1, 'messaging_server', 'Messaging Server Type', 'openstack::mq::service_type', 'rabbitmq');

DROP TABLE IF EXISTS `thunder_cloud_spec_values`;
CREATE TABLE IF NOT EXISTS `thunder_cloud_spec_values` (
`id` int(11) NOT NULL,
  `spec_id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `spec_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_disk_drive`;
CREATE TABLE IF NOT EXISTS `thunder_disk_drive` (
`id` int(11) NOT NULL,
  `nodelist_id` int(11) NOT NULL,
  `name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `system_space` decimal(19,1) NOT NULL,
  `storage_space` decimal(19,1) NOT NULL,
  `total_space` decimal(19,1) NOT NULL,
  `format` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_dns_server`;
CREATE TABLE IF NOT EXISTS `thunder_dns_server` (
`id` int(11) NOT NULL,
  `thunder_network_details_id` int(11) NOT NULL,
  `dns_server` char(15) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_domain`;
CREATE TABLE IF NOT EXISTS `thunder_domain` (
`id` int(11) NOT NULL,
  `domain_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `scope_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_domain_role`;
CREATE TABLE IF NOT EXISTS `thunder_domain_role` (
`id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_domain_role` (`id`, `name`, `domain_id`, `permission_id`) VALUES
(1, 'ThunderAdmin', 1, 1),
(2, 'CloudAdmin', 1, 2),
(3, 'Engineer', 1, 3),
(4, 'User', 1, 4);

DROP TABLE IF EXISTS `thunder_domain_role_permission`;
CREATE TABLE IF NOT EXISTS `thunder_domain_role_permission` (
`id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` varchar(200) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_domain_role_permission` (`id`, `name`, `description`) VALUES
(1, 'ThunderAdmin', 'Individual Cloud or Thunder ( all clouds)'),
(2, 'CloudAdmin', 'View, change configurations or deploy'),
(3, 'Engineer', 'View or change cloud configurations'),
(4, 'User', 'View cloud configurations only');

DROP TABLE IF EXISTS `thunder_floatingip_network`;
CREATE TABLE IF NOT EXISTS `thunder_floatingip_network` (
`id` int(11) NOT NULL,
  `thunder_network_details_id` int(11) NOT NULL,
  `ip_range_from` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `ip_range_to` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `ip_cidr` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `use_vlan` tinyint(1) NOT NULL,
  `vlan_tag` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_job`;
CREATE TABLE IF NOT EXISTS `thunder_job` (
`id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `job_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `updated_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `job_status` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `job_priority` int(11) NOT NULL,
  `job_progress` int(11) NOT NULL,
  `visited` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_log`;
CREATE TABLE IF NOT EXISTS `thunder_log` (
`id` int(11) NOT NULL,
  `level` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `timedata` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_manage_addons`;
CREATE TABLE IF NOT EXISTS `thunder_manage_addons` (
`id` int(11) NOT NULL,
  `addon_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `timedata` datetime DEFAULT NULL,
  `filepath` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_monitor_service`;
CREATE TABLE IF NOT EXISTS `thunder_monitor_service` (
`id` int(11) NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `command` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `thunder_monitor_service` (`id`, `name`, `command`, `status`) VALUES
(1, 'cobbler', '/etc/init.d/cobbler status', 1),
(2, 'chef-server', 'chef-server-ctl status', 1);

DROP TABLE IF EXISTS `thunder_network_details`;
CREATE TABLE IF NOT EXISTS `thunder_network_details` (
`id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `public_cidr` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `public_use_vlan` tinyint(1) NOT NULL,
  `public_vlan` int(11) DEFAULT NULL,
  `in_network_cidr` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `in_use_vlan` tinyint(1) NOT NULL,
  `in_vlan` int(11) DEFAULT NULL,
  `st_network_cidr` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `st_use_vlan` tinyint(1) NOT NULL,
  `st_vlan` int(11) DEFAULT NULL,
  `gre_tunnel_from` int(11) NOT NULL,
  `gre_tunnel_to` int(11) NOT NULL,
  `update_date` datetime DEFAULT NULL,
  `last_verified` datetime DEFAULT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_network_interface`;
CREATE TABLE IF NOT EXISTS `thunder_network_interface` (
`id` int(11) NOT NULL,
  `nodelist_id` int(11) NOT NULL,
  `name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `mac_address` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `model_name` varchar(120) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_nic_mapping`;
CREATE TABLE IF NOT EXISTS `thunder_nic_mapping` (
`id` int(11) NOT NULL,
  `nic_id` int(11) NOT NULL,
  `network_type` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `ip_address` char(39) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_nodelist`;
CREATE TABLE IF NOT EXISTS `thunder_nodelist` (
`id` int(11) NOT NULL,
  `cloud_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `node_ip` char(39) COLLATE utf8_unicode_ci NOT NULL,
  `host_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `user_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `sudo_password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL,
  `prepared` tinyint(1) NOT NULL,
  `preos` tinyint(1) NOT NULL,
  `currentos` tinyint(1) NOT NULL,
  `node_up` tinyint(1) NOT NULL,
  `zabbix_host_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_nodelog`;
CREATE TABLE IF NOT EXISTS `thunder_nodelog` (
`id` int(11) NOT NULL,
  `node_listid` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `log_type` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  `log_title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `log_details` longtext COLLATE utf8_unicode_ci NOT NULL,
  `updated_time` datetime NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_noderole`;
CREATE TABLE IF NOT EXISTS `thunder_noderole` (
`id` int(11) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `node_id` int(11) NOT NULL,
  `assigned` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_nodespec`;
CREATE TABLE IF NOT EXISTS `thunder_nodespec` (
`id` int(11) NOT NULL,
  `nodelist_id` int(11) NOT NULL,
  `core` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ram` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `hdd` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `mac_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_option`;
CREATE TABLE IF NOT EXISTS `thunder_option` (
`id` int(11) NOT NULL,
  `option_category` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `option_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `option_column` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `default_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `option_type` varchar(120) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `thunder_option` (`id`, `option_category`, `option_name`, `option_column`, `default_value`, `option_type`) VALUES
(1, 'openstack_admin_details', 'Default Username', 'defaultusername', 'admin', 'textbox'),
(2, 'openstack_admin_details', 'Default Password', 'Default_Password', 'ThunDer', 'textbox'),
(3, 'openstack_admin_details', 'Default Tenant', 'Default_Tenant', 'admin', 'textbox'),
(4, 'openstack_admin_details', 'Default Email', 'defaultemail', '', 'textbox'),
(5, 'shared', 'Auto start guests when host boots', 'Auto_start_guests_when_host_boots', '', 'checkbox'),
(6, 'shared', 'Use RAW images for guests instead of QCOW', 'Use_RAW_images_for_guests_instead_of_QCOW', '', 'checkbox'),
(7, 'shared', 'Enable Auto-Evacuation of Guests (requires guests boot from volume).', 'Enable_auto_evacuation', '', 'checkbox');

DROP TABLE IF EXISTS `thunder_option_value`;
CREATE TABLE IF NOT EXISTS `thunder_option_value` (
`id` int(11) NOT NULL,
  `cloud_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  `option_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_patch_updates`;
CREATE TABLE IF NOT EXISTS `thunder_patch_updates` (
`id` int(11) NOT NULL,
  `version` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `intsalled_on` datetime NOT NULL,
  `rollbacked_on` datetime DEFAULT NULL,
  `rollbacked_status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_permission`;
CREATE TABLE IF NOT EXISTS `thunder_permission` (
`id` int(11) NOT NULL,
  `permission_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_private_network`;
CREATE TABLE IF NOT EXISTS `thunder_private_network` (
`id` int(11) NOT NULL,
  `thunder_network_details_id` int(11) NOT NULL,
  `network_cidr` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_public_network`;
CREATE TABLE IF NOT EXISTS `thunder_public_network` (
`id` int(11) NOT NULL,
  `thunder_network_details_id` int(11) NOT NULL,
  `ip_range_from` char(15) COLLATE utf8_unicode_ci NOT NULL,
  `ip_range_to` char(15) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_recipe`;
CREATE TABLE IF NOT EXISTS `thunder_recipe` (
`id` int(11) NOT NULL,
  `roletype_id` int(11) NOT NULL,
  `recipe_name` varchar(255) NOT NULL,
  `priority` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_recipe` (`id`, `roletype_id`, `recipe_name`, `priority`, `status`) VALUES
(1, 1, 'openstack-identity::server', 1, 1),
(2, 1, 'openstack-identity::client', 1, 1),
(3, 1, 'openstack-identity::registration', 1, 1),
(4, 1, 'openstack-image::api', 2, 1),
(5, 1, 'openstack-image::registry', 2, 1),
(6, 1, 'openstack-image::identity_registration', 2, 1),
(7, 1, 'openstack-image::image_upload', 2, 1),
(8, 1, 'openstack-compute::nova-setup', 3, 1),
(9, 1, 'openstack-compute::api-os-compute', 3, 1),
(10, 1, 'openstack-compute::conductor', 3, 1),
(11, 1, 'openstack-compute::client', 3, 1),
(12, 1, 'openstack-compute::identity_registration', 3, 1),
(13, 1, 'openstack-compute::nova-cert', 3, 1),
(14, 1, 'openstack-compute::scheduler', 3, 1),
(15, 1, 'openstack-compute::vncproxy', 3, 1),
(16, 1, 'openstack-network::server', 4, 1),
(17, 1, 'openstack-network::client', 4, 1),
(18, 1, 'openstack-network::dhcp_agent', 4, 1),
(19, 1, 'openstack-network::metadata_agent', 4, 1),
(21, 1, 'openstack-network::identity_registration', 4, 1),
(22, 1, 'openstack-network::openvswitch', 5, 1),
(23, 1, 'openstack-network::l3_agent', 5, 1),
(24, 1, 'openstack-dashboard::server', 6, 1),
(25, 2, 'openstack-compute::compute', 1, 1),
(26, 3, 'openstack-block-storage::volume', 1, 1),
(27, 1, 'openstack-block-storage::api', 7, 1),
(28, 1, 'openstack-block-storage::client', 7, 1),
(29, 1, 'openstack-block-storage::scheduler', 7, 1),
(30, 1, 'openstack-block-storage::identity_registration', 7, 1),
(31, 1, 'recipe[openstack-object-storage::setup],recipe[openstack-object-storage::management-server],recipe[openstack-object-storage::proxy-server]', 8, 1),
(32, 4, 'role[os-object-storage-account],role[os-object-storage-container],role[os-object-storage-object]', 2, 1),
(33, 1, 'thunder-setup::setup_network', 9, 1),
(34, 4, 'thunder-setup::object_storage_setup', 1, 1);

DROP TABLE IF EXISTS `thunder_roletype`;
CREATE TABLE IF NOT EXISTS `thunder_roletype` (
`id` int(11) NOT NULL,
  `role_typename` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `role_code` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `role_details` longtext COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `thunder_roletype` (`id`, `role_typename`, `role_code`, `role_details`, `status`) VALUES
(1, 'Controller', 'controller', 'This role handles all shared services including keystone, cinder api, neutron, swift proxies etc', 1),
(2, 'Compute', 'compute', 'This role manages guests on KVM or QEMU', 1),
(3, 'Block Storage', 'block_storage', 'The role assigns block storage to the node', 1),
(4, 'Object Storage(Swift or Ceph)', 'object_storage', 'This role assigns swift storage or Ceph OSD (As defined in cloud setup)', 1);

DROP TABLE IF EXISTS `thunder_scope`;
CREATE TABLE IF NOT EXISTS `thunder_scope` (
`id` int(11) NOT NULL,
  `scope_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_task`;
CREATE TABLE IF NOT EXISTS `thunder_task` (
`id` int(11) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_update_logs`;
CREATE TABLE IF NOT EXISTS `thunder_update_logs` (
`id` int(11) NOT NULL,
  `version` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `log_details` longtext COLLATE utf8_unicode_ci NOT NULL,
  `updated_on` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_userrole`;
CREATE TABLE IF NOT EXISTS `thunder_userrole` (
`id` int(11) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_userrole_type`;
CREATE TABLE IF NOT EXISTS `thunder_userrole_type` (
`id` int(11) NOT NULL,
  `role_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `thunder_user_role_mapping`;
CREATE TABLE IF NOT EXISTS `thunder_user_role_mapping` (
`id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_user_role_mapping` (`id`, `role_id`, `user_id`) VALUES
(1, 1, 1);


ALTER TABLE `auth_group`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `auth_group_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `group_id` (`group_id`,`permission_id`), ADD KEY `auth_group_permissions_5f412f9a` (`group_id`), ADD KEY `auth_group_permissions_83d7f98b` (`permission_id`);

ALTER TABLE `auth_permission`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `content_type_id` (`content_type_id`,`codename`), ADD KEY `auth_permission_37ef4eb4` (`content_type_id`);

ALTER TABLE `auth_user`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

ALTER TABLE `auth_user_groups`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`group_id`), ADD KEY `auth_user_groups_6340c63c` (`user_id`), ADD KEY `auth_user_groups_5f412f9a` (`group_id`);

ALTER TABLE `auth_user_user_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`permission_id`), ADD KEY `auth_user_user_permissions_6340c63c` (`user_id`), ADD KEY `auth_user_user_permissions_83d7f98b` (`permission_id`);

ALTER TABLE `django_admin_log`
 ADD PRIMARY KEY (`id`), ADD KEY `django_admin_log_6340c63c` (`user_id`), ADD KEY `django_admin_log_37ef4eb4` (`content_type_id`);

ALTER TABLE `django_content_type`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `app_label` (`app_label`,`model`);

ALTER TABLE `django_session`
 ADD PRIMARY KEY (`session_key`), ADD KEY `django_session_b7b81f0c` (`expire_date`);

ALTER TABLE `install_installation_status`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `install_network_card`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `install_pxe_network`
 ADD PRIMARY KEY (`id`), ADD KEY `install_pxe_network_c17b074a` (`nic_id`);

ALTER TABLE `install_thunder_access`
 ADD PRIMARY KEY (`id`), ADD KEY `install_thunder_access_c17b074a` (`nic_id`);

ALTER TABLE `shoogie_servererror`
 ADD PRIMARY KEY (`id`), ADD KEY `shoogie_servererror_6340c63c` (`user_id`);

ALTER TABLE `thunder_alert`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_cloud`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_cloud_6340c63c` (`user_id`);

ALTER TABLE `thunder_cloud_databag`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_cloud_databag_78e320f1` (`cloud_id`), ADD KEY `thunder_cloud_databag_0a47aae8` (`item_id`);

ALTER TABLE `thunder_cloud_databag_item`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_cloud_domain`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_cloud_domain_map`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_cloud_domain_map_abc7588b` (`cloud_id`), ADD KEY `thunder_cloud_domain_map_662cbf12` (`domain_id`);

ALTER TABLE `thunder_cloud_specification`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_cloud_specification_278213e1` (`role_id`);

ALTER TABLE `thunder_cloud_spec_values`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_cloud_spec_values_421877ba` (`spec_id`), ADD KEY `thunder_cloud_spec_values_78e320f1` (`cloud_id`);

ALTER TABLE `thunder_disk_drive`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_disk_drive_d1a78974` (`nodelist_id`);

ALTER TABLE `thunder_dns_server`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_dns_server_0048ef3e` (`thunder_network_details_id`);

ALTER TABLE `thunder_domain`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_domain_1224d57b` (`scope_id`);

ALTER TABLE `thunder_domain_role`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_domain_role_662cbf12` (`domain_id`), ADD KEY `thunder_domain_role_8373b171` (`permission_id`);

ALTER TABLE `thunder_domain_role_permission`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_floatingip_network`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_floatingip_network_0048ef3e` (`thunder_network_details_id`);

ALTER TABLE `thunder_job`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_job_78e320f1` (`cloud_id`);

ALTER TABLE `thunder_log`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_manage_addons`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_monitor_service`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_network_details`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_network_details_78e320f1` (`cloud_id`);

ALTER TABLE `thunder_network_interface`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_network_interface_d1a78974` (`nodelist_id`);

ALTER TABLE `thunder_nic_mapping`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_nic_mapping_c17b074a` (`nic_id`);

ALTER TABLE `thunder_nodelist`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_nodelog`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_noderole`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_noderole_278213e1` (`role_id`), ADD KEY `thunder_noderole_e453c5c5` (`node_id`);

ALTER TABLE `thunder_nodespec`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_nodespec_d1a78974` (`nodelist_id`);

ALTER TABLE `thunder_option`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_option_value`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_option_value_78e320f1` (`cloud_id`), ADD KEY `thunder_option_value_9c74a4f3` (`option_id`);

ALTER TABLE `thunder_patch_updates`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_permission`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_private_network`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_private_network_0048ef3e` (`thunder_network_details_id`);

ALTER TABLE `thunder_public_network`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_public_network_0048ef3e` (`thunder_network_details_id`);

ALTER TABLE `thunder_recipe`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_recipe_ab0b04ce` (`roletype_id`);

ALTER TABLE `thunder_roletype`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_scope`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_task`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_update_logs`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `thunder_userrole`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_userrole_278213e1` (`role_id`), ADD KEY `thunder_userrole_6340c63c` (`user_id`);

ALTER TABLE `thunder_userrole_type`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_userrole_type_e8b327e7` (`domain_id`), ADD KEY `thunder_userrole_type_83d7f98b` (`permission_id`);

ALTER TABLE `thunder_user_role_mapping`
 ADD PRIMARY KEY (`id`), ADD KEY `thunder_user_role_mapping_84566833` (`role_id`), ADD KEY `thunder_user_role_mapping_e8701ad4` (`user_id`);


ALTER TABLE `auth_group`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `auth_group_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `auth_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=151;
ALTER TABLE `auth_user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
ALTER TABLE `auth_user_groups`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `auth_user_user_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `django_admin_log`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `django_content_type`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=51;
ALTER TABLE `install_installation_status`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
ALTER TABLE `install_network_card`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `install_pxe_network`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `install_thunder_access`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `shoogie_servererror`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_alert`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_cloud`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_cloud_databag`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_cloud_databag_item`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=21;
ALTER TABLE `thunder_cloud_domain`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
ALTER TABLE `thunder_cloud_domain_map`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
ALTER TABLE `thunder_cloud_specification`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=17;
ALTER TABLE `thunder_cloud_spec_values`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_disk_drive`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_dns_server`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_domain`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_domain_role`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6;
ALTER TABLE `thunder_domain_role_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
ALTER TABLE `thunder_floatingip_network`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_job`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_log`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_manage_addons`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_monitor_service`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
ALTER TABLE `thunder_network_details`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_network_interface`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_nic_mapping`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_nodelist`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_nodelog`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_noderole`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_nodespec`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_option`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=8;
ALTER TABLE `thunder_option_value`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_patch_updates`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_private_network`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_public_network`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_recipe`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=35;
ALTER TABLE `thunder_roletype`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
ALTER TABLE `thunder_scope`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_task`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_update_logs`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_userrole`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_userrole_type`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `thunder_user_role_mapping`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;

ALTER TABLE `auth_group_permissions`
ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

ALTER TABLE `auth_permission`
ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

ALTER TABLE `auth_user_groups`
ADD CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
ADD CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `auth_user_user_permissions`
ADD CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
ADD CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `django_admin_log`
ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
ADD CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `install_pxe_network`
ADD CONSTRAINT `nic_id_refs_id_bb075d86` FOREIGN KEY (`nic_id`) REFERENCES `install_network_card` (`id`);

ALTER TABLE `install_thunder_access`
ADD CONSTRAINT `nic_id_refs_id_8fc30abd` FOREIGN KEY (`nic_id`) REFERENCES `install_network_card` (`id`);

ALTER TABLE `shoogie_servererror`
ADD CONSTRAINT `user_id_refs_id_e96cdda6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `thunder_cloud`
ADD CONSTRAINT `user_id_refs_id_9d40449c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `thunder_cloud_databag`
ADD CONSTRAINT `cloud_id_refs_id_593e561a` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`),
ADD CONSTRAINT `item_id_refs_id_39fa5adf` FOREIGN KEY (`item_id`) REFERENCES `thunder_cloud_databag_item` (`id`);

ALTER TABLE `thunder_cloud_domain_map`
ADD CONSTRAINT `thunder_cl_domain_id_7659d7deaa3e43fc_fk_thunder_cloud_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `thunder_cloud_domain` (`id`),
ADD CONSTRAINT `thunder_cloud_domai_cloud_id_dfed449cd65dc74_fk_thunder_cloud_id` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`);

ALTER TABLE `thunder_cloud_specification`
ADD CONSTRAINT `role_id_refs_id_1856c77c` FOREIGN KEY (`role_id`) REFERENCES `thunder_roletype` (`id`);

ALTER TABLE `thunder_cloud_spec_values`
ADD CONSTRAINT `cloud_id_refs_id_35f9c4ec` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`),
ADD CONSTRAINT `spec_id_refs_id_f003926b` FOREIGN KEY (`spec_id`) REFERENCES `thunder_cloud_specification` (`id`);

ALTER TABLE `thunder_disk_drive`
ADD CONSTRAINT `nodelist_id_refs_id_e1588541` FOREIGN KEY (`nodelist_id`) REFERENCES `thunder_nodelist` (`id`);

ALTER TABLE `thunder_dns_server`
ADD CONSTRAINT `thunder_network_details_id_refs_id_c65baace` FOREIGN KEY (`thunder_network_details_id`) REFERENCES `thunder_network_details` (`id`);

ALTER TABLE `thunder_domain`
ADD CONSTRAINT `scope_id_refs_id_e13c8483` FOREIGN KEY (`scope_id`) REFERENCES `thunder_scope` (`id`);

ALTER TABLE `thunder_domain_role`
ADD CONSTRAINT `D57b6acd5ade8e1da6a28cab65c30d4a` FOREIGN KEY (`permission_id`) REFERENCES `thunder_domain_role_permission` (`id`),
ADD CONSTRAINT `thunder_do_domain_id_46440d90174d4745_fk_thunder_cloud_domain_id` FOREIGN KEY (`domain_id`) REFERENCES `thunder_cloud_domain` (`id`);

ALTER TABLE `thunder_floatingip_network`
ADD CONSTRAINT `thunder_network_details_id_refs_id_b7d8be89` FOREIGN KEY (`thunder_network_details_id`) REFERENCES `thunder_network_details` (`id`);

ALTER TABLE `thunder_job`
ADD CONSTRAINT `cloud_id_refs_id_d48c08d3` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`);

ALTER TABLE `thunder_network_details`
ADD CONSTRAINT `cloud_id_refs_id_287f0737` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`);

ALTER TABLE `thunder_network_interface`
ADD CONSTRAINT `nodelist_id_refs_id_a655d0ff` FOREIGN KEY (`nodelist_id`) REFERENCES `thunder_nodelist` (`id`);

ALTER TABLE `thunder_nic_mapping`
ADD CONSTRAINT `nic_id_refs_id_95f562bf` FOREIGN KEY (`nic_id`) REFERENCES `thunder_network_interface` (`id`);

ALTER TABLE `thunder_noderole`
ADD CONSTRAINT `node_id_refs_id_7973dd72` FOREIGN KEY (`node_id`) REFERENCES `thunder_nodelist` (`id`),
ADD CONSTRAINT `role_id_refs_id_2874f63d` FOREIGN KEY (`role_id`) REFERENCES `thunder_roletype` (`id`);

ALTER TABLE `thunder_nodespec`
ADD CONSTRAINT `nodelist_id_refs_id_b2a685ca` FOREIGN KEY (`nodelist_id`) REFERENCES `thunder_nodelist` (`id`);

ALTER TABLE `thunder_option_value`
ADD CONSTRAINT `cloud_id_refs_id_bdb0e07a` FOREIGN KEY (`cloud_id`) REFERENCES `thunder_cloud` (`id`),
ADD CONSTRAINT `option_id_refs_id_4ba57f3d` FOREIGN KEY (`option_id`) REFERENCES `thunder_option` (`id`);

ALTER TABLE `thunder_private_network`
ADD CONSTRAINT `thunder_network_details_id_refs_id_0d9343d1` FOREIGN KEY (`thunder_network_details_id`) REFERENCES `thunder_network_details` (`id`);

ALTER TABLE `thunder_public_network`
ADD CONSTRAINT `thunder_network_details_id_refs_id_aff1a0e2` FOREIGN KEY (`thunder_network_details_id`) REFERENCES `thunder_network_details` (`id`);

ALTER TABLE `thunder_recipe`
ADD CONSTRAINT `roletype_id_refs_id_a21302b8` FOREIGN KEY (`roletype_id`) REFERENCES `thunder_roletype` (`id`);

ALTER TABLE `thunder_userrole`
ADD CONSTRAINT `role_id_refs_id_22b252af` FOREIGN KEY (`role_id`) REFERENCES `thunder_userrole_type` (`id`),
ADD CONSTRAINT `user_id_refs_id_39e7c667` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `thunder_userrole_type`
ADD CONSTRAINT `domain_id_refs_id_ca2e1d63` FOREIGN KEY (`domain_id`) REFERENCES `thunder_domain` (`id`),
ADD CONSTRAINT `permission_id_refs_id_ca2e1d63` FOREIGN KEY (`permission_id`) REFERENCES `thunder_domain` (`id`);

ALTER TABLE `thunder_user_role_mapping`
ADD CONSTRAINT `thunder_user_r_role_id_4b34bec9a5d22a9_fk_thunder_domain_role_id` FOREIGN KEY (`role_id`) REFERENCES `thunder_domain_role` (`id`),
ADD CONSTRAINT `thunder_user_role_mappi_user_id_50b761b626e61146_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

INSERT INTO `thunder_patch_updates` (`id`, `version`, `type`, `intsalled_on`, `rollbacked_on`, `rollbacked_status`) VALUES
(1, '1.0', 'macro', '0000-00-00 00:00:00', NULL, 0);


DROP TABLE IF EXISTS `thunder_system_password`;

CREATE TABLE `thunder_system_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `value` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

INSERT INTO `thunder_system_password` VALUES (1,'SYSTEM_OS_PASS','zvo7nlj6buGSZA5V3dmqqQ==');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
