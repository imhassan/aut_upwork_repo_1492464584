#!/usr/bin/env python

import lambda_lib

npm_packages = [
    {"moment","2.18.1"},
    {"underscore","1.8.3"}
]

javascript_code = """
  exports.handler = function(event, context) {
    console.log('key1 =', event.key1);
    console.log('key2 =', event.key2);
    console.log('key3 =', event.key3);
    context.succeed('the value for key2 is ' + event.key2);
  };
"""

function_name = "matt_test_lambda_1";

lambda_lib.create_lambda(npm_packages,javascript_code,function_name)
