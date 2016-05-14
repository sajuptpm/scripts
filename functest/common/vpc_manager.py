import base_manager
import generic_manager
import utils

class VpcManager(base_manager.BaseManager):

    def create_vpc(self, cidr_block):
        res = self.jclient.vpc.create_vpc(cidr_block=cidr_block)
        vpc_id = utils.get_item(('CreateVpcResponse', 'vpc', 'vpcId'), res)
        return vpc_id

    def get_all_vpc_ids(self):
        ids = []
        items = None
        res = self.jclient.vpc.describe_vpcs()
        items = utils.get_item(('DescribeVpcsResponse', 'vpcSet', 'item'), res)
        if isinstance(items, list):
            return [item['vpcId'] for item in items]
        elif isinstance(items, dict):
            return [items['vpcId']]
        return ids

    def delete_all_vpcs(self, force=False):
        ids = self.get_all_vpc_ids()
        print "......Cleaning VPCs: ", len(ids), ids
        for _id in ids:
            if force:
                gm = generic_manager.GenericManager(self.jclient)
                gm.delete_vpc(_id)
            else:
                self.jclient.vpc.delete_vpc(vpc_id=_id)

