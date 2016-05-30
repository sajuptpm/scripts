import base_manager
import generic_manager
import utils

class VpcManager(base_manager.BaseManager):

    def create_vpc(self, cidr_block, logger=None):
        resp = self.jclient.vpc.create_vpc(cidr_block=cidr_block)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('CreateVpcResponse', 'vpc', 'vpcId'), resp)
        else:
            logger and logger.error(resp)

    def describe_vpcs(self, vpc_ids=None, logger=None):
        resp = self.jclient.vpc.describe_vpcs(vpc_ids=vpc_ids)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def delete_vpc(self, vpc_id, logger=None):
        resp = self.jclient.vpc.delete_vpc(vpc_id=vpc_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def get_all_vpc_ids(self, logger=None):
        ids = []
        items = None
        res = self.jclient.vpc.describe_vpcs()
        items = utils.get_item(('DescribeVpcsResponse', 'vpcSet', 'item'), res)
        logger and logger.info(items)
        if isinstance(items, list):
            return [item['vpcId'] for item in items]
        elif isinstance(items, dict):
            return [items['vpcId']]
        return ids

    def delete_all_vpcs(self, force=False, logger=None):
        vpc_ids = self.get_all_vpc_ids(logger=logger)
        logger and logger.info("......Cleaning VPCs: {num}".format(num=len(vpc_ids)))
        for vpc_id in vpc_ids:
            if force:
                gm = generic_manager.GenericManager(self.jclient)
                gm.delete_vpc(vpc_id, logger=logger)
            else:
                resp = self.jclient.vpc.delete_vpc(vpc_id=vpc_id)
                if utils.get_status_code(resp):
                    logger and logger.info(resp)
                else:
                    logger and logger.error(resp)

