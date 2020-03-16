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



## 更新历史
- 2020-03-16 增加了
    - Nexus Repository Manager <= 3.14.0 RCE(CVE-2019-7238) 
    - Nexus Repository Manager <= 3.17.0 Week Pass 

- 2020-03-15 增加了
    - Apache Flink任意Jar包上传导致远程代码执行漏洞
    - grafana弱口令
    - druid未授权访问

- 2019-12-16  增加Elasticsearch漏洞扫描
	- cve-2014-3120
	- cve-2015-1427
	- cve-2015-3337

- 2019-11-25 默认去除oracle弱口令测试，案例极少