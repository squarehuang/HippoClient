# Hippo Plugin Build Tool

Hippo Plugin 是一個讓 microservice 具有彈性的 start|restart|stop|status 功能並加入自動監控重啟的機制

Build Tool 能夠快速地自動化安裝 Hippo Plugin 到各個 Project

本頁以手動執行 build tool 的情境，詳細介紹 build.sh 使用方式

#### 項目結構

| 文件夾        |     說明      |
| :----------- | :----------- |
| plugin-installer.sh     | service 的自動化安裝/移除 plugin 模組                      |
## 前置作業

### 若為 MacOS 需安裝與 linux 一致的 getopt

```shell=
brew install gnu-getopt
echo 'export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"' >> ~/.bash_profile
```


## Installation

### 安裝 hippo plugin 到專案

執行 `./plugin-installer.sh` 

```shell=
./plugin-installer.sh --install $your-project-home
./plugin-installer.sh -i $your-project-home
```

查看 project path 目錄下會多一個 `hippo` 的資料夾

### 填寫 Kafka 相關資訊

於 `$PROJECT_HOME/hippo/etc/monitor.conf`

| name           | description        |
| :--------------| :------------------|
| KAFKA_HOST     | kafka 的 host      |
| HEALTH_TOPIC   | 傳送監控資訊的 topic |

```shell
[kafka]
KAFKA_HOST=localhost:9092
HEALTH_TOPIC=service-health
```

### 新增一個 service

```shell=
./plugin-installer.sh --create-service $SERVICE --cmd "sh {PROJECT_HOME}/sbin/mock_training.sh" $your-project-home
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
./plugin-installer.sh [OPTIONS] PROJECT_PATH
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

> `--cmd` 需與 `--create-service` 一起使用

#### Example

安裝 hippo plugin 到 `recommender_system` 專案

```shell=
./plugin-installer.sh --install ~/recommender_system  

```

移除 `recommender_system` 專案的 hippo plugin

```shell=
./plugin-installer.sh --uninstall ~/recommender_system

or

./plugin-installer.sh -u ~/recommender_system

```


新增一個 SERVICE `recommender-evaluation` 的 Service

```shell=
./plugin-installer.sh --create-service recommender-evaluation ~/recommender_system
```

新增一個 SERVICE `recommender-training` 的 Service，並設定啟動時帶入的 command

```shell=
./plugin-installer.sh --create-service recommender-training --cmd "{PROJECT_HOME}/sbin/mock_training.sh" ~/recommender_system
```

查詢 Project 內的 Service

```shell=
./plugin-installer.sh --list-services ~/recommender_system
```

Output

```shell=
PROJECT_NAME                             SERVICE_NAME
recommender_system                       recommender-evaluation
recommender_system                       recommender-training

```


刪除一個 SERVICE `recommender-evaluation` 的 Service

```shell=
./plugin-installer.sh --build-server --delete-service recommender-evaluation ~/recommender_system
```

## HOW TO USE Service Plugin

> 當 Project 已安裝 Hippo Plugin 可以使用以下指令啟動 service
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
| -i    | --interval                 | 監控的間隔(毫秒              |         |TRUE      |
| -r    | --restart                  | 重啟服務模式                |FALSE    |FALSE     |
| -c    | --coordAddress             | coordAddress              |FALSE    |FALSE     |
| -u    | --user                     | 啟動服務的 user             |FALSE    |FALSE     |


#### Example

啟動監控間隔 60 秒的 service `recommender-training`

```shell=
${PROJECT_HOME}/hippo/bin/monitor-start -i 60000 recommender-training
```

重新啟動一個監控間隔 30 秒的 service `recommender-training`

```shell
${PROJECT_HOME}/hippo/bin/monitor-start -r -i 30000 recommender-training
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
