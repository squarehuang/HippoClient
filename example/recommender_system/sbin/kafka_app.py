from __future__ import print_function
import os
import json
import subprocess
import SimpleHTTPServer
import SocketServer
import configparser
import datetime
import time
from threading import Thread
from kafka import KafkaConsumer, KafkaProducer
import configparser

CONFIG = '/Users/square_huang/Dropbox/Square/Study/Code/hippos/services/recommender_system/etc/dev.conf'
config = configparser.ConfigParser()
config.read(CONFIG)
START_TOPIC = config['kafka']['START_TOPIC']
FINISH_TOPIC = config['kafka']['FINISH_TOPIC']
HIPPONAME = config['kafka']['HIPPONAME']
GROUP_ID = config['kafka']['GROUP_ID']
SCRIPT = config['shell']['BATHPATH']
EVENT = config['shell']['EVENT'].split(',')
SERVERS = config['kafka']['KAFKA_HOST']
PORT = int(config['APP']['PORT'])



class SparkJobSubmitter(Thread):
    daemon = True

    def __init__(self, hippo_name, offset="latest"):
        Thread.__init__(self)
        config = configparser.ConfigParser()
        config.read(CONFIG)
        self.hippo_name = hippo_name
        self.start_topic = START_TOPIC
        self.finish_topic = FINISH_TOPIC
        self.servers = SERVERS
        self.group_id = GROUP_ID
        self.event = EVENT
        self.require_tables = set()

        # consumer
        self.consumer = KafkaConsumer(bootstrap_servers=self.servers, auto_offset_reset=offset, group_id=GROUP_ID)
        self.consumer.subscribe(self.start_topic)

        # producer
        self.producer = KafkaProducer(bootstrap_servers=self.servers)

    def pub_job_result(self,tag_date):
        print('pub_job_result')
        #finish_time = int(time.time())
        finish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for event in self.event:
            pub_msg = {"hippo_name":self.hippo_name, "job_name":"{}".format(event.strip()), "finish_time": finish_time, "is_success":True, "tag_date":tag_date}
            self.producer.send(self.finish_topic, json.dumps(pub_msg))

    def call_job_on_system(self):
        #date_script = date.strftime('%Y-%m-%d')
        tag_date = datetime.datetime.now().strftime('%Y%m%d')
        print("run script : {}".format(SCRIPT))
        code = subprocess.call(['python', SCRIPT ])
        print("submit spark job result: {}".format(code))
        self.pub_job_result(tag_date)

    def run(self):
        print('====run====')
        for message in self.consumer:
            print (message.value)
            try:
                v =json.loads(message.value)
                if v['table'] == 'chp_event_camp_response':
                   print ('Tables Ready')
                   self.call_job_on_system()
            except Exception as e:
                print(str(e))
                print(message.value)

if __name__ == '__main__':
    print("Start kafka consumer...")
    submitter = SparkJobSubmitter(HIPPONAME)
    submitter.start()

    # == start a server ==
    #input("Wait for message...")
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print("serving client app at port: {}".format(PORT))
    httpd.serve_forever()
