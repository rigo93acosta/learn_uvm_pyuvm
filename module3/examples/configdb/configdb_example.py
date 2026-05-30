"""
Module 3 Example 3.4: UVM ConfigDB
Demonstrates UVM configuration database usage with default values.
"""

import cocotb
from cocotb.triggers import Timer
import pyuvm
from pyuvm import *


# ==============================================================================
# AUX FUNCTION TO GET CONFIG WITH DEFAULT 
# ==============================================================================
def get_config(cntxt, inst_name, field_name, default=None):
    try:
        return ConfigDB().get(cntxt, inst_name, field_name)
    except Exception:
        return default


class AgentConfig(uvm_object):
    """Configuration object for agent."""

    def __init__(self, name="AgentConfig"):
        super().__init__(name)
        self.active = True
        self.has_coverage = False
        self.address_width = 32
        self.data_width = 8


class ConfigurableAgent(uvm_agent):
    """Agent that uses ConfigDB for configuration."""

    def build_phase(self):
        """Build phase - get configuration from ConfigDB."""
        self.logger.info(f"[{self.get_name()}] Building agent")

        config = get_config(self, "", "agent_config", default=None)

        if config is not None:
            self.logger.info(
                f"  Got config: active={config.active}, "
                f"has_coverage={config.has_coverage}"
            )
            self.active = config.active
            self.has_coverage = config.has_coverage
        else:
            self.logger.warning("  No config found, using defaults")
            self.active = True
            self.has_coverage = False

        self.address_width = get_config(self, "", "address_width", default=32)
        self.data_width = get_config(self, "", "data_width", default=8)

        self.logger.info(f"  Got address_width: {self.address_width}")
        self.logger.info(f"  Got data_width: {self.data_width}")


class ConfigurableEnv(uvm_env):
    """Environment that sets configuration in ConfigDB."""

    def build_phase(self):
        """Build phase - set configuration in ConfigDB."""
        self.logger.info("Building ConfigurableEnv")


        
        # Create and set configuration object
        agent_config = AgentConfig("agent_config")
        agent_config.active = True
        agent_config.has_coverage = True
        agent_config.address_width = 16
        agent_config.data_width = 2

        # Configuramos para el path del agente
        ConfigDB().set(self, "agent_t0", "agent_config", None)
        self.logger.info("Set agent_config in ConfigDB")

        # Si descomentas estos, también sobreescriben los escalares:
        # ConfigDB().set(self, "agent_t0", "address_width", 16)
        # ConfigDB().set(self, "agent_t0", "data_width", 2)
        self.logger.info("Set scalar configs in ConfigDB")

        # Create agent (will get config from ConfigDB)
        self.agent = ConfigurableAgent.create("agent_t0", self)
        

    def connect_phase(self):
        """Connect phase."""
        self.logger.info("Connecting ConfigurableEnv")


@pyuvm.test()
class ConfigDBTest(uvm_test):
    """Test demonstrating ConfigDB usage."""

    def build_phase(self):
        """Build phase."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB Example")
        self.logger.info("=" * 60)
        self.env = ConfigurableEnv.create("env", self)

    async def run_phase(self):
        """Run phase."""
        self.raise_objection()
        self.logger.info("Running ConfigDBTest")

        self.logger.info("=" * 60)
        self.logger.info("Hierarchical Configuration Example:")

        # Set config at test level
        ConfigDB().set(self, "env.agent", "test_config", "test_value")
        self.logger.info("Set config at test level for env.agent")

        test_value = get_config(self, "env.agent", "test_config", default=None)
        if test_value is not None:
            self.logger.info(f"Got config: {test_value}")

        await Timer(10, unit="ns")
        self.drop_objection()

    def report_phase(self):
        """Report phase."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB test completed")
        self.logger.info("=" * 60)


@pyuvm.test()
class ConfigDBHierarchyTest(uvm_test):
    """Test demonstrating ConfigDB hierarchy."""

    def build_phase(self):
        """Build phase - demonstrate configuration hierarchy."""
        self.logger.info("=" * 60)
        self.logger.info("ConfigDB Hierarchy Example")
        self.logger.info("=" * 60)

        # Set configuration at different levels
        ConfigDB().set(None, "", "global_config", "global_value")
        ConfigDB().set(self, "", "test_config", "test_value")
        ConfigDB().set(self, "env", "env_config", "env_value")

        self.logger.info("Set configurations at different hierarchy levels")
        self.env = ConfigurableEnv.create("env", self)

    async def run_phase(self):
        """Run phase."""
        self.raise_objection()

        self.logger.info("=" * 60)
        self.logger.info("Configuration Lookup:")

        # CORREGIDO: Usando la función auxiliar con defaults
        global_val = get_config(None, "", "global_config", default="fallback_global")
        self.logger.info(f"  Global config: {global_val}")

        test_val = get_config(self, "", "test_config", default="fallback_test")
        self.logger.info(f"  Test config: {test_val}")

        env_val = get_config(self, "env", "env_config", default="fallback_env")
        self.logger.info(f"  Env config: {env_val}")

        await Timer(10, unit="ns")
        self.drop_objection()