import base_manager
import generic_manager
import utils

class SecurityGroupManager(base_manager.BaseManager):

    def create_security_group(self, name, description, vpc_id):
        res = self.jclient.vpc.create_security_group(name = name, description = description, vpc_id = vpc_id)
        group_id = utils.get_item(('CreateSecurityGroupResponse','groupId'), res)
        return group_id


