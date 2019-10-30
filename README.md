# intro

Port scan script (unauthorized / weak password) 端口扫描脚本(未授权/弱口令)。

Support for the following services 支持扫描以下服务

```angular
redis, mongo, genkins, memcached, jboss, zookeeper, 
rsync, couchdb, elasticsearch, hadoop, jupyter,
docker, ftp, smb, postgresql, oracle, mssql, mysql
```

# how to use?

- -H specify a single target 指定单个目标
- -HF specify target file 指定目标文件
- -P specify port(Ignorable) 指定扫描端口(可忽略)

example:

![](https://github.com/saucer-man/unauth_scan/blob/master/doc/show.png)