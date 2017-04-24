#!/usr/bin/env python

import lambda_lib

function_name = "matt_test_lambda_1"

event_object = '{ "key1" : "value1", "key2" : "value2", "key3" : "value3" }'

lambda_lib.execute_lambda(function_name, event_object)
