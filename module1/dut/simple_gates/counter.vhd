--
-- Module 1: Simple Counter (VHDL)
--
-- A basic up-counter with reset for verification examples.
--
-- Ports:
--   clk:    Clock signal
--   rst_n:  Active-low asynchronous reset
--   enable: Counter enable
--   count:  Counter output (wraps from 255 to 0)
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
    port (
        clk    : in  std_logic := '0';
        rst_n  : in  std_logic := '0';
        enable : in  std_logic := '0';
        count  : out std_logic_vector(7 downto 0)
    );
end entity counter;

architecture rtl of counter is
    signal count_reg : unsigned(7 downto 0) := (others => '0');
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            count_reg <= (others => '0');
        elsif rising_edge(clk) then
            if enable = '1' then
                count_reg <= count_reg + 1;
            end if;
        end if;
    end process;

    count <= std_logic_vector(count_reg);

end architecture rtl;
