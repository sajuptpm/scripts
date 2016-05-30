import base_manager
import utils

class AddressManager(base_manager.BaseManager):

    def allocate_address(self, logger=None):
        resp = self.jclient.vpc.allocate_address(domain='vpc')
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('AllocateAddressResponse', 'allocationId'), resp)
        else:
            logger and logger.error(resp)

    def describe_addresses(self, address_allocation_ids, logger=None):
        resp = self.jclient.vpc.describe_addresses(allocation_ids=address_allocation_ids)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def associate_address(self, address_allocation_id, instance_id, logger=None):
        resp = self.jclient.vpc.associate_address(allocation_id=address_allocation_id, instance_id=instance_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('AssociateAddressResponse', 'associationId'), resp)
        else:
            logger and logger.error(resp)

    def disassociate_address(self, address_association_id, logger=None):
        resp = self.jclient.vpc.disassociate_address(association_id=address_association_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def release_address(self, address_allocation_id, logger=None):
        resp = self.jclient.vpc.release_address(allocation_id=address_allocation_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def get_all_address_alloc_and_assoc_ids(self):
        alloc_ids = []
        assoc_ids = []
        res = self.jclient.vpc.describe_addresses()
        items = utils.get_item(('DescribeAddressesResponse', 'addressesSet', 'item'), res)
        if isinstance(items, list):
            alloc_ids = [item['allocationId'] for item in items if item.get('allocationId')]
            assoc_ids = [item['associationId'] for item in items if item.get('associationId')]
        elif isinstance(items, dict):
            alloc_ids = [items.get('allocationId') and items['allocationId']]
            if items.get('associationId'):
                assoc_ids = [items['associationId']]
        return (alloc_ids, assoc_ids)

    def delete_all_addresses(self, logger=None):
        alloc_ids, assoc_ids = self.get_all_address_alloc_and_assoc_ids()
        logger and logger.info("......Cleaning Addresses: {num}".format(num=len(alloc_ids)))
        for assoc_id in assoc_ids:
            resp = self.jclient.vpc.disassociate_address(association_id=assoc_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)
        for alloc_id in alloc_ids:
            resp = self.jclient.vpc.release_address(allocation_id=alloc_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)

