import base_manager
import utils

class InstanceManager(base_manager.BaseManager):

    def check_instance_state(self, instance_id, timeout=300, logger=None):
        start_time = time.time()
        while True:
            resp = self.jclient.compute.describe_instances(instance_ids=instance_id)
            state = utils.get_item(('DescribeInstancesResponse', 'instancesSet', 'item', 'instanceState', 'name'), resp)
            if state in ['running']:
                logger and logger.info(resp)
                return
            if (time.time() - start_time) >= timeout:
                logger and logger.error(resp)
                return

    def run_instances(image_id, instance_type_id, subnet_id, key_name=None, timeout=300, logger=None):
        resp = self.jclient.compute.run_instances(image_id=image_id, instance_type_id=instance_type_id, subnet_id=subnet_id, key_name=key_name)
        if self.get_status_code(resp):
            logger and logger.info(resp)
            instance_id = utils.get_item(('RunInstancesResponse', 'instancesSet', 'item', 'instanceId'), res)
            self.check_instance_state(instance_id, timeout=timeout, logger=logger)
            return instance_id
        else:
            logger and logger.error(resp) 

    def get_all_instance_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.compute.describe_instances()
        items = utils.get_item(('DescribeInstancesResponse', 'instancesSet', 'item'), res)
        if isinstance(items, list):
            return [item['instanceId'] for item in items if item.get('vpcId') == vpc_id]
        elif isinstance(items, dict):
            if items['vpcId'] == vpc_id:
                return [items['instanceId']]
        return ids

    def delete_all_instances(self, vpc_id, logger=None):
        instance_ids = self.get_all_instance_ids(vpc_id)
        logger and logger.info("......Cleaning Instances: {num}".format(num=len(instance_ids)))
        for instance_id in instance_ids:
            resp = self.jclient.compute.terminate_instances(instance_ids=instance_id)
            if utils.get_status_code(resp):
                logger and logger.info(resp)
            else:
                logger and logger.error(resp)

