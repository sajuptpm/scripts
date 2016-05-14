import time
import logging
import netaddr
import simplejson as json
import threading
import client
import utils
import vpc_manager
import subnet_manager
import address_manager
import security_group_manager
import instance_manager

class BaseTest(object):

    def __init__(self, jclient, config):
        self.jclient = jclient
        self.config = config
        log_file_name = config.get("name")+".log"
        print "---log_file_name----", log_file_name
        log_format = '%(levelname)s %(asctime)s [%(filename)s %(funcName)s %(lineno)d] [Pid %(process)d, Thread %(thread)d]: %(message)s'
        logging.basicConfig(filename=log_file_name,
                        level=logging.INFO,
                        format=log_format)
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.address_manager = address_manager.AddressManager(self.jclient)

        self.vpc_id = None
        self.vpc_cidr = "11.0.0.0/16"
        self.subnet_id = None
        self.security_group_id = None
        self.address_allocation_id = None
        self.address_association_id = None
        self.image_id = self.get_image_id(self.config)
        self.instance_type_id = self.get_instance_type_id(self.config)
        self.route_table_id = None
        self.route_table_association_id = None
        self.instance_id = None
        self.INSTANCE_WAIT_TIME = 20

    def get_image_id(self, config):
        return config.get("image_id")

    def get_instance_type_id(self, config):
        return config.get("instance_type_id")

    def get_status_code(self, resp):
        return resp.get("Status") == 200

    def run(self):
        self.clear_all_resources()
        self.test_cases()
        self.clear_all_resources()

    def test_cases(self):
        raise Exception("not implemented")

    def create_vpc(self):
        resp = self.jclient.vpc.create_vpc(cidr_block=self.vpc_cidr)
        if self.get_status_code(resp):
            self.vpc_id = utils.get_item(('CreateVpcResponse', 'vpc', 'vpcId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def create_subnet(self):
        if not self.vpc_id:
            logging.error(msg="vpc_id is None")
            return
        net = netaddr.IPNetwork(self.vpc_cidr)
        subnet_cidr = list(net.subnet(28))[0]
        resp = self.jclient.vpc.create_subnet(vpc_id=self.vpc_id, cidr_block=str(subnet_cidr))
        if self.get_status_code(resp):
            self.subnet_id = utils.get_item(('CreateSubnetResponse', 'subnet', 'subnetId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def create_security_group(self):
        if not self.vpc_id:
            logging.error(msg="vpc_id is None")
            return
        else:
            name = "test_group_{vpc_id}".format(vpc_id=self.vpc_id)
            description = name
            resp = self.jclient.vpc.create_security_group(vpc_id=self.vpc_id, group_name=name, group_description=description)
            if self.get_status_code(resp):
                self.security_group_id = utils.get_item(('CreateSecurityGroupResponse', 'groupId'), resp)
                logging.info(resp)
            else:
                logging.error(resp)
 
    def create_ingress_rule(self):
        if not self.security_group_id:
            logging.error(msg="security_group_id is None")
            return
        else:
            ip_permissions = '[{"IpProtocol": "icmp", "FromPort": 80, "ToPort": 81, "IpRanges":[{"CidrIp": "0.0.0.0/0"}]}]'
            resp = self.jclient.vpc.authorize_security_group_ingress(group_id=self.security_group_id, ip_permissions=ip_permissions)
            if not self.get_status_code(resp):
                logging.error(resp)
            else:
                logging.info(resp)

    def allocate_address(self):
        resp = self.jclient.vpc.allocate_address(domain='vpc')
        if self.get_status_code(resp):
            self.address_allocation_id = utils.get_item(('AllocateAddressResponse', 'allocationId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def check_instance_state(self):
        resp = self.jclient.compute.describe_instances(instance_ids=self.instance_id)
        start_time = time.time()
        while True:
            state = utils.get_item(('DescribeInstancesResponse', 'instancesSet', 'item', 'instanceState', 'name'), resp)
            if state in ['running']:
                return
            if (time.time() - start_time) >= self.INSTANCE_WAIT_TIME:
                return

    def run_instance(self):
        if not self.subnet_id:
            logging.error(msg="subnet_id is None")
            return
        elif not self.image_id:
            logging.error(msg="image_id is None")
            return
        elif not self.instance_type_id:
            logging.error(msg="instance_type_id is None")
            return
        resp = self.jclient.compute.run_instances(subnet_id=self.subnet_id, image_id=self.image_id, instance_type_id=self.instance_type_id)
        if self.get_status_code(resp):
            self.instance_id = utils.get_item(('RunInstancesResponse', 'instancesSet', 'item', 'instanceId'), resp)
            logging.info(resp)
            self.check_instance_state()
        else:
            logging.error(resp)

    def associate_address(self):
        if not self.address_allocation_id:
            logging.error(msg="allocation_id is None")
            return
        if not self.instance_id:
            logging.error(msg="instance_id is None")
            return
        resp = self.jclient.vpc.associate_address(allocation_id=self.address_allocation_id, instance_id=self.instance_id)
        if self.get_status_code(resp):
            self.address_association_id = utils.get_item(('AssociateAddressResponse', 'associationId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def disassociate_address(self):
        if not self.address_association_id:
            logging.error(msg="address_association_id is None")
            return
        resp = self.jclient.vpc.disassociate_address(association_id=self.address_association_id)
        if not self.get_status_code(resp):
            logging.error(resp)
        else:
            logging.info(resp)

    def release_address(self):
        if not self.address_allocation_id:
            logging.error(msg="allocation_id is None")
            return
        resp = self.jclient.vpc.release_address(allocation_id=self.address_allocation_id)
        if not self.get_status_code(resp):
            logging.error(resp)
        else:
            logging.info(resp)

    def create_route_table(self):
        if not self.vpc_id:
            logging.error(msg="vpc_id is None")
            return
        resp = self.jclient.vpc.create_route_table(vpc_id=self.vpc_id)
        if self.get_status_code(resp):
            self.route_table_id = utils.get_item(('CreateRouteTableResponse', 'routeTable', 'routeTableId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def add_route(self):
        if not self.instance_id:
            logging.error(msg="instance_id is None")
            return
        if not self.route_table_id:
            logging.error(msg="route_table_id is None")
            return
        resp = self.jclient.vpc.create_route(instance_id=self.instance_id, route_table_id=self.route_table_id, destination_cidr_block="10.0.0.0/24")
        if not self.get_status_code(resp):
            logging.error(resp)
        else:
            logging.info(resp)    

    def associate_route_table(self):
        if not self.subnet_id:
            logging.error(msg="subnet_id is None")
            return
        if not self.route_table_id:
            logging.error(msg="route_table_id is None")
            return
        resp = self.jclient.vpc.associate_route_table(route_table_id=self.route_table_id, subnet_id=self.subnet_id)
        if self.get_status_code(resp):
            self.route_table_association_id = utils.get_item(('AssociateRouteTableResponse', 'associationId'), resp)
            logging.info(resp)
        else:
            logging.error(resp)

    def disassociate_route_table(self):
        if not self.route_table_association_id:
            logging.error(msg="route_table_association_id is None")
            return
        resp = self.jclient.vpc.disassociate_route_table(association_id=self.route_table_association_id)
        if not self.get_status_code(resp):
            logging.error(resp)
        else:
            logging.info(resp)    
    
    def delete_route_table(self):
        if not self.route_table_id:
            logging.error(msg="route_table_id is None")
            return
        resp = self.jclient.vpc.delete_route_table(route_table_id=self.route_table_id)
        if not self.get_status_code(resp):
            logging.error(resp)
        else:
            logging.info(resp)

    def clear_all_resources(self):
        self.vpc_manager.delete_all_vpcs(force=True)
        self.address_manager.delete_all_addresses()

class LoadTestSuit(BaseTest):

    def __init__(self, client, config):
        super(LoadTestSuit, self).__init__(client, config)

    def test_cases(self):
        self.create_vpc()
        self.create_subnet()
        self.create_security_group()
        self.create_ingress_rule()
        self.run_instance()
        self.create_route_table()
        self.add_route()
        self.associate_route_table()
        self.allocate_address()
        self.associate_address()

        self.disassociate_route_table()
        self.delete_route_table()

        self.disassociate_address()
        self.release_address()


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




