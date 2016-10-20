#!/usr/bin/python
# TODO: License goes here

import library.apigw_rest_api as apigw_rest_api
from library.apigw_rest_api import ApiGwRestApi
import mock
from mock import patch
from mock import create_autospec
import unittest

class TestApiGwRestApi(unittest.TestCase):

  def setUp(self):
    self.module = mock.MagicMock()
    reload(apigw_rest_api)

  def test_boto_module_not_found(self):
    # Setup Mock Import Function
    import __builtin__ as builtins
    real_import = builtins.__import__

    def mock_import(name, *args):
      if name == 'boto': raise ImportError
      return real_import(name, *args)

    # Under Test
    with mock.patch('__builtin__.__import__', side_effect=mock_import):
      reload(apigw_rest_api)
      ApiGwRestApi(self.module)

    # Assert Expected Behavior
    self.module.fail_json.assert_called_with(msg='boto and boto3 are required for this module')
    reload(apigw_rest_api)

  def test_boto3_module_not_found(self):
    # Setup Mock Import Function
    import __builtin__ as builtins
    real_import = builtins.__import__

    def mock_import(name, *args):
      if name == 'boto3': raise ImportError
      return real_import(name, *args)

    # Under Test
    with mock.patch('__builtin__.__import__', side_effect=mock_import):
      reload(apigw_rest_api)
      ApiGwRestApi(self.module)

    # Assert Expected Behavior
    self.module.fail_json.assert_called_with(msg='boto and boto3 are required for this module')
    reload(apigw_rest_api)


  def test_define_argument_spec(self):
    result = ApiGwRestApi._define_module_argument_spec()
    self.assertIsInstance(result, dict)
    self.assertEqual(result, dict(
                     id=dict(required=True, aliases=['name']),
                     description=dict(required=False),
                     state=dict(default='present', choices=['present', 'absent'])
    ))

  @patch.object(apigw_rest_api, 'AnsibleModule')
  @patch.object(apigw_rest_api, 'ApiGwRestApi')
  def test_main(self, mock_ApiGwRestApi, mock_AnsibleModule):
    mock_ApiGwRestApi_instance      = mock.MagicMock()
    mock_AnsibleModule_instance     = mock.MagicMock()
    mock_ApiGwRestApi.return_value  = mock_ApiGwRestApi_instance
    mock_AnsibleModule.return_value = mock_AnsibleModule_instance

    apigw_rest_api.main()

    mock_ApiGwRestApi.assert_called_once_with(mock_AnsibleModule_instance)
    assert mock_ApiGwRestApi_instance.process_request.call_count == 1


if __name__ == '__main__':
    unittest.main()
