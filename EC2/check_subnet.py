from jcsclient import clilib
import unittest

### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

class VpcTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.vpcId =  clilib.request('vpc','create-vpc', cidr_block='174.0.0.0/16')['content']['CreateVpcResponse']['vpc']['vpcId']

    @classmethod
    def tearDownClass(self):
        clilib.request('vpc','delete-vpc',vpc_id=self.vpcId)

    def test_linklocal_cidr(self):
        print "test link local"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='169.254.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc', 'create-subnet', vpc_id=self.vpcId, cidr_block='169.254.0.0/24')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)


    def test_loopback_cidr(self):
        print "test loopback ip"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='127.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='127.0.0.0/17')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='127.0.0.0/25')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='127.0.0.0/17')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)


    def test_reserveip_cidr(self):
        print "0.x.x.x test"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='0.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:

           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='0.1.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='0.0.0.0/24')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)

    def test_class_C_D_cidr(self):
        print "Class C & D test"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='224.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='225.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='224.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='240.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='245.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)

    def test_wrong_cidr(self):
        print "Wrong cidr"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='10.0.0.1/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId = resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='10.0.1.1/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId = resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='10.0.1.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId = resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.0.1/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidNetworkId", Code)

    def test_correct_cidr(self):
        print "correct cidr"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.0.0/24')
        self.assertEqual(200, resp['status'])
        subnetId= resp['content']['CreateSubnetResponse']['subnet']['subnetId']
        clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.1.0/24')
        self.assertEqual(200, resp['status'])
        subnetId= resp['content']['CreateSubnetResponse']['subnet']['subnetId']
        clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.2.0/24')
        self.assertEqual(200, resp['status'])
        subnetId= resp['content']['CreateSubnetResponse']['subnet']['subnetId']
        clilib.request('vpc','delete-subnet',subnet_id=subnetId)

    def test_outside_vpc_range(self):
        print "ouside VPC range"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='11.0.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='173.0.0.0/24')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='10.0.1.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='192.168.0.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("OutOfVpcSubnet.Range", Code)

    def test_invalid_cidr_range(self):
        print "invalid cidr and invalid netmask"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='11.0.0.0')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidParameterValue", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='256.0.0.0/24')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidParameterValue", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='10.286.1.0/16')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidParameterValue", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='192.168.0.0/0')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='192.168.0.0/29')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidSubnet.Range", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='192.168.0.0/45')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidParameterValue", Code)
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='192.168.0.0/15')
        self.assertEqual(400, resp['status'])
        if resp['status'] == 200:
           subnetId=resp['content']['CreateSubnetResponse']['subnet']['subnetId']
           clilib.request('vpc','delete-subnet',subnet_id=subnetId)
        else:
           Code=resp['content']['Response']['Errors']['Error']['Code']
           self.assertEqual("InvalidSubnet.Range", Code)

    def test_Subnet_conflict(self):
        print "correct subnet conflict"
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.10.0/24')
        self.assertEqual(200, resp['status'])
        subnetId= resp['content']['CreateSubnetResponse']['subnet']['subnetId']
        resp = clilib.request('vpc','create-subnet', vpc_id=self.vpcId, cidr_block='174.0.10.0/24')
        self.assertEqual(400, resp['status'])
        Code=resp['content']['Response']['Errors']['Error']['Code']
        self.assertEqual("InvalidSubnet.Conflict", Code)
        clilib.request('vpc','delete-subnet',subnet_id=subnetId)

if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    #add = Address()
    unittest.main()

