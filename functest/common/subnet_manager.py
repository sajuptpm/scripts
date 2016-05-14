import base_manager
import utils

class SubnetManager(base_manager.BaseManager):

    def create_subnet(self, vpc_id, cidr_block):
        res = self.jclient.vpc.create_subnet(vpc_id=vpc_id, cidr_block=cidr_block)
        subnet_id = utils.get_item(('CreateSubnetResponse', 'subnet', 'subnetId'), res)
        return subnet_id

    def get_all_subnet_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.vpc.describe_subnets()
        items = utils.get_item(('DescribeSubnetsResponse', 'subnetSet', 'item'), res)
        if isinstance(items, list):
            return [item['subnetId'] for item in items if item.get('vpcId') == vpc_id]
        elif isinstance(items, dict):
            if items['vpcId'] == vpc_id:
                return [items['subnetId']]
        return ids

    def delete_all_subnets(self, vpc_id):
        ids = self.get_all_subnet_ids(vpc_id)
        print "......Cleaning Subnets: ", len(ids)
        for _id in ids:
            self.jclient.vpc.delete_subnet(subnet_id=_id)

