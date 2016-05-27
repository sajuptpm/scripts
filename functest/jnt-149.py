from jcsclient import client
from jcsclient import clilib
import unittest
import logging
### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script
#   Test Cases
#   1. Allocate 2 Rjil IP
#   2. Create 2 new instances instance1 and instace2. Associate 1st IP to insatnce1
#   3. Associate 2nd IP to insatnce1
#   4. Associate 1st IP to insatnce2
#   5. Associate 2nd IP to insatnce2
#   6. Disassociate 1st ip from instance1 and the Associate to insatnce2
#   7. Associate 1st ip to instance1 and terminate the instance1
#   8. Disassociate 2nd ip from instance2
#   9. Associate 1st ip to instance2
#   10.Associate 2nd ip to instance2 


class AddressTest(unittest.TestCase):

    def __init__(self,*args, **kargs) : #access=None,secret=None,vpc_url = None, compute_url=None):
        super(AddressTest,self).__init__(*args, **kargs)
        self.jclient = client.Client()#access_key = access, secret_key = secret, vpc_url = vpc_url , compute_url = compute_url )

    @classmethod
    def setUpClass(self):

        self.jclient = client.Client()#access_key = access, secret_key = secret, vpc_url = vpc_url , compute_url = compute_url )
        LOG_FILENAME = 'address_test.log'
        logging.basicConfig(filename=LOG_FILENAME, 
                        level=logging.INFO,
                        )

        logging.info( "Calling setup")
        self.instanceId = None
        self.allocateAddressId1 = None
        self.allocateAddressId2 = None
        self.associateAddressId1 = None
        self.associateAddressId2 = None

        resp = self.jclient.vpc.create_vpc(cidr_block='192.168.0.0/24')
        logging.info(resp)

        self.vpcId = resp['CreateVpcResponse']['vpc']['vpcId']

        if self.vpcId:
            resp = self.jclient.vpc.create_subnet(vpc_id = self.vpcId, cidr_block='192.168.0.64/26')
            logging.info(resp)
            self.subnetId = resp['CreateSubnetResponse']['subnet']['subnetId']
        else:
            self.fail('Vpc not created')
        
        images = self.jclient.compute.describe_images()['DescribeImagesResponse']['imagesSet']['item']
        for image in images:
            if image['name'] == "Ubuntu 14.04":
                imageId = image['imageId']
        resp = self.jclient.compute.run_instances(subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.instanceId1 = resp['RunInstancesResponse']['instancesSet']['item']['instanceId']
        resp = self.jclient.compute.run_instances(subnet_id=self.subnetId, image_id = imageId , instance_type_id = 'c1.small')
        self.instanceId2 = resp['RunInstancesResponse']['instancesSet']['item']['instanceId']

    def test_allocate_address1(self):
        resp = self.jclient.vpc.allocate_address(domain='vpc')
        logging.info(resp)
        self.assertEqual(200, resp['status'])
        self.__class__.allocateAddressId1 = resp['AllocateAddressResponse']['allocationId']


    def test_allocate_address2(self):
        resp = self.jclient.vpc.allocate_address(domain='vpc')
        logging.info(resp)
        self.assertEqual(200, resp['status'])
        self.__class__.allocateAddressId2 = resp['AllocateAddressResponse']['allocationId']

    def test_associate_address1_instance1(self):
        if self.__class__.allocateAddressId1 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId1 , instance_id = self.__class__.instanceId1 )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.associateAddressId1 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address1 not allcoated')


    def test_associate_address2_instance1(self):
        if self.__class__.allocateAddressId2 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId2 , instance_id = self.__class__.instanceId1 )
            logging.info(resp)
            self.assertEqual(400, resp['status'])
#            self.__class__.associateAddressId1 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address2 not allcoated')

    def test_associate_address1_instance2(self):
        if self.__class__.allocateAddressId1 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId1 , instance_id = self.__class__.instanceId2 )
            logging.info(resp)
            self.assertEqual(400, resp['status'])
#            self.__class__.associateAddressId1 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address1 not allcoated')

    def test_associate_address2_instance2(self):
        if self.__class__.allocateAddressId2 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId2 , instance_id = self.__class__.instanceId2 )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.associateAddressId2 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address1 not allcoated')

