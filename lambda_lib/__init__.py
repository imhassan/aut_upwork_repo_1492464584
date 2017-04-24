
#from lib.helper import cleanInstallNpmPackages, executeLambda
import subprocess
import os
import boto3
from boto3.session import Session
import time


config = {}
config['tmpFolder'] = os.path.dirname(os.path.realpath(__file__)) +"/tmp/" #Full path
config['region'] = "us-west-2"
config['accessKeyId'] = ""
config['secretAccessKey'] = ""
config['roleName'] = "lambda_basic_execution2";
config['rolePolicyDoc'] = '{"Version":"2012-10-17","Statement":{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}}'
config['rolePolicy'] = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":["logs:*"],"Resource":"arn:aws:logs:*:*:*"}]}'

session = Session(aws_access_key_id=config['accessKeyId'], aws_secret_access_key=config['secretAccessKey'], region_name=config['region'])
lambdaClient = boto3.client('lambda')
IAMclient = boto3.client('iam')


def create_role():
     #Check IAM Role exist. if not create it first.
    try:
        role_resp =  IAMclient.get_role(RoleName=config['roleName'])
        print('role already exist.')
        return role_resp
    except:
        #Create role
        print('role not exist create new.')
        role_response = IAMclient.create_role( RoleName=config['roleName'], AssumeRolePolicyDocument=config['rolePolicyDoc'])
        policy_response = IAMclient.put_role_policy( RoleName=config['roleName'], PolicyName='lambda_custom_policy', PolicyDocument=config['rolePolicy'])
        time.sleep(10)
        print('role created')
        return role_response
        
def create_lambda(npm_packages,javascript_code,function_name):
    print("This function should create or update an AWS lambda function with the function name:")
    print(function_name)
    print(os.getcwd())

    cleanCmd = "rm -rf "+config['tmpFolder']+"*"
    print(cleanCmd)
    subprocess.call(cleanCmd, shell=True)
    
    print("Using the following npm packages:")
    for k, v in npm_packages.items():
        npmInstallCmd = "npm install " + k + "@"+v+" --prefix " + config['tmpFolder']
        print (npmInstallCmd)
        subprocess.call(npmInstallCmd, shell=True)
        #print(" Package : {0} Version : {1}".format(k, v))
    
    with open(config['tmpFolder']+'index.js', 'w') as f:
        f.write(javascript_code)

    zipCmd = "cd "+config['tmpFolder']+"; zip   -r  lambda.zip   node_modules/   index.js"
    print(zipCmd)
    subprocess.call(zipCmd, shell=True)

    role_resp = create_role()
    print("Arn: "+role_resp['Role']['Arn'])
    #Now check function name exist, if not create it
    try:
        response = lambdaClient.get_function(FunctionName=function_name)
        #print(response)
        print("function already exist, updating  its code")
        with open(config['tmpFolder']+"lambda.zip") as file:
            response = lambdaClient.update_function_code(FunctionName=function_name, ZipFile=file.read())
            print("DONE")
    except: 
        print('There is no lambda function. create new')
        with open(config['tmpFolder']+"lambda.zip") as file:
            response = lambdaClient.create_function( FunctionName=function_name, Runtime='nodejs6.10', Role=role_resp['Role']['Arn'], Handler="index.handler", Code={ 'ZipFile': file.read() }, 
            Description='This is description of lambda function',
            Timeout=15,
            MemorySize=128,
            Publish=True)
            print("DONE.")
       
def execute_lambda(function_name, event_object):
    print("This function should execute an existing AWS lambda function with the ID:")
    print(function_name)

    print("Using the following event object:")
    print(event_object)
    
    response = lambdaClient.invoke( FunctionName=function_name, Payload=event_object)
    print("Function Response is below.")
    print(response['Payload'].read())
    
def delete_lambda(function_name):
    print("This function should delete an existing AWS lambda function with the ID:")
    print(function_name)
    response = lambdaClient.delete_function(FunctionName=function_name)
    print("deleted function: "+function_name)
    