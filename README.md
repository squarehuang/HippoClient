# HippoClient

HippoClient 是一個介接 Hippo Manager 與安裝於 service 的 plugin，讓 microservice 達到監控與自動重啟的機制

#### 項目結構

| 文件夾        |     說明      |
| :----------- | :----------- |
| build-tool   | plugin 與 service 的自動化安裝/移除模組  |
| cli          | 使用者操作介面                          |
| etc          | cli 相關設定檔                         |
| plugin-templates  | build tool 使用到的 template |
| example      | 示範程式碼，Demo 透過 hippo cli 操作 microservice  |


## 前置作業

### python package
- netifaces
- click

### 若為 MacOS 需安裝與 linux 一致的 getopt

```bash
brew install gnu-getopt
echo 'export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"' >> ~/.bash_profile
```

### build-tool 的使用需先設定 server 與 server 之間 ==免密碼登入 SSH server==

e.g.

```
ssh-keygen -t rsa 或 ssh-keygen -d (dsa) => 產生出 id_rsa, id_rsa.pub
scp id_rsa.pub server_hostname:~/.ssh/
ssh server_hostname
cat .ssh/id_rsa.pub >> .ssh/authorized_keys 即可
```

### 填寫 python 環境相關資訊
於 `./etc/runtime-env-info.sh`

```bash
export PYTHONPATH=${PYTHONPATH}:${APP_HOME}/cli/app

# Setting the python virtual ENV path
source /Users/square_huang/ENV/bin/activate
```

### 填寫 CLI 相關設定

於 `./etc/cli-env.conf`

```
[HippoManagerAPI]
host = localhost
port = 8080
base = /hippo/v0.2.0
```

### 填寫 plugin template 的 Kafka 相關資訊

於 `/plugin-templates/basic/etc/env.conf`

| name           | description        |
| :--------------| :------------------|
| KAFKA_PRODUCER | producer 路徑      |
| KAFKA_HOST     | kafka 的 host      |
| HEALTH_TOPIC   | 傳送監控資訊的 topic |

```shell
SERVICE_LIST=""

KAFKA_PRODUCER=/Users/square_huang/Documents/Software/kafka_2.10-0.9.0.0/bin/kafka-console-producer.sh
KAFKA_HOST=localhost:9092
HEALTH_TOPIC=service-health
```

## HOW TO USE CLI


### register

#### Usage

```bash
Usage: hippo register [OPTIONS]
```

#### Options

```bash
Options:
  -p, --project_home TEXT  [required]
  -s, --service_name TEXT  Service name, Default: last directory name from
                           ${project_home}
  -c, --run_cmd TEXT       command for run service, you can use
                           "{PROJECT_HOME}" variable to build command (e.g.
                           "python {PROJECT_HOME}/bin/message_client.py")
  --client_ip TEXT         Client server IP, Default: 192.168.0.106
  --api_host TEXT          hippo manager api host, Default: localhost
  --api_port TEXT          hippo manager api port, Default: 8080
  -u, --user TEXT          register user, Default: UNKNOWN
  -h, --help               Show this message and exit.
```


#### Example

註冊一個 recommender-training 的 service

```bash
hippo register -p /Users/square_huang/test/recommender_system -s recommender-training -u sq
```

註冊一個 recommender-prediction 的 service，並加入 run command

```bash
hippo register -p /Users/square_huang/test/recommender_system -s recommender-prediction -c "sh /Users/square_huang/test/recommender_system/bin/mock_prediction.sh" -u sq
```

### remove

#### Usage

```bash
Usage: hippo remove [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT          hippo id  [required]
  -f, --force        force stop and deregister if service is running
  -d, --del_service  delete service plugin from project
  --api_host TEXT    hippo manager api host, Default: localhost
  --api_port TEXT    hippo manager api port, Default: 8080
  -h, --help         Show this message and exit.
```


#### Example

取消註冊一個 service
> 若該 service 狀態為 running 時，將無法取消註冊
```bash
hippo remove --id 18d424b5f85790aad450d8d0f912ab28 
```

強制取消註冊一個 service

```bash
hippo remove --id 18d424b5f85790aad450d8d0f912ab28 -f
```

取消註冊一個 service，並刪除該 service 的 hippo plugin

```bash
hippo remove --id 18d424b5f85790aad450d8d0f912ab28 -d
```


### start

#### Usage

```bash
Usage: hippo start [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT               hippo id  [required]
  -i, --interval INTEGER  sec
  --api_host TEXT         hippo manager api host, Default: localhost
  --api_port TEXT         hippo manager api port, Default: 8080
  -h, --help              Show this message and exit.
```

#### Example

啟動一個已註冊的 service
```bash
hippo start --id 6c58b631148c86d43e3b1c66bdb73d3f
```

啟動一個已註冊的 service ，並設定 監控區間 (interval)

```bash
hippo start --id 6c58b631148c86d43e3b1c66bdb73d3f -i 10
```


### restart

#### Usage

```bash
Usage: hippo restart [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT               hippo id  [required]
  -i, --interval INTEGER  sec
  --api_host TEXT         hippo manager api host, Default: localhost
  --api_port TEXT         hippo manager api port, Default: 8080
  -h, --help              Show this message and exit.
```

#### Example

重新啟動一個正在執行的 service
```bash
hippo restart --id 6c58b631148c86d43e3b1c66bdb73d3f
```

重新啟動一個已註冊的 service ，並設定 監控區間 (interval)

```bash
hippo restart --id 6c58b631148c86d43e3b1c66bdb73d3f -i 10
```


### stop

#### Usage

```bash
Usage: hippo stop [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT        hippo id  [required]
  --api_host TEXT  hippo manager api host, Default: localhost
  --api_port TEXT  hippo manager api port, Default: 8080
  -h, --help       Show this message and exit. 
```

#### Example

停止一個正在執行的 service
```bash
hippo-stop --id 6c58b631148c86d43e3b1c66bdb73d3f 
```

停止一個正在執行的 service，並刪除該 service 的 plugin

```bash
hippo-stop --id 6c58b631148c86d43e3b1c66bdb73d3f -d

```


### restart

#### Usage

```bash
Usage: hippo restart [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT               hippo id  [required]
  -i, --interval INTEGER  sec
  --api_host TEXT         hippo manager api host, Default: localhost
  --api_port TEXT         hippo manager api port, Default: 8080
  -h, --help              Show this message and exit.
```

#### Example

重新啟動一個正在執行的 service
```bash
hippo restart --id 6c58b631148c86d43e3b1c66bdb73d3f
```

重新啟動一個已註冊的 service ，並設定 監控區間 (interval)

```bash
hippo restart --id 6c58b631148c86d43e3b1c66bdb73d3f -i 10
```


### stop

#### Usage

```bash
Usage: hippo stop [OPTIONS]
```

#### Options

```bash
Options:
  --id TEXT        hippo id  [required]
  --api_host TEXT  hippo manager api host, Default: localhost
  --api_port TEXT  hippo manager api port, Default: 8080
  -h, --help       Show this message and exit. 
```

#### Example

停止一個正在執行的 service
```bash
hippo-stop --id 6c58b631148c86d43e3b1c66bdb73d3f 
```

停止一個正在執行的 service，並刪除該 service 的 plugin

```bash
hippo-stop --id 6c58b631148c86d43e3b1c66bdb73d3f -d

```

### status

#### Usage

```bash
Usage: hippo status
```

#### Options

```bash
Options:
  --id TEXT         hippo id
  --api_host TEXT   hippo manager api host, Default: localhost
  --api_port TEXT   hippo manager api port, Default: 8080
  -a, --all_mode    Get cluster status, Default: active
  -n, --node_mode   Get node (api_host) status
  -u, --user TEXT   filter by register user
  --client_ip TEXT  filter by client server IP
  -h, --help        Show this message and exit.
```

#### Example

查看 cluster 內所有的 service 狀態
```bash
hippo status
hippo status -u sq
hippo status --client_ip 192.168.0.106


```

根據 id 查看 service 狀態


```bash
hippo status --id 6c58b631148c86d43e3b1c66bdb73d3f
```# git-workshop
