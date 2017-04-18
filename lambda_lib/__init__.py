
from lib.helper import cleanInstallNpmPackages, executeLambda

def create_lambda(npm_packages,javascript_code,function_name):
    print("This function should create or update an AWS lambda function with the function name:")
    print(function_name)

    print("Using the following npm packages:")
    for k, v in npm_packages.items():
        print("     Package : {0} Version : {1}".format(k, v))

    print("With this javascript code:")
    print(javascript_code)

    cleanInstallNpmPackages()

def execute_lambda(function_name, event_object):
    print("This function should execute an existing AWS lambda function with the ID:")
    print(function_name)

    print("Using the following event object:")
    print(event_object)

    executeLambda()

def delete_lambda(function_name):
    print("This function should delete an existing AWS lambda function with the ID:")
    print(function_name)








