import base_manager
import utils

class SecurityGroupRuleManager(base_manager.BaseManager):

    def create_ingress_rule(self, security_group_id, ip_permissions=None, logger=None):
        if not ip_permissions:
            ip_permissions = '[{"IpProtocol": "icmp", "FromPort": 80, "ToPort": 81, "IpRanges":[{"CidrIp": "0.0.0.0/0"}]}]'
        resp = self.jclient.vpc.authorize_security_group_ingress(group_id=security_group_id, ip_permissions=ip_permissions)
        if utils.get_status_code(resp):
            logger and logger.info(resp)
        else:
            logger and logger.error(resp)


