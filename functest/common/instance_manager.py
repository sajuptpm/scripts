import base_manager
import utils

class InstanceManager(base_manager.BaseManager):
    
    def run_instances(image_id, instance_type_id, subnet_id, key_name):
        res = self.jclient.compute.run_instances(image_id=image_id, instance_type_id=instance_type_id, subnet_id=subnet_id, key_name=key_name)
        instance_id = utils.get_item(('RunInstancesResponse', 'instancesSet', 'item', 'instanceId'), res)
        return instance_id

    def get_all_instance_ids(self, vpc_id):
        ids = []
        items = None
        res = self.jclient.compute.describe_instances()
        try:
            items = utils.get_item(('DescribeInstancesResponse', 'instancesSet', 'item'), res)
        except (KeyError, AttributeError) as ex:
            pass
        if isinstance(items, list):
            return [item['instanceId'] for item in items if item.get('vpcId') == vpc_id]
        elif isinstance(items, dict):
            if items['vpcId'] == vpc_id:
                return [items['instanceId']]
        return ids

    def delete_all_instances(self, vpc_id):
        instance_ids = self.get_all_instance_ids(vpc_id)
        print "......Cleaning Instances: ", len(instance_ids)
        for instance_id in instance_ids:
            self.jclient.compute.terminate_instances(instance_ids=instance_id)

