"""
A simple inventory plugin that reads a list of hosts off a kafka topic
dparry@redhat.com
"""

import os.path
from typing import List, Dict, Any
import json
# The imports below are the ones required for an Ansible plugin
from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable

DOCUMENTATION = r'''
    name: event_hub_inventory_plugin
    plugin_type: inventory
    short_description: Returns a dynamic host inventory from an Event Hub
    description: Returns a dynamic host inventory from Event hub 
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['event_hub_inventory_plugin']
      topic:
        description: Name of the topic to query
        required: true
'''


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'event_hub_inventory_plugin'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.topic = None
        self.plugin = None

    def verify_file(self, path: str):
        if super(InventoryModule, self).verify_file(path):
            return path.endswith('yaml') or path.endswith('yml')
        return False

    def parse(self, inventory: Any, loader: Any, path: Any, cache: bool = True) -> Any:
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)  # This also loads the cache
        try:
            self.plugin = self.get_option('plugin')
            self.topic = self.get_option('topic')
            hosts_data = list(EventHubParser(self.topic))
            if not hosts_data:
                raise AnsibleParserError("Unable to get data from Event Hub")
            for host_data in hosts_data:
                self.inventory.add_group(host_data['db_type'])
                self.inventory.add_host(host_data['hostname'], group=host_data['db_type'])
                self.inventory.set_variable(host_data['hostname'], 'database', host_data['database_name'])
        except KeyError as kerr:
            raise AnsibleParserError(f'Missing required option on the configuration file: {path}', kerr)

class EventHubParser:

    def __init__(self, topic: str):
        self.topic = topic
        self.hosts = None

    def __iter__(self):
        with open(self.topic) as fp:
            self.hosts = json.load(fp)
        if not self.hosts:
            raise ValueError("No valid json imported")
        return self

    def __next__(self):
        try:
            return self.hosts.pop()
        except IndexError:
            raise StopIteration