#when address1 is deassociated
    def test_Disassociate_address1_then_associate_to_instance2(self):
        if self.__class__.allocateAddressId1 :
            resp = self.jclient.vpc.disassociate_address(association_id = self.__class__.associateAddressId1 )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId1 , instance_id = self.__class__.instanceId2 )
            logging.info(resp)
            self.assertEqual(400, resp['status'])
#            self.__class__.associateAddressId1 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address1 not allcoated')

    def test_disaccociate_address2_from_instance2(self):
        if self.associateAddressId1 :
            resp = self.jclient.vpc.disassociate_address(association_id = self.associateAddressId1 )
            self.assertEqual(200, resp['status'])
            logging.info(resp)
        else:
            self.fail('Address1 not associated')

    def test_terminate_instance1(self):
        if self.instanceId1 :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.instanceId1)
            self.assertEqual(200, resp['status'])
            logging.info(resp)
        else:
            self.fail('Instance not created')


    def test_associate_address1_instance2_after_terminate_instance1(self):
        if self.__class__.allocateAddressId1 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId1 , instance_id = self.__class__.instanceId2 )
            logging.info(resp)
            self.assertEqual(200, resp['status'])
            self.__class__.associateAddressId1 = resp['AssociateAddressResponse']['associationId']
        else:
            self.fail('Address1 not allcoated')

    def test_associate_address2_instance2_after_terminate_instance1(self):
        if self.__class__.allocateAddressId2 :
            resp = self.jclient.vpc.associate_address(allocation_id= self.__class__.allocateAddressId2 , instance_id = self.__class__.instanceId1 )
            logging.info(resp)
            self.assertEqual(400, resp['status'])
        else:
            self.fail('Address1 not allcoated')


    @classmethod
    def tearDownClass(self):
        logging.info( "Calling teardown")
        '''
        if self.instanceId1 :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.instanceId1)
            logging.info(resp)
        else:
            self.fail('Instance not created')
        '''
        if self.instanceId2 :
            resp = self.jclient.compute.terminate_instances(instance_ids=self.instanceId2)
            logging.info(resp)
        else:
            self.fail('Instance not created')

        if self.associateAddressId1 :
            resp = self.jclient.vpc.disassociate_address(association_id = self.associateAddressId1 )
            logging.info(resp)
        else:
            self.fail('Address1 not associated')

        if self.associateAddressId2 :
            resp = self.jclient.vpc.disassociate_address(association_id = self.associateAddressId2 )
            logging.info(resp)
        else:
            self.fail('Address2 not associated')

        if self.allocateAddressId1 :
            resp = self.jclient.vpc.release_address(allocation_id= self.allocateAddressId1)
            logging.info(resp)
        else:
            self.fail('Address1 not allcoated')

        if self.allocateAddressId2 :
            resp = self.jclient.vpc.release_address(allocation_id= self.allocateAddressId2)
            logging.info(resp)
        else:
            self.fail('Address2 not allcoated')

        if self.__class__.subnetId :
            resp = self.jclient.vpc.delete_subnet(subnet_id=self.subnetId)
            logging.info(resp)
        else:
            self.fail('Subnet not created')

        if self.__class__.vpcId :
            resp = self.jclient.vpc.delete_vpc(vpc_id=self.vpcId)
            logging.info(resp)
        else:
            self.fail('VPC not created')


if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    test = unittest.TestSuite()
    test.addTest(AddressTest("test_allocate_address1")) 
    test.addTest(AddressTest("test_allocate_address2"))    
    test.addTest(AddressTest("test_associate_address1_instance1"))
    test.addTest(AddressTest("test_associate_address2_instance1"))
    test.addTest(AddressTest("test_associate_address1_instance2"))
    test.addTest(AddressTest("test_associate_address2_instance2"))
    test.addTest(AddressTest("test_Disassociate_address1_then_associate_to_instance2"))
    test.addTest(AddressTest("test_associate_address1_instance1"))
    test.addTest(AddressTest("test_terminate_instance1"))
    test.addTest(AddressTest("test_associate_address1_instance2_after_terminate_instance1"))
    test.addTest(AddressTest("test_associate_address2_instance2_after_terminate_instance1"))
    unittest.TextTestRunner(verbosity=2).run(test)
