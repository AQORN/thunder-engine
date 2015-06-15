# vim: ft=sh:

@test "mysql registered with etcd" {
  curl http://127.0.0.1:4001/v1/keys/services/mysql/members
}

@test "mysql is running" {
  netstat -tan | grep 3306
}

@test "mysql show databases" {
  /usr/local/mysql/bin/mysqlshow -uroot -ppassword
}

@test "mysql status" {
  /usr/local/mysql/bin/mysqladmin status -uroot -ppassword
}
