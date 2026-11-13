--
-- Module 4: Simple Interface (VHDL)
--
-- A simple valid/ready interface for UVM component testing.
--
-- Ports:
--   clk:     Clock signal
--   rst_n:   Active-low asynchronous reset
--   valid:   Valid signal
--   ready:   Ready signal (valid delayed one cycle)
--   data:    Data bus
--   address: Address bus (not used by the logic)
--   result:  data + 1 (wraps at 255), registered when valid = '1'
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity simple_interface is
    port (
        clk     : in  std_logic := '0';
        rst_n   : in  std_logic := '0';
        valid   : in  std_logic := '0';
        ready   : out std_logic;
        data    : in  std_logic_vector(7 downto 0)  := (others => '0');
        address : in  std_logic_vector(15 downto 0) := (others => '0');
        result  : out std_logic_vector(7 downto 0)
    );
end entity simple_interface;

architecture rtl of simple_interface is
    signal ready_reg  : std_logic := '0';
    signal result_reg : std_logic_vector(7 downto 0) := (others => '0');
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            ready_reg  <= '0';
            result_reg <= (others => '0');
        elsif rising_edge(clk) then
            if valid = '1' then
                ready_reg <= '1';
                -- Simple operation: result = data + 1
                result_reg <= std_logic_vector(unsigned(data) + 1);
            else
                ready_reg <= '0';
            end if;
        end if;
    end process;

    ready  <= ready_reg;
    result <= result_reg;

end architecture rtl;
