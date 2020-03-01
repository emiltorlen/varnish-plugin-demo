from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import socket
import os
logger = logging.getLogger(__name__)
class VarnishContainerPluginRemote(RemoteBasePlugin):
	def initialize(self, **kwargs):
		logger.info("Config: %s", self.config)
		self.containerId = self.config["containerid"]
	def query(self, **kwargs):
		# Create group - provide group id used to calculate unique entity id in dynatrace
		#   and display name for UI presentation
		group = self.topology_builder.create_group(identifier="Varnish",
												   group_name="Varnishstats")
		# Create device - provide device id used to calculate unique entity id in dynatrace
		#   and display name for UI presentation
		device = group.create_device(identifier="varnishcache", display_name="VarnishCache")
		# device.add_endpoint(ip=self.address, port=self.port)
		logger.info("Topology: group name=%s, device name=%s", group.name, device.name)
		# Execute command
		try:
			cmd = "docker exec -it " + self.containerId + "  varnishstat -j > out.json"
			os.system(cmd)
			with open('out.json') as f:
				data = json.load(f)
				device.state_metric(key="cachehit",value=data["MAIN.cache_hit"]["value"])
		except Exception as e:
			device.state_metric(key='cachehit', value=0)
		finally:
			logger.info("Done")