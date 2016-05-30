import base_manager
import utils

class RouteTableManager(base_manager.BaseManager):

    def create_route_table(self, vpc_id, logger=None):
        resp = self.jclient.vpc.create_route_table(vpc_id=vpc_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('CreateRouteTableResponse', 'routeTable', 'routeTableId'), resp)
        else:
            logger and logger.error(resp)

    def describe_route_tables(self, route_table_ids=None, logger=None):
        resp = self.jclient.vpc.describe_route_tables(route_table_ids=route_table_ids)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def add_route(selfi, instance_id, route_table_id, destination_cidr_block, logger=None):
        resp = self.jclient.vpc.create_route(instance_id=instance_id, route_table_id=route_table_id, destination_cidr_block=destination_cidr_block)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def associate_route_table(self, subnet_id, route_table_id, logger=None):
        resp = self.jclient.vpc.associate_route_table(route_table_id=route_table_id, subnet_id=subnet_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('AssociateRouteTableResponse', 'associationId'), resp)
        else:
            logger and logger.error(resp)

    def disassociate_route_table(self, route_table_association_id, logger=None):
        resp = self.jclient.vpc.disassociate_route_table(association_id=route_table_association_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def delete_route_table(self, route_table_id, logger=None):
        resp = self.jclient.vpc.delete_route_table(route_table_id=route_table_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def get_all_route_table_ids_and_assoc_ids(self, vpc_id, include_main_route=False):
        route_table_ids = []
        assoc_ids = []
        res = self.jclient.vpc.describe_route_tables()
        items = utils.get_item(('DescribeRouteTablesResponse', 'routeTableSet', 'item'), res)
        if isinstance(items, list):
            for item in items:
                if item['vpcId']==vpc_id:
                    if utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), item):
                        if not include_main_route:
                            if not utils.get_item(('associationSet', 'item', 'main'), item):
                                assoc_ids.append(utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), item))
                                route_table_ids.append(item['routeTableId'])
                        else:
                            assoc_ids.append(utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), item))
                            route_table_ids.append(item['routeTableId'])
                    else:
                        route_table_ids.append(item['routeTableId'])
        elif isinstance(items, dict):
            if items['vpcId'] == vpc_id:
                if utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), items):
                    if not include_main_route:
                        if not utils.get_item(('associationSet', 'item', 'main'), items):
                            assoc_ids.append(utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), items))
                            route_table_ids.append(items['allocationId'])
                    else:
                        assoc_ids.append(utils.get_item(('associationSet', 'item', 'routeTableAssociationId'), items))
                else:
                    route_table_ids.append(items['allocationId'])
        return (route_table_ids, assoc_ids)

    def delete_all_route_tables(self, vpc_id, include_main_route=False, logger=None):
        route_table_ids, assoc_ids = self.get_all_route_table_ids_and_assoc_ids(vpc_id, include_main_route=include_main_route)
        logger and logger.info("......Disassociating Route Tables: {num}".format(num=len(assoc_ids)))
        for assoc_id in assoc_ids:
            resp = self.jclient.vpc.disassociate_route_table(association_id=assoc_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)
        logger and logger.info("......Deleting Route Tables: {num}".format(num=len(route_table_ids)))
        for route_table_id in route_table_ids:
            resp = self.jclient.vpc.delete_route_table(route_table_id=route_table_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)


