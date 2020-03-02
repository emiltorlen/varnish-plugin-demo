from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import socket
import json
import os
from subprocess import Popen, PIPE

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
        device = group.create_device(identifier="varnishcache",
                                     display_name="VarnishCache")
        # device.add_endpoint(ip=self.address, port=self.port)
        logger.info("Topology: group name=%s, device name=%s", group.name,
                    device.name)
        logger.info("Container %s", self.containerId)
        # Execute command
        try:
            cmd = "docker exec " + self.containerId + "  varnishstat -j"
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            logger.info("Error executing command=%s , err=%s", cmd, stderr)
            data = json.loads(stdout)
            device.absolute("cachehit", value=data["MAIN.cache_hit"]["value"])
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            device.absolute(key='cachehit', value=0)
        finally:
            logger.info("Done")