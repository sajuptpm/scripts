from jcsclient import clilib
import unittest

### Usage info
### Make sure you have sorced openrc and
### you have jcsclient installed before 
### starting this script

class VpcTest(unittest.TestCase):
    def test_linklocal_cidr(self):
        print "test link local"
        resp = clilib.request('vpc','create-vpc', cidr_block='169.254.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='169.254.0.0/24')
        self.assertEqual(400, resp['status'])

    def test_loopback_cidr(self):
        print "test loopback ip"
        resp = clilib.request('vpc','create-vpc', cidr_block='127.0.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='127.0.0.0/8')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='127.0.0.0/25')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='127.0.0.0/29')
        self.assertEqual(400, resp['status'])
        
    def test_reserveip_cidr(self):
        print "0.x.x.x test"
        resp = clilib.request('vpc','create-vpc', cidr_block='0.0.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='0.1.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='0.0.0.0/8')
        self.assertEqual(400, resp['status'])

    def test_class_C_D_cidr(self):
        print "Class C & D test"
        resp = clilib.request('vpc','create-vpc', cidr_block='224.0.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='225.0.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='224.0.0.0/8')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='240.0.0.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='245.0.0.0/16')
        self.assertEqual(400, resp['status'])

    def test_wrong_cidr(self):
        print "Wrong cidr"
        resp = clilib.request('vpc','create-vpc', cidr_block='10.0.0.1/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='10.0.1.1/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='10.0.1.0/16')
        self.assertEqual(400, resp['status'])
        resp = clilib.request('vpc','create-vpc', cidr_block='172.168.0.1/16')
        self.assertEqual(400, resp['status'])

    def test_correct_cidr(self):
        print "correct cidr"
        resp = clilib.request('vpc','create-vpc', cidr_block='169.253.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)
        resp = clilib.request('vpc','create-vpc', cidr_block='169.255.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)
        resp = clilib.request('vpc','create-vpc', cidr_block='128.0.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)
        resp = clilib.request('vpc','create-vpc', cidr_block='10.0.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)
        resp = clilib.request('vpc','create-vpc', cidr_block='1.0.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)
        resp = clilib.request('vpc','create-vpc', cidr_block='223.0.0.0/24')
        self.assertEqual(200, resp['status'])
        vpcId= resp['content']['CreateVpcResponse']['vpc']['vpcId']
	clilib.request('vpc','delete-vpc',vpc_id=vpcId)

if __name__ == '__main__':
    #LOG.info('Initiating test cases: ')
    #add = Address()
    unittest.main()

