from utils.base_app import BaseApp
from collections import OrderedDict
import json


class Command(BaseApp):
    def execute(self):
        pass

    def output(self, output_dict, enum_header):
        sort_order = [e.value for e in enum_header]
        output_dict_ordered = OrderedDict(
            sorted(output_dict.iteritems(), key=lambda (k, v): sort_order.index(k)))
        print(json.dumps(output_dict_ordered, indent=4))
