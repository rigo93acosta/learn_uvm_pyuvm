--
-- Module 5: Multi-Channel Interface (VHDL)
--
-- A multi-channel interface for advanced UVM testing.
--
-- Ports:
--   clk:          Clock signal
--   rst_n:        Active-low asynchronous reset
--   master_valid: Master channel valid
--   master_ready: Master channel ready (master_valid delayed one cycle)
--   master_data:  Master channel data (not used by the logic)
--   slave_valid:  Slave channel valid
--   slave_ready:  Slave channel ready (slave_valid delayed one cycle)
--   slave_data:   Slave channel data (not used by the logic)
--
library ieee;
use ieee.std_logic_1164.all;

entity multi_channel is
    port (
        clk          : in  std_logic := '0';
        rst_n        : in  std_logic := '0';
        master_valid : in  std_logic := '0';
        master_ready : out std_logic;
        master_data  : in  std_logic_vector(7 downto 0) := (others => '0');
        slave_valid  : in  std_logic := '0';
        slave_ready  : out std_logic;
        slave_data   : in  std_logic_vector(7 downto 0) := (others => '0')
    );
end entity multi_channel;

architecture rtl of multi_channel is
    signal master_ready_reg : std_logic := '0';
    signal slave_ready_reg  : std_logic := '0';
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            master_ready_reg <= '0';
            slave_ready_reg  <= '0';
        elsif rising_edge(clk) then
            master_ready_reg <= master_valid;
            slave_ready_reg  <= slave_valid;
        end if;
    end process;

    master_ready <= master_ready_reg;
    slave_ready  <= slave_ready_reg;

end architecture rtl;
