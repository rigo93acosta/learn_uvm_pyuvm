--
-- Module 9: Lossy Channel (VHDL)
--
-- Whatever enters on TX leaves on RX one clock cycle later, unless the channel
-- drops it. Drops are decided by an 8-bit LFSR (taps 8,6,5,4: maximal length,
-- period 255), so they are deterministic and the simulation is repeatable.
-- A word is dropped when the two low bits of the LFSR are "00" (about 25 %).
--
-- Ports:
--   clk:       Clock signal
--   rst:       Active-high synchronous reset
--   lfsr_seed: Value loaded into the LFSR while rst = '1'. It selects the loss
--              pattern. Seed 0 locks the LFSR at 0: the channel drops everything.
--   tx_valid:  Word on tx_data is valid this cycle
--   tx_data:   Word to send
--   rx_valid:  Word on rx_data is valid this cycle (one-cycle pulse)
--   rx_data:   Word that left the channel
--
-- The channel does not interpret the data. The 8-bit format (sequence number
-- in bits 7..4, information in bits 3..0) is only known to the testbench.
--
library ieee;
use ieee.std_logic_1164.all;

entity lossy_channel is
    port (
        clk       : in  std_logic := '0';
        rst       : in  std_logic := '0';
        lfsr_seed : in  std_logic_vector(7 downto 0) := x"A5";
        tx_valid  : in  std_logic := '0';
        tx_data   : in  std_logic_vector(7 downto 0) := (others => '0');
        rx_valid  : out std_logic;
        rx_data   : out std_logic_vector(7 downto 0)
    );
end entity lossy_channel;

architecture rtl of lossy_channel is
    signal lfsr         : std_logic_vector(7 downto 0) := x"A5";
    signal drop         : std_logic;
    signal rx_valid_reg : std_logic := '0';
    signal rx_data_reg  : std_logic_vector(7 downto 0) := (others => '0');
begin

    drop <= '1' when lfsr(1 downto 0) = "00" else '0';

    process(clk)
    begin
        if rising_edge(clk) then
            rx_valid_reg <= '0';
            if rst = '1' then
                lfsr        <= lfsr_seed;
                rx_data_reg <= (others => '0');
            else
                lfsr <= lfsr(6 downto 0)
                        & (lfsr(7) xor lfsr(5) xor lfsr(4) xor lfsr(3));
                if tx_valid = '1' and drop = '0' then
                    rx_valid_reg <= '1';
                    rx_data_reg  <= tx_data;
                end if;
            end if;
        end if;
    end process;

    rx_valid <= rx_valid_reg;
    rx_data  <= rx_data_reg;

end architecture rtl;
