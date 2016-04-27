from jcsclient import clilib
import unittest

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
        clilib.request('vpc','delete-security-group',group_id=self.securityGroupId)
        clilib.request('vpc','delete-subnet',subnet_id=self.subnetId)
        clilib.request('vpc','delete-vpc',vpc_id=self.vpcId)

    def attach_address(self):
        print "Calling test 1"
        images = clilib.request('compute','describe-images')['content']['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = clilib.request('compute','run-instances',subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.assertEqual(200, resp['status'])
        self.instance1 = resp['content']['RunInstancesResponse']['instancesSet']['item']['instanceId']
        resp = clilib.request('vpc','allocate-address', domain='vpc')
        self.assertEqual(200, resp['status'])
        self.alloc1 = resp['content']['AllocateAddressResponse']['allocationId']
        resp = clilib.request('vpc','associate-address', instance_id=self.instance1, allocation_id=self.alloc1) 
        self.assertEqual(200, resp['status'])
        self.assoc1 = resp['content']['AssociateAddressResponse']['associationId']

        
    def wrongly_associate_release_address(self):
        print "calling test 2"
        images = clilib.request('compute','describe-images')['content']['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = clilib.request('compute','run-instances',subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.assertEqual(200, resp['status'])
        self.instance2 = resp['content']['RunInstancesResponse']['instancesSet']['item']['instanceId']

        resp = clilib.request('vpc','release-address',allocation_id=self.alloc1)
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','associate-address', instance_id=self.instance2, allocation_id=self.alloc1 )
        self.assertEqual(400, resp['status'])

    def associate_address_of_terminated_instance(self):
        print "Calling test 3"
        resp = clilib.request('compute','terminate-instances',instance_ids=self.instance1)
        self.assertEqual(200, resp['status'])
        resp = clilib.request('vpc','associate-address', instance_id=self.instance2, allocation_id=self.alloc1)
        self.assertEqual(200, resp['status'])
        self.assoc1 = resp['content']['AssociateAddressResponse']['associationId']

    def release_address_of_terminated_instance(self):
        print "calling test 4"
        resp = clilib.request('compute','terminate-instances',instance_ids=self.instance2)
        self.assertEqual(200, resp['status'])

        resp = clilib.request('vpc','release-address',allocation_id=self.alloc1)
        self.assertEqual(200, resp['status'])


#    def test5():


                  

if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    #add = Address()
    unittest.main()
    
