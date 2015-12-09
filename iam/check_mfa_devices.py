#!/usr/bin/env python

'''

Purpose : Add, Delete and List AWS access Key
Author : Falko Zurell
Email : falko.zurell@ubirch.com
Creation Date : 10/12/2015
'''


import boto
import argparse
import os

# Parameter parser

parser=argparse.ArgumentParser(description="Add,Delete or list AWS access key")
parser.add_argument("-u","--user", help="aws user name",required=True)
parser.add_argument("-a","--action", help="action to be performed",required=True,choices=['add', 'delete', 'list', 'mfa'])
parser.add_argument("-i","--id",help="access key id")
args=parser.parse_args()



class iaManage:
    def __init__(self,user):
        try:
            # fetch credentials from ./.boto
            boto_credentials = os.getcwd() + "/.boto"
            boto.config.load_credential_file(boto_credentials)
            self.iam_conn = boto.connect_iam()
        except Exception, e:
            print("connection error, Check your credentials")
            print e.message
            exit(0)
        self.user=user
        self.get_keys()
        self.get_mfa_status()

    def get_mfa_status(self):

        try:
            self.user_mfa = self.iam_conn.get_all_mfa_devices(self.user)
        except Exception, e:
            print "Error fetching MFA"
            print e.message
            exit(0)

        return self.user_mfa

    def get_keys(self):
        try:
            self.user_key_list=self.iam_conn.get_all_access_keys(self.user)
        except Exception, e:
            print("Failed to get the key(s)")
            exit(0)
        return self.user_key_list

    def display_mfa(self):

        print "-" * 80
        print("%-50s  %-10s %-32s"%("Serial Number","Username","Enable Date"))
        for i in self.user_mfa.list_mfa_devices_response.list_mfa_devices_result.mfa_devices:
            print("%-50s  %-10s %-32s"%(i.serial_number,i.user_name,i.enable_date))
        print "-" * 80


    def display(self):
        print "-" * 80
        print("%-12s%-10s%-32s%-s"%("User","Status","Creation Date","Key ID"))
        print "-" * 80
        for i in self.user_key_list.access_key_metadata:
            print("%-12s%-10s%-32s%-s"%(i.user_name,i.status,i.create_date,i.access_key_id))
        print "-" * 80

    def key_delete(self,key_id):
        if len(self.user_key_list.access_key_metadata)==0:
            print("Nothing to Delete !!!!")
            exit(0)
        try:
            self.iam_conn.delete_access_key(key_id,user_name=self.user)
        except Exception, e:
            print("Failed to delete")

    def key_add(self):
        if len(self.user_key_list.access_key_metadata)==2:
            print("Already 2 records exist for this user(AWS Limitation),Cannot add more")
            exit(0)
        try:
            response = self.iam_conn.create_access_key(self.user)
        except Exception, e:
            print("Failed to create access key, Make sure this user exist")
            exit(0)
        print "Access Id:%s" %(response.access_key_id)
        print "Access Key:%s" %(response.secret_access_key)


user=iaManage(args.user)
if args.action == "delete":
    if args.id:
        user.key_delete(args.id)
    else:
        print("Access key id missing, Please pass key id with -i option")
        exit(0)
if args.action == "add":
    user.key_add()
if args.action == "list":
    user.display()
if args.action == "mfa":
    user.display_mfa()