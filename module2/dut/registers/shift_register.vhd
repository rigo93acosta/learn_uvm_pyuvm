--
-- Module 2: Shift Register (VHDL)
--
-- A simple 8-bit shift register (shifts towards the MSB).
--
-- Ports:
--   clk:      Clock signal
--   rst_n:    Active-low asynchronous reset
--   shift:    Shift enable
--   data_in:  Serial data input (enters at q(0))
--   data_out: Serial data output (registered copy of the bit leaving q(7))
--   q:        Parallel output
--
library ieee;
use ieee.std_logic_1164.all;

entity shift_register is
    port (
        clk      : in  std_logic := '0';
        rst_n    : in  std_logic := '0';
        shift    : in  std_logic := '0';
        data_in  : in  std_logic := '0';
        data_out : out std_logic;
        q        : out std_logic_vector(7 downto 0)
    );
end entity shift_register;

architecture rtl of shift_register is
    signal q_reg        : std_logic_vector(7 downto 0) := (others => '0');
    signal data_out_reg : std_logic := '0';
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            q_reg        <= (others => '0');
            data_out_reg <= '0';
        elsif rising_edge(clk) then
            if shift = '1' then
                q_reg        <= q_reg(6 downto 0) & data_in;
                data_out_reg <= q_reg(7);
            end if;
        end if;
    end process;

    q        <= q_reg;
    data_out <= data_out_reg;

end architecture rtl;
