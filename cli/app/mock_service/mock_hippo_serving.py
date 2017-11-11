# -*- coding: utf-8 -*-

from entity.response_entity import KeyResponse


def get_manager_sshkey(res):
    """ Remove a Service.
    Arguments:
        coord_address
    Return:
        message
    """
    key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFAM72n1kz56TOFGAeJiXZYGApLQPpxel6qW6wxVEzL51KTQm4sC1RXhXz+RULhd8bNGUQjwuEIIaE+oFLSL99Md0T/E082GVu+bg3VwFDBwzC9Ot5SPoN9d+tTcshgIBFoihZrqISk9TCsvtqmpQHbZKmubjCijOYxjtYhg+eey7Iz2xYidnsYSzMtm0vaHxHL9a1FyQ4VkZMeM6L0qXDw9gdwLzIfxE/5jZhDTk9oQp2rzEgJiDuwo5GWw4RD/SowzS3ednj3bjzl5JaoiRTwWdHexcI9uvHwpChLOkIvUWf1YnFQ4xci3OJh/JQbT5BDxFikgJFS+l5YRjfdGw9 square_huang@SquareHuangdeMacBook-Pro.local"
    resp = dict()
    resp['key'] = key
    return KeyResponse.from_dict(resp)
