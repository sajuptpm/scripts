#!/usr/bin/env python

from common import client
from common import quota_manager
from common import utils
import netaddr
import unittest
import settings
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Quota Update UT')

class ShowQuotaCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.quota_manager = quota_manager.QuotaManager()
	
    def test_check_show_quota_api(self):
        #Deepak's Second Account-id - different from Account
        #for which Accees/Secret key is used to run this script
        account_id = '00000000000000000000860112177782'
	resp = self.quota_manager.show_vpc_all_resources_quota(account_id)
        #FIXME: once neutron side is fixed
        self.fail(resp)

    def tearDown(self):
	print "......Cleaning show_quota_api_test: "

class FloatingIpQuotaUpdateCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.quota_manager = quota_manager.QuotaManager()
	
    def test_check_fip_quota_update(self):
        #Deepak's Second Account-id - different from Account
        #for which Accees/Secret key is used to run this script
        account_id = '00000000000000000000860112177782'
	resp = self.quota_manager.update_vpc_resource_quota(
                                                 'floatingip',
                                                 4,
                                                 account_id)
        if resp.get('floatingip') == '4':
           log.info("Test: Floating-up Update: PASS");
           return
        else:
           log.error('Failed to update: FIP='+resp.get('floatingip'))
           self.fail(resp)

    def tearDown(self):
	print "...... Update quota back to default : "
        account_id = '00000000000000000000860112177782'
	resp = self.quota_manager.update_vpc_resource_quota(
                                                 'floatingip',
                                                 5,
                                                 account_id)
        if resp.get('floatingip') == '5':
           return
        else:
           print 'Failed to cleanup: FIP='+resp.get('floatingip')
           self.fail(resp)

class EniQuotaUpdateCheck(unittest.TestCase):
    def setUp(self):
        self.jclient = client.Client()
        self.quota_manager = quota_manager.QuotaManager()
	
    def test_check_eni_quota_update(self):
        #Deepak's Second Account-id - different from Account
        #for which Accees/Secret key is used to run this script
        account_id = '00000000000000000000860112177782'
	resp = self.quota_manager.update_vpc_resource_quota(
                                                 'port',
                                                 50,
                                                 account_id)
        if resp.get('port') == '50':
           log.info("Test: ENI Update: PASS");
           return
        else:
           log.error('Failed to update: ENI='+resp.get('port'))
           self.fail(resp)

    def tearDown(self):
	print "...... Update quota back to default : "
        account_id = '00000000000000000000860112177782'
	resp = self.quota_manager.update_vpc_resource_quota(
                                                 'port',
                                                 100,
                                                 account_id)
        if resp.get('port') == '100':
           return
        else:
           print 'Failed to cleanup: ENI='+resp.get('port')
           self.fail(resp)

if __name__ == '__main__':
    unittest.main()


