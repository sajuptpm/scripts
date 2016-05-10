#!/usr/bin/env python

from common import client
from common import vpc_manager
from common import subnet_manager
from common import address_manager
from common import security_group_manager
from common import instance_manager
import unittest
import netaddr
import settings

class VpcQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def test_vpc_quota(self):
        cidr_block = '11.0.0.0/16'
        net = netaddr.IPNetwork(cidr_block)
        for vpc_cidr in list(net.subnet(28))[:settings.VPC_QUOTA+1]:
            res = self.jclient.vpc.create_vpc(cidr_block=str(vpc_cidr))
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "VpcLimitExceeded")
                return
        self.fail("Could not find expected exception VpcLimitExceeded")

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs()

class SubnetQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)
        self.vpc_id = None

    def test_subnet_quota(self):
        cidr_block = '12.0.0.0/16'
        self.vpc_id = self.vpc_manager.create_vpc(cidr_block)
        net = netaddr.IPNetwork(cidr_block)
        for subnet_cidr in list(net.subnet(28))[:settings.SUBNET_QUOTA+1]:
            res = self.jclient.vpc.create_subnet(vpc_id=self.vpc_id, cidr_block=str(subnet_cidr))
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "SubnetLimitExceeded")
                return
        self.fail("Could not find expected exception SubnetLimitExceeded")

    def tearDown(self):
        self.subnet_manager.delete_all_subnets(self.vpc_id)

class AddressQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.address_manager = address_manager.AddressManager(self.jclient)

    def test_address_quota(self):
        for x in range(settings.ADDRESS_QUOTA+1):
            res = self.jclient.vpc.allocate_address(domain='vpc')
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "AddressLimitExceeded")
                return
        self.fail("Could not find expected exception AddressLimitExceeded")
 
    def tearDown(self):
        self.address_manager.delete_all_addresses()

class SecurityGroupQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def test_security_group_quota(self):
        cidr_block = '12.0.0.0/16'
        self.vpc_id = self.vpc_manager.create_vpc(cidr_block)
        for x in range(settings.SECURITY_GROUP_QUOTA+1):
            gname="test-{num}".format(num=str(x))
            res = self.jclient.vpc.create_security_group(vpc_id=self.vpc_id, group_name=gname, group_description=gname)
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "Forbidden")
                return
        self.fail("Could not find expected exception Forbidden")

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs(force=True)

class SecurityGroupRuleQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def test_security_group_rule_quota(self):
        cidr_block = '12.0.0.0/16'
        self.vpc_id = self.vpc_manager.create_vpc(cidr_block)
        group_name = "test_group"
        self.group_id = self.security_group_manager.create_security_group(self.vpc_id, group_name, group_name)
        for x in range(settings.SECURITY_GROUP_RULE_QUOTA+1):
            ip_permissions = '[{"IpProtocol": "icmp", "FromPort": %s, "ToPort": 81, "IpRanges":[{"CidrIp": "0.0.0.0/0"}]}]' %(x)
            res = self.jclient.vpc.authorize_security_group_ingress(group_id=self.group_id, ip_permissions=ip_permissions)
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "RulesPerSecurityGroupLimitExceeded")
                return
        self.fail("Could not find expected exception RulesPerSecurityGroupLimitExceeded")

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs(force=True)

class InstanceQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.instance_manager = instance_manager.InstanceManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def test_instance_quota(self):
        vpc_cidr = '12.0.0.0/16'
        subnet_cidr = '12.0.0.0/24'
        self.vpc_id = self.vpc_manager.create_vpc(vpc_cidr)
        self.subnet_id = self.subnet_manager.create_subnet(self.vpc_id, subnet_cidr)
        for x in range(settings.INSTANCE_QUOTA+1):
            res = self.jclient.compute.run_instances(image_id=settings.IMAGE_ID, instance_type_id=settings.INSTANCE_TYPE,\
                        subnet_id=self.subnet_id, key_name=settings.KEYPAIR_NAME) 
            if res.get("Response"):
                self.assertEqual(res['Response']['Errors']['Error']['Code'],  "Forbidden")
                return
        self.fail("Could not find expected exception Forbidden")

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs(force=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)

