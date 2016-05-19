import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import netaddr
import simplejson as json
import threading
import settings
from common import client
from common import utils
from common import vpc_manager
from common import subnet_manager
from common import address_manager
from common import security_group_manager
from common import security_group_rule_manager
from common import instance_manager
from common import route_table_manager

class BaseTest(object):

    def __init__(self, jclient, config):
        self.jclient = jclient
        self.config = config
        log_file_name = config.get("name")+".log"
        self.logger = utils.initialize_logger(log_file_name)
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.address_manager = address_manager.AddressManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.security_group_rule_manager = security_group_rule_manager.SecurityGroupRuleManager(self.jclient)
        self.route_table_manager = route_table_manager.RouteTableManager(self.jclient)
        self.vpc_cidrs = []
        self.image_id = self.get_image_id(self.config)
        self.instance_type_id = self.get_instance_type_id(self.config)

    def get_image_id(self, config):
        return config.get("image_id")

    def get_instance_type_id(self, config):
        return config.get("instance_type_id")

    def run(self):
        self.test_cases()

    def test_cases(self):
        raise Exception("not implemented")

    def clear_all_resources(self):
        self.vpc_manager.delete_all_vpcs(force=True, logger=self.logger)
        self.address_manager.delete_all_addresses(logger=self.logger)

class LoadTestSuit(BaseTest):

    def __init__(self, client, config):
        super(LoadTestSuit, self).__init__(client, config)
        self.vpc_cidrs = ["10.0.0.0/16", "11.0.0.0/16", "12.0.0.0/16", "13.0.0.0/16", "14.0.0.0/16"]

    def test_address_operations(self):
        for x in range(settings.ADDRESS_QUOTA):
            address_allocation_id = self.address_manager.allocate_address(logger=self.logger)
            if address_allocation_id:
                self.address_manager.describe_addresses(address_allocation_id, logger=self.logger)
                self.address_manager.release_address(address_allocation_id, logger=self.logger)

    def test_security_group_operations(self, vpc_id):
        for x in range(settings.SECURITY_GROUP_QUOTA):
            gname="test-{num}".format(num=str(x))
            security_group_id = self.security_group_manager.create_security_group(vpc_id, gname, gname, logger=self.logger)
            if security_group_id:
                self.security_group_manager.describe_security_groups(group_ids=security_group_id, logger=self.logger)
                self.security_group_rule_manager.create_ingress_rule(security_group_id, logger=self.logger)
                self.security_group_manager.delete_security_group(security_group_id, logger=self.logger)

    def test_route_table_operations(self, vpc_id, subnet_id):
        route_table_id = self.route_table_manager.create_route_table(vpc_id, logger=self.logger)
        if route_table_id:
            self.route_table_manager.describe_route_tables(route_table_ids=route_table_id, logger=self.logger)
            route_table_association_id = self.route_table_manager.associate_route_table(subnet_id, route_table_id, logger=self.logger)
            if route_table_association_id:
                self.route_table_manager.disassociate_route_table(route_table_association_id, logger=self.logger)
            self.route_table_manager.delete_route_table(route_table_id, logger=self.logger)

    def test_vpc_operations(self, vpc_cidr):
        vpc_id = self.vpc_manager.create_vpc(vpc_cidr, logger=self.logger)
        print "=======vpc_id========", vpc_id
        if vpc_id:
            self.vpc_manager.describe_vpcs(vpc_ids=vpc_id, logger=self.logger)
            thread_list = []

            ##SecurityGroup Ops thread
            secg_td = threading.Thread(target=self.test_security_group_operations, args=(vpc_id,))
            secg_td.start()
            thread_list.append(secg_td)

            net = netaddr.IPNetwork(vpc_cidr)
            for subnet_cidr in list(net.subnet(28))[:settings.SUBNET_QUOTA]:
                subnet_id = self.subnet_manager.create_subnet(vpc_id, str(subnet_cidr), logger=self.logger)
                if subnet_id:
                    self.subnet_manager.describe_subnets(subnet_ids=subnet_id, logger=self.logger)
                    ##RouteTable Ops thread
                    rtb_td = threading.Thread(target=self.test_route_table_operations, args=(vpc_id, subnet_id))
                    rtb_td.start()
                    thread_list.append(rtb_td)

            for tr in thread_list:
                tr.join()

    def test_cases(self):
        for x in range(5):
            print "===Start==="
            self.clear_all_resources()
            #continue
            thread_list = []

            ##Address Ops thread
            addr_td = threading.Thread(target=self.test_address_operations)
            addr_td.start()
            thread_list.append(addr_td) 

            ##VPC Ops thread
            for vpc_cidr in self.vpc_cidrs:
                vpc_td = threading.Thread(target=self.test_vpc_operations, args=(vpc_cidr,))
                vpc_td.start()
                thread_list.append(vpc_td)

            for tr in thread_list:
                tr.join()
            print "===End==="

class TestRunner(object):

    def __init__(self, test_suit_class, config_file=None):
        self.test_suit_class = test_suit_class 
        self.config_file = config_file
        self.config = None
        self.accounts = []
        self.parse_cred_file()        

    def parse_cred_file(self):
        with open(self.config_file) as config_file:
            self.config = json.load(config_file)
        if self.config:
            self.accounts = self.config['accounts']

    def run_test(self):
        thread_list = []
        for account in self.accounts:
            if account.get("enabled"):
                jclient = client.Client(access_key=account['access_key'], secret_key=account['secret_key'])
                test_suit = self.test_suit_class(jclient, account)
                t = threading.Thread(target=test_suit.run)
                t.start()
                thread_list.append(t)
        for tr in thread_list:
            tr.join()


test_runner = TestRunner(LoadTestSuit, config_file="config.json")
test_runner.run_test()




