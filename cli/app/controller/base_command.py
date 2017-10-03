from collections import OrderedDict
import json
import datetime
from utils.base_app import BaseApp
from entity.column_enum import HippoColumn


class Command(BaseApp):
    def execute(self):
        pass

    def output(self, output_dict):
        print(json.dumps(output_dict, indent=4))

    def order_dict(self, output_dict, enum_header):
        sort_order = [e.value for e in enum_header]
        output_dict_ordered = OrderedDict(
            sorted(output_dict.iteritems(), key=lambda (k, v): sort_order.index(k)))
        return output_dict_ordered

    def refactor_result(self, resp):
        '''
            exectime : timestamp to YYYY-MM-DD HH:mm:ss
            lastupdatetime : timestamp to YYYY-MM-DD HH:mm:ss
            interval : ms to sec 
        '''
        output_dict = {}
        for k, v in resp.items():
            if k == HippoColumn.CONFIG.value:
                for conf_k, conf_v in v.items():
                    if conf_k == HippoColumn.EXECTIME.value:
                        conf_v = datetime.datetime.fromtimestamp(
                            conf_v / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                    output_dict.setdefault(conf_k, conf_v)
            else:
                if k == HippoColumn.LASTUPDATETIME.value:
                    v = datetime.datetime.fromtimestamp(
                        v / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                elif k == HippoColumn.INTERVAL.value:
                    v = v / 1000
                output_dict.setdefault(k, v)

        output_dict_ordered = self.order_dict(output_dict, HippoColumn)
        return output_dict_ordered
