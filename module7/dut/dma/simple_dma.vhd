--
-- Module 7: Simple DMA Controller (VHDL)
--
-- A simple DMA controller for verification. It does not move data: it only
-- latches the request and counts `dma_length + 1` cycles before pulsing
-- `dma_done` for one cycle.
--
-- Ports:
--   clk:          Clock signal
--   rst_n:        Active-low asynchronous reset
--   dma_start:    Start DMA transfer
--   dma_done:     DMA transfer complete (one-cycle pulse)
--   dma_src_addr: Source address
--   dma_dst_addr: Destination address
--   dma_length:   Transfer length
--   dma_channel:  DMA channel select
--
-- Cycle-exact port of simple_dma.v. Known quirk kept on purpose: after reset
-- length_reg = 0 and count = 0, so `dma_done` pulses every other cycle while
-- idle, even if `dma_start` was never asserted (see docs/ROADMAP_es.md).
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity simple_dma is
    port (
        clk          : in  std_logic := '0';
        rst_n        : in  std_logic := '0';
        dma_start    : in  std_logic := '0';
        dma_done     : out std_logic;
        dma_src_addr : in  std_logic_vector(31 downto 0) := (others => '0');
        dma_dst_addr : in  std_logic_vector(31 downto 0) := (others => '0');
        dma_length   : in  std_logic_vector(15 downto 0) := (others => '0');
        dma_channel  : in  std_logic_vector(2 downto 0)  := (others => '0')
    );
end entity simple_dma;

architecture rtl of simple_dma is
    signal dma_done_reg : std_logic := '0';
    signal src_addr_reg : std_logic_vector(31 downto 0) := (others => '0');
    signal dst_addr_reg : std_logic_vector(31 downto 0) := (others => '0');
    signal length_reg   : unsigned(15 downto 0) := (others => '0');
    signal channel_reg  : std_logic_vector(2 downto 0) := (others => '0');
    signal count        : unsigned(15 downto 0) := (others => '0');
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            dma_done_reg <= '0';
            src_addr_reg <= (others => '0');
            dst_addr_reg <= (others => '0');
            length_reg   <= (others => '0');
            channel_reg  <= (others => '0');
            count        <= (others => '0');
        elsif rising_edge(clk) then
            if dma_start = '1' and dma_done_reg = '0' then
                src_addr_reg <= dma_src_addr;
                dst_addr_reg <= dma_dst_addr;
                length_reg   <= unsigned(dma_length);
                channel_reg  <= dma_channel;
                count        <= (others => '0');
            elsif dma_done_reg = '0' then
                if count < length_reg then
                    count <= count + 1;
                else
                    dma_done_reg <= '1';
                end if;
            else
                dma_done_reg <= '0';
            end if;
        end if;
    end process;

    dma_done <= dma_done_reg;

end architecture rtl;
