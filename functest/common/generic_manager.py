import utils
import base_manager
import vpc_manager
import subnet_manager
import address_manager
import security_group_manager
import instance_manager
import route_table_manager

class GenericManager(base_manager.BaseManager):

    def __init__(self, *args, **kwargs):
        super(GenericManager, self).__init__(*args, **kwargs)
        self.vpc_manager = vpc_manager.VpcManager(self.jclient)
        self.subnet_manager = subnet_manager.SubnetManager(self.jclient)
        self.address_manager = address_manager.AddressManager(self.jclient)
        self.security_group_manager = security_group_manager.SecurityGroupManager(self.jclient)
        self.instance_manager = instance_manager.InstanceManager(self.jclient)
        self.route_table_manager = route_table_manager.RouteTableManager(self.jclient)

    def delete_vpc(self, vpc_id, force=False, logger=None):
        self.instance_manager.delete_all_instances(vpc_id, logger=logger)
        self.security_group_manager.delete_all_security_groups(vpc_id, include_default_group=False, logger=logger)
        self.route_table_manager.delete_all_route_tables(vpc_id, include_main_route=False, logger=logger)
        self.subnet_manager.delete_all_subnets(vpc_id, logger=logger) 
        resp = self.jclient.vpc.delete_vpc(vpc_id=vpc_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

