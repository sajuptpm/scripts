import base_manager
import utils

class SubnetManager(base_manager.BaseManager):

    def create_subnet(self, vpc_id, cidr_block, logger=None):
        resp = self.jclient.vpc.create_subnet(vpc_id=vpc_id, cidr_block=cidr_block)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('CreateSubnetResponse', 'subnet', 'subnetId'), resp)
        else:
            logger and logger.error(resp)

    def describe_subnets(self, subnet_ids=None, logger=None):
        resp = self.jclient.vpc.describe_subnets(subnet_ids=subnet_ids)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def delete_subnet(self, subnet_id, logger=None):
        resp = self.jclient.vpc.delete_subnet(subnet_id=subnet_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def get_all_subnet_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.vpc.describe_subnets()
        items = utils.get_item(('DescribeSubnetsResponse', 'subnetSet', 'item'), res)
        if isinstance(items, list):
            return [item['subnetId'] for item in items if item.get('vpcId')==vpc_id]
        elif isinstance(items, dict):
            if items['vpcId'] == vpc_id:
                return [items['subnetId']]
        return ids

    def delete_all_subnets(self, vpc_id, logger=None):
        subnet_ids = self.get_all_subnet_ids(vpc_id)
        logger and logger.info("......Cleaning Subnets: {num}".format(num=len(subnet_ids)))
        for subnet_id in subnet_ids:
            resp = self.jclient.vpc.delete_subnet(subnet_id=subnet_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)

