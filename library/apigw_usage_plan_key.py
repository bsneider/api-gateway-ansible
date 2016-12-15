#!/usr/bin/python

# API Gateway Ansible Modules
#
# Modules in this project allow management of the AWS API Gateway service.
#
# Authors:
#  - Brian Felton <bjfelton@gmail.com>
#
# apigw_usage_plan_key
#    Manage creation and removal of API Gateway UsagePlanKey resources
#

## TODO: Add an appropriate license statement

DOCUMENTATION='''
module: apigw_usage_plan_key
description: An Ansible module to add, update, or remove UsagePlanKey
  resources for AWS API Gateway.
version_added: "2.2"
options:
  usage_plan_id:
    description: Id of the UsagePlan resource to which a key will be associated
    type: string
    required: True
  api_key_id:
    description: Id of the UsagePlan resource to which a key will be associated
    type: string
    required: True
  key_type:
    description: Type of the api key.  You can choose any value you like, so long as you choose 'API_KEY'
    type: string
    default: 'API_KEY'
    required: False
    choices: ['API_KEY']
  state:
    description: Should usage_plan_key exist or not
    choices: ['present', 'absent']
    default: 'present'
    required: False
requirements:
    - python = 2.7
    - boto
    - boto3
notes:
    - This module requires that you have boto and boto3 installed and that your
      credentials are created or stored in a way that is compatible (see
      U(https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration)).
'''

EXAMPLES = '''
---
- hosts: localhost
  gather_facts: False
  tasks:
'''

RETURN = '''
'''

__version__ = '${version}'

try:
  import boto3
  import boto
  from botocore.exceptions import BotoCoreError
  HAS_BOTO3 = True
except ImportError:
  HAS_BOTO3 = False

class ApiGwUsagePlanKey:
  def __init__(self, module):
    """
    Constructor
    """
    self.module = module
    if (not HAS_BOTO3):
      self.module.fail_json(msg="boto and boto3 are required for this module")
    self.client = boto3.client('apigateway')

  @staticmethod
  def _define_module_argument_spec():
    """
    Defines the module's argument spec
    :return: Dictionary defining module arguments
    """
    return dict( usage_plan_id=dict(required=True),
                 api_key_id=dict(required=True),
                 key_type=dict(required=False, default='API_KEY', choices=['API_KEY']),
                 state=dict(default='present', choices=['present', 'absent']),
    )

  def _retrieve_usage_plan_key(self):
    """
    Retrieve all usage_plan_keys in the account and match them against the provided name
    :return: Result matching the provided api name or an empty hash
    """
    resp = None
    try:
      get_resp = self.client.get_usage_plan_keys(usagePlanId=self.module.params['usage_plan_id'])

      for item in get_resp.get('items', []):
        if item['id'] == self.module.params.get('api_key_id'):
          resp = item
    except BotoCoreError as e:
      self.module.fail_json(msg="Error when getting usage_plan_keys from boto3: {}".format(e))

    return resp

  def process_request(self):
    """
    Process the user's request -- the primary code path
    :return: Returns either fail_json or exit_json
    """

    usage_plan_key = None
    changed = False
    self.me = self._retrieve_usage_plan_key()


def main():
    """
    Instantiates the module and calls process_request.
    :return: none
    """
    module = AnsibleModule(
        argument_spec=ApiGwUsagePlanKey._define_module_argument_spec(),
        supports_check_mode=True
    )

    usage_plan_key = ApiGwUsagePlanKey(module)
    usage_plan_key.process_request()

from ansible.module_utils.basic import *  # pylint: disable=W0614
if __name__ == '__main__':
    main()
