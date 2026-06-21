--
-- Module 3: Simple Adder (VHDL)
--
-- A basic 8-bit adder for UVM testing.
--
-- Ports:
--   clk:    Clock signal
--   rst_n:  Active-low reset
--   a:      Operand A
--   b:      Operand B
--   sum:    Sum output
--   carry:  Carry output
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity adder is
    port (
        clk   : in  std_logic;
        rst_n : in  std_logic;
        a     : in  std_logic_vector(7 downto 0);
        b     : in  std_logic_vector(7 downto 0);
        sum   : out std_logic_vector(7 downto 0);
        carry : out std_logic
    );
end entity adder;

architecture rtl of adder is
    signal sum_reg   : std_logic_vector(7 downto 0) := (others => '0');
    signal carry_reg : std_logic := '0';
begin

    process(clk, rst_n)
        variable tmp : unsigned(8 downto 0);
    begin
        if rst_n = '0' then
            sum_reg   <= (others => '0');
            carry_reg <= '0';
        elsif rising_edge(clk) then
            tmp := ('0' & unsigned(a)) + ('0' & unsigned(b));
            sum_reg   <= std_logic_vector(tmp(7 downto 0));
            carry_reg <= tmp(8);
        end if;
    end process;

    sum   <= sum_reg;
    carry <= carry_reg;

end architecture rtl;
