import base_manager
import utils

class AddressManager(base_manager.BaseManager):

    def get_all_address_ids(self):
        ids = []
        items = None
        res = self.jclient.vpc.describe_addresses()
        items = utils.get_item(('DescribeAddressesResponse', 'addressesSet', 'item'), res)
        if isinstance(items, list):
            #Bug:Sometimes allocationId key doesn't exist in item
            return [item['allocationId'] for item in items if item.get("allocationId")]
        elif isinstance(items, dict):
            return [items['allocationId']]
        return ids

    def delete_all_addresses(self):
        ids = self.get_all_address_ids()
        print "......Cleaning Addresses: ", len(ids)
        for _id in ids:
            self.jclient.vpc.release_address(allocation_id=_id)

