### mongos_install
初始化新机器:

```json
./dbactuator_redis  --uid={{uid}} --root_id={{root_id}} --node_id={{node_id}} --version_id={{version_id}} --atom-job-list="mongos_install" --data_dir=/path/to/data  --backup_dir=/path/to/backup --user="xxx"  --group="xxx" --payload='{{payload_base64}}'
```


原始payload

```json
{
  "mediapkg":{
    "pkg":"mongodb-linux-x86_64-3.4.20.tar.gz",
    "pkg_md5":"e68d998d75df81b219e99795dec43ffb"
  },
  "ip":"1.1.1.1",
  "port":27021,
  "dbVersion":"3.4.20",
  "instanceType":"mongos",
  "setId": "s1",
  "keyFile": "xxx",
  "auth": true,
  "configDB":["1.1.1.2:27001","1.1.1.3:27002","1.1.1.4:27003"],
  "dbConfig":{
    "slowOpThresholdMs":200,
    "destination":"file"
  }
}
```