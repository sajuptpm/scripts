import base_manager
import utils

class RouteTableManager(base_manager.BaseManager):

    def get_all_association_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.vpc.describe_route_tables()
        items = utils.get_item(('DescribeRouteTablesResponse', 'routeTableSet', 'item'), res)
        if isinstance(items, list):
           return [self._get_association_id(item) for item in items if item['vpcId']==vpc_id if self._get_association_id(item)]
        elif isinstance(items, dict):
            return [_id for _id in [self._get_association_id(items)] if _id]
        return ids

    def get_all_route_table_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.vpc.describe_route_tables()
        items = utils.get_item(('DescribeRouteTablesResponse', 'routeTableSet', 'item'), res)
        if isinstance(items, list):
            return [item['routeTableId'] for item in items if item['vpcId']==vpc_id]
        elif isinstance(items, dict):
            return [items['routeTableId']]
        return ids

    def delete_all_route_tables(self, vpc_id):
        ids = self.get_all_association_ids(vpc_id)
        print "......Disassociating Route Tables: ", len(ids)
        for _id in ids:
            self.jclient.vpc.disassociate_route_table(association_id=_id)
        ids = self.get_all_route_table_ids(vpc_id)
        print "......Cleaning Route Tables: ", len(ids)
        for _id in ids:
            self.jclient.vpc.delete_route_table(route_table_id=_id)            

    def _get_association_id(self, item):
        return utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), item)
        

