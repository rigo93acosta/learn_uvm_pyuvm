--
-- Module 2: Simple Register (VHDL)
--
-- A basic register with clock, reset, and enable.
--
-- Ports:
--   clk:    Clock signal
--   rst_n:  Active-low asynchronous reset
--   enable: Register enable
--   d:      Data input
--   q:      Data output
--
library ieee;
use ieee.std_logic_1164.all;

entity simple_register is
    port (
        clk    : in  std_logic := '0';
        rst_n  : in  std_logic := '0';
        enable : in  std_logic := '0';
        d      : in  std_logic_vector(7 downto 0) := (others => '0');
        q      : out std_logic_vector(7 downto 0)
    );
end entity simple_register;

architecture rtl of simple_register is
    signal q_reg : std_logic_vector(7 downto 0) := (others => '0');
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            q_reg <= (others => '0');
        elsif rising_edge(clk) then
            if enable = '1' then
                q_reg <= d;
            end if;
        end if;
    end process;

    q <= q_reg;

end architecture rtl;
