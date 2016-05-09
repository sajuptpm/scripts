from jcsclient import clilib
import unittest
import time

### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

# Test cases:
# 1. Associate an IP with already running instance.
# 2. Try to release already associated that IP. Try to associate already associated IP to another instance.
# 3. Terminate Instance. Try to re-associate formerly associated RJIL IP to another instance.
# 4. Terminate Instance. Try to release formerly associated RJIL IP.
# 5. Terminate Instance. Do a describe-addresses


class AddressTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print 'calling setUP methode'
        self.vpcId =  clilib.request('vpc','create-vpc', cidr_block='172.0.0.0/16')['content']['CreateVpcResponse']['vpc']['vpcId']
        self.subnetId = clilib.request('vpc','create-subnet', cidr_block='172.0.0.0/24', vpc_id=self.vpcId)['content']['CreateSubnetResponse']['subnet']['subnetId']
        self.securityGroupId = clilib.request('vpc','create-security-group', group_name='TestSecurity', vpc_id=self.vpcId, description='Something something')['content']['CreateSecurityGroupResponse']['groupId']
        images = clilib.request('compute','describe-images')['content']['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = clilib.request('compute','run-instances',subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.instance1 = resp['content']['RunInstancesResponse']['instancesSet']['item']['instanceId']
        resp = clilib.request('compute','run-instances',subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.instance2 = resp['content']['RunInstancesResponse']['instancesSet']['item']['instanceId']
        self.alloc1=''
        self.assoc1=''


    @classmethod
    def tearDownClass(self):
        print 'calling tearDown'
        clilib.request('vpc','describe-addresses')
        clilib.request('vpc','delete-security-group',group_id=self.securityGroupId)
        clilib.request('vpc','delete-subnet',subnet_id=self.subnetId)
        clilib.request('vpc','delete-vpc',vpc_id=self.vpcId)

    def test_1_allocate_address(self):
        print "Calling test 1"
        resp = clilib.request('vpc','allocate-address', domain='vpc')
        self.assertEqual(200, resp['status'])
        self.__class__.alloc1 = resp['content']['AllocateAddressResponse']['allocationId']
        resp = clilib.request('vpc','associate-address', instance_id=self.instance1, allocation_id=self.__class__.alloc1) 
        self.assertEqual(200, resp['status'])
        self.__class__.assoc1 = resp['content']['AssociateAddressResponse']['associationId']

        
    def test_2_wrongly_disassociate_release_address(self):
        print "calling test 2"
        resp = clilib.request('vpc','release-address',allocation_id=self.__class__.alloc1)
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','associate-address', instance_id=self.instance2, allocation_id=self.__class__.alloc1 )
        self.assertEqual(400, resp['status'])

    def test_3_associate_terminated_instace_address(self):
        print "Calling test 3"
        resp = clilib.request('compute','terminate-instances',instance_ids=self.instance1)
        self.assertEqual(200, resp['status'])
        print resp
        time.sleep (1)
        resp = clilib.request('vpc','associate-address', instance_id=self.instance2, allocation_id=self.__class__.alloc1)
        print resp
        self.assertEqual(200, resp['status'])
        self.__class__.assoc1 = resp['content']['AssociateAddressResponse']['associationId']

    def test_4_release_terminated_instance_address(self):
        print "calling test 4"
        resp = clilib.request('compute','terminate-instances',instance_ids=self.instance2)
        print resp
        self.assertEqual(200, resp['status'])
        time.sleep(1)
        resp = clilib.request('vpc','release-address',allocation_id=self.__class__.alloc1)
        print resp
        self.assertEqual(200, resp['status'])


#    def test5():


                  

if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    #add = Address()
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(AddressTest)
    unittest.TextTestRunner(verbosity=2).run(suite)    
