import base_manager
import generic_manager
import utils

class SecurityGroupManager(base_manager.BaseManager):

    def create_security_group(self, vpc_id, name, description, logger=None):
        resp = self.jclient.vpc.create_security_group(vpc_id=vpc_id, group_name=name, group_description=description)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
            return utils.get_item(('CreateSecurityGroupResponse', 'groupId'), resp)
        else:
            logger and logger.error(resp)

    def describe_security_groups(self, group_ids=None, logger=None):
        resp = self.jclient.vpc.describe_security_groups(group_ids=group_ids)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def delete_security_group(self, group_id, logger=None):
        resp = self.jclient.vpc.delete_security_group(group_id=group_id)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)

    def get_all_security_group_ids(self, vpc_id, include_default_group=False):
        ids = []
        items = None
        res = self.jclient.vpc.describe_security_groups()
        items = utils.get_item(('DescribeSecurityGroupsResponse', 'securityGroupInfo', 'item'), res)
        if isinstance(items, list):
            if include_default_group:
                return [item['groupId'] for item in items if item.get('vpcId') == vpc_id]
            else:
                return [item['groupId'] for item in items if item.get('vpcId') == vpc_id if item.get('groupName') != 'default']
        elif isinstance(items, dict):
            if include_default_group:
                if items['vpcId'] == vpc_id:
                    return [items['groupId']]
                else:
                    if items['vpcId'] == vpc_id and items.get('groupName') != 'default':
                        return [items['groupId']]
        return ids

    def delete_all_security_groups(self, vpc_id, include_default_group=False, logger=None):
        ids = self.get_all_security_group_ids(vpc_id, include_default_group=include_default_group)
        logger and logger.info("......Cleaning Security Groups: {num}".format(num=len(ids)))
        for secgrp_id in ids:
            resp = self.jclient.vpc.delete_security_group(group_id=secgrp_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)


