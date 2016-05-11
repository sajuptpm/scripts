#!/usr/bin/env python

import time
import netaddr
import unittest
import threading
import settings
from common import client
from common import vpc_manager

class PerformanceTest(unittest.TestCase):

    def setUp(self):
        self.jclient = client.Client()
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.vpc_manager.delete_all_vpcs(force=True)

    def test_performance(self):
        cidr_block = '12.0.0.0/16'
        net = netaddr.IPNetwork(cidr_block)
        thread_list = []
        start_time = time.time()
        for _cidr_block in list(net.subnet(28))[:settings.VPC_QUOTA]:
            t = threading.Thread(target=self.jclient.vpc.create_vpc, kwargs={'cidr_block':str(_cidr_block)})
            t.start()
            thread_list.append(t)
        for tr in thread_list:
            tr.join()
	end_time = time.time() - start_time
	print "Time (in seconds) taken to create {num} VPCs: {time_taken}".format(num=settings.VPC_QUOTA, time_taken=end_time)

    def tearDown(self):
        self.vpc_manager.delete_all_vpcs()

if __name__ == '__main__':
    unittest.main(verbosity=2)


