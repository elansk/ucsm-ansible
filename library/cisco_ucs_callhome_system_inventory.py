#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_ucs_callhome_system_inventory
short_description: configures callhome system inventory on a cisco ucs server
version_added: 0.9.0.0
description:
   -  configures callhome system inventory on a cisco ucs server
Input Params:
    admin_state:
        description: enable/disable send inventory
        required: False
        choices: ['on', 'off']
        default: "on"
    interval_days:
        description: send interval(days)
        required: False
        default: "30"
    time_of_day_hour:
        description: Hours of day to send
        required: False
        default: "0"
    time_of_day_minute:
        description: Minute of hour
        required: False
        default: "0"
    maximum_retry_count:
        description: maximum retry count
        required: False
        default: "1"
    poll_interval_seconds:
        description: poll interval in seconds
        required: False
        default: "300"
    retry_delay_minutes:
        description: retry after 'n' minutes
        required: False
        default: "10"
    minimum_send_now_interval_seconds:
        description: minimun send interval
        required: False
        default: "5"
    send_now:
        description: send inventory now
        required: False
        choices: ['yes', 'no']
        default: "no"

requirements: ['ucsmsdk', 'ucsm_apis']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_ucs_callhome_system_inventory:
    admin_state: "on"
    interval_days: "30"
    time_of_day_hour: "0"
    time_of_day_minute: "0"
    maximum_retry_count: "1"
    poll_interval_seconds: "300"
    retry_delay_minutes: "10"
    minimum_send_now_interval_seconds: "5"
    send_now: "no"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''


def _argument_mo():
    return dict(
                admin_state=dict(type='str', choices=['on', 'off'],
                                 default="on"),
                interval_days=dict(type='str', default="30"),
                time_of_day_hour=dict(type='str', default="0"),
                time_of_day_minute=dict(type='str', default="0"),
                maximum_retry_count=dict(type='str', default="1"),
                poll_interval_seconds=dict(type='str', default="300"),
                retry_delay_minutes=dict(type='str', default="10"),
                minimum_send_now_interval_seconds=dict(type='str',
                                                       default="5"),
                send_now=dict(type='str', choices=['yes', 'no'], default="no"),
    )


def _argument_connection():
    return  dict(
        # UcsHandle
        ucs_server=dict(type='dict'),

        # Ucs server credentials
        ucs_ip=dict(type='str'),
        ucs_username=dict(default="admin", type='str'),
        ucs_password=dict(type='str', no_log=True),
        ucs_port=dict(default=None),
        ucs_secure=dict(default=None),
        ucs_proxy=dict(default=None)
    )


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    from ansible.module_utils.cisco_ucs import UcsConnection
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
            continue
        args[key] = params.get(key)
    return args


def setup_callhome_system_inventory(server, module):
    from ucsm_apis.admin.callhome import callhome_system_inventory_configure
    from ucsm_apis.admin.callhome import callhome_system_inventory_exists

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = callhome_system_inventory_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists
    callhome_system_inventory_configure(handle=server, **args_mo)

    return True


def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_callhome_system_inventory(server, module)
    except Exception as e:
        err = True
        result["msg"] = "setup error: %s " % str(e)
        result["changed"] = False

    return result, err


def main():
    from ansible.module_utils.cisco_ucs import UcsConnection

    module = _ansible_module_create()
    conn = UcsConnection(module)
    server = conn.login()
    result, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**result)
    module.exit_json(**result)


if __name__ == '__main__':
    main()

