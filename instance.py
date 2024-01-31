#!/usr/bin/env python3

import os
import boto3
import argparse
import botocore.exceptions
import datetime

command=""
ID=""
launchTemplate = ""
newSSH = False
username = "ec2-user"
verbose = False

def startSSH(host):

    if verbose:
        print("SSH into: "  + host)

    if os.name == 'nt':
        command = "start \"\" ssh://" + username + "@" + host
        os.system(command)
    else:
        command = "open \"\" ssh://" + username + "@" + host
        os.system(command)

def waitToStart(ec2: boto3.client, instance):

    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance])

    r = ec2.describe_instances(InstanceIds=[instance])
    DNS = r["Reservations"][0]["Instances"][0]["PublicDnsName"]

    return DNS


def createNewInstance():
    ec2 = boto3.client("ec2")

    response = ec2.run_instances(
        LaunchTemplate={
            'LaunchTemplateId': launchTemplate
        },
        MinCount=1,
        MaxCount=1
    )

    if verbose:
        print(response)
    
    if newSSH:
        startSSH(waitToStart(ec2, response["Instances"][0]["InstanceId"]))

    exit(0)

def executeCommand(instance):
    try:
        methodTocall = getattr(instance, command)
        response = methodTocall()

        if verbose:
            print(response)

    except TypeError as e:
        propToGet = eval("instance." + command)
        print(propToGet)

def main():
    if verbose:
        print(args)
        print(datetime.datetime.now().isoformat())
        
    if launchTemplate: # branch. no return
        try:
            createNewInstance()
        except botocore.exceptions.ClientError as e:
            print (e)

    if not ID:
        print("Need ID!")
        exit(-1)

    ec2res = boto3.resource("ec2")
    ec2client = boto3.client("ec2")
    instance = ec2res.Instance(ID)

    if verbose:
        print(instance.state)

    if command:
        executeCommand(instance)

    if newSSH:
        startSSH(waitToStart(ec2client, instance.id))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true",
                   help='Verbose')
    parser.add_argument('-c','--command', default=command,
                    help="Command to run against ec2")
    parser.add_argument('-i','--instanceID',
                    help="Instance ID")
    parser.add_argument('-l','--launchTemplate',
                    help="Create new isntance based off of a Launch Template")
    parser.add_argument('-s', '--ssh', action="store_true",
                   help='Launch and open new SSH session')
    parser.add_argument('-u','--userID', default=username,
                    help="username to SSH as")

    args = parser.parse_args()

    verbose = args.verbose
    command = args.command
    ID = args.instanceID
    username = args.userID
    newSSH = args.ssh
    launchTemplate = args.launchTemplate
    
    main()