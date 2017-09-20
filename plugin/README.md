# Hippo Plugin

Hippo Plugin 是一個結合 Hippo Manager ，讓 microservice 達到監控與自動重啟的機制

#### 項目結構

| 文件夾        |     說明      |
| :----------- | :----------- |
| build-tool   | plugin 與 service 的自動化安裝/移除模組                      |
| test         | 示範程式碼，Demo 一個 microservice 與 hippo pluing 的使用方式 |

## 前置作業

### 若為 MacOS 需安裝與 linux 一致的 getopt

```shell=
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

## Installation

### 安裝 hippo plugin 到專案

於 `plugin/build-tool` 資料夾執行 `build.sh`

```shell=
./build.sh --install $your-project-home
./build.sh -i $your-project-home
```

查看 project path 目錄下會多一個 `hippo` 的資料夾


### 填寫 Kafka 相關資訊

於 `$PROJECT_HOME/hippo/etc/env.conf`

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

### 新增一個 service

**於 Project 內的 hippo/build-tool**

於 `plugin/build-tool` 資料夾執行 `build.sh`

```shell=
./build.sh --create-service $SERVICE $your-project-home
```

```shell=
./build.sh --create-service $SERVICE --cmd "sh {PROJECT_HOME}/sbin/mock_training.sh" $your-project-home
```


### 設定執行 service 的 command

於 `$PROJECT_HOME/hippo/etc/$SERVICE/$SERVICE-env.conf` 編輯 `EXECUTE_CMD`

```shell
# You can use PROJECT_HOME variable to build command
EXECUTE_CMD="sh ${PROJECT_HOME}/sbin/mock_training.sh"
```


## HOW TO USE Build-Tool

### build.sh
安裝/移除專案的 hippo plugin   
新增/刪除/查詢 Project 內的 Service

#### Usage

```shell
plugin/build-tool/build.sh [OPTIONS] PROJECT_PATH
```

#### Options

| short | command                   | description                    | Default | Required |
| :---- | :------------------------ | :-----------------------------| :----- | :-----    |
| -h    | --help                    | Show help                       |        |        |
| -i    | --install                 | 安裝 hippo plugin 到專案         |        |FALSE   |
| -u    | --uninstall               | 移除專案的 hippo plugin          |        |FALSE   |
|       | --check-install           | 確認 Project 內是否有安裝 hippo plugin |   |FALSE   |
| -l    | --list-services           | 列出 Project 內的 Service        |        |FALSE   |
|       |--check-service=SERVICE    | 確認 Project 內是否有該 Service   |        |FALSE   |
|       |--cmd=\"CMD\"              | 啟動 Service 時帶入的指令(執行 py、jar、shell)，可以使用  "{PROJECT_HOME}" 變數 |  | FALSE |
|       | --build-account           | 遠端 server 的帳號           | HippoPlugin owner | FALSE |
|       | --build-server            | 遠端 server 的 host or ip   | HippoPlugin server | FALSE   |

> `--cmd` 需與 `--create-service` 一起使用

#### Example

安裝 hippo plugin 到 `recommender_system` 專案

```shell=
./plugin/build-tool/build.sh --install --build-server 88.8.146.34 ~/recommender_system  

or

./plugin/build-tool/build.sh -i ~/recommender_system

```

移除 `recommender_system` 專案的 hippo plugin

```shell=
./plugin/build-tool/build.sh --uninstall ~/recommender_system

or

./plugin/build-tool/build.sh -u ~/recommender_system

```


新增一個 SERVICE `recommender-evaluation` 的 Service

```shell=
./plugin/build-tool/build.sh --build-server localhost --create-service recommender-evaluation ~/recommender_system
```

新增一個 SERVICE `recommender-training` 的 Service，並設定啟動時帶入的 command

```shell=
./plugin/build-tool/build.sh --build-server localhost --create-service recommender-training --cmd "{PROJECT_HOME}/sbin/mock_training.sh" ~/recommender_system
```

查詢 Project 內的 Service

```shell=
./plugin/build-tool/build.sh --list-services --build-server localhost ~/recommender_system
```

Output

```shell=
PROJECT_NAME                             SERVICE_NAME
recommender_system                       recommender-evaluation
recommender_system                       recommender-training

```


刪除一個 SERVICE `recommender-evaluation` 的 Service

```shell=
./plugin/build-tool/build.sh --build-server --delete-service recommender-evaluation ~/recommender_system
```

## HOW TO USE Service Plugin
### monitor-start

啟動 monitor 服務

#### Usage

```shell
${PROJECT_HOME}/hippo/bin/monitor-start [OPTIONS] SERVICE
```


#### Options

| short | command                    | description               | Default | Required |
| :---- | :------------------------  | :------------------------ | :------ | :------- |
| -h    | --help                     | Show help                 |         |          |
| -i    | --interval                 | 監控的間隔(秒)              |         |TRUE      |
| -r    | --restart                  | 重啟服務模式                |FALSE    |FALSE     |


#### Example

啟動監控間隔 60 秒的 service `recommender-training`

```shell=
${PROJECT_HOME}/hippo/bin/monitor-start -i 60 recommender-training
```

重新啟動一個監控間隔 30 秒的 service `recommender-training`

```shell
${PROJECT_HOME}/hippo/bin/monitor-start -r -i 30 recommender-training
```

### monitor-stop

停止 monitor 服務

#### Usage

```shell
${PROJECT_HOME}/hippo/bin/monitor-stop SERVICE
```

#### Example

暫停 service `recommender-training`

```shell
${PROJECT_HOME}/hippo/bin/monitor-stop recommender-training
```


### monitor-status

檢查 monitor 、hippo service 服務狀態

#### Usage

```shell
${PROJECT_HOME}/hippo/bin/monitor-status SERVICE
```

#### Example

檢查 service `recommender-training` 狀態

```shell
${PROJECT_HOME}/hippo/bin/monitor-status recommender-training
```
