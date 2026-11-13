--
-- Module 7: UART Transmitter/Receiver (VHDL)
--
-- A simple UART for protocol verification. There is no baud-rate divider:
-- one bit lasts exactly one clock cycle (8N1, LSB first).
--
-- Ports:
--   clk:      Clock signal
--   rst_n:    Active-low asynchronous reset
--   tx:       Transmit data line (idle high)
--   rx:       Receive data line (idle high)
--   tx_data:  Data to transmit
--   tx_start: Start transmission (sampled only while idle)
--   tx_busy:  Transmission in progress
--   rx_data:  Received data
--   rx_ready: Received data ready (cleared when the next start bit arrives)
--
-- Cycle-exact port of uart.v. Two things differ from a real UART and are worth
-- knowing before writing a testbench:
--   * the receiver waits one extra cycle after the start bit (RX_START), so
--     it samples data bits 1..7 plus the stop bit: it cannot receive what
--     this same transmitter sends in a tx -> rx loopback.
--   * `rx` defaults to '1' (idle) here; in Verilator an undriven `rx` is 0,
--     which looks like a permanent start bit.
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity uart is
    port (
        clk      : in  std_logic := '0';
        rst_n    : in  std_logic := '0';
        tx       : out std_logic;
        rx       : in  std_logic := '1';
        tx_data  : in  std_logic_vector(7 downto 0) := (others => '0');
        tx_start : in  std_logic := '0';
        tx_busy  : out std_logic;
        rx_data  : out std_logic_vector(7 downto 0);
        rx_ready : out std_logic
    );
end entity uart;

architecture rtl of uart is
    -- Transmitter state machine (same 4-bit encoding as the Verilog version)
    constant TX_IDLE      : std_logic_vector(3 downto 0) := x"0";
    constant TX_START_BIT : std_logic_vector(3 downto 0) := x"1";
    constant TX_DATA_BITS : std_logic_vector(3 downto 0) := x"2";
    constant TX_STOP_BIT  : std_logic_vector(3 downto 0) := x"3";

    signal tx_reg       : std_logic := '1';
    signal tx_busy_reg  : std_logic := '0';
    signal tx_state     : std_logic_vector(3 downto 0) := TX_IDLE;
    signal tx_shift     : std_logic_vector(7 downto 0) := (others => '0');
    signal tx_bit_count : unsigned(3 downto 0) := (others => '0');

    -- Receiver state machine
    constant RX_IDLE      : std_logic_vector(3 downto 0) := x"0";
    constant RX_START_BIT : std_logic_vector(3 downto 0) := x"1";
    constant RX_DATA_BITS : std_logic_vector(3 downto 0) := x"2";
    constant RX_STOP_BIT  : std_logic_vector(3 downto 0) := x"3";

    signal rx_data_reg  : std_logic_vector(7 downto 0) := (others => '0');
    signal rx_ready_reg : std_logic := '0';
    signal rx_state     : std_logic_vector(3 downto 0) := RX_IDLE;
    signal rx_shift     : std_logic_vector(7 downto 0) := (others => '0');
    signal rx_bit_count : unsigned(3 downto 0) := (others => '0');
begin

    -- Transmitter
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            tx_reg       <= '1';
            tx_busy_reg  <= '0';
            tx_state     <= TX_IDLE;
            tx_shift     <= (others => '0');
            tx_bit_count <= (others => '0');
        elsif rising_edge(clk) then
            case tx_state is
                when TX_IDLE =>
                    if tx_start = '1' then
                        tx_state    <= TX_START_BIT;
                        tx_shift    <= tx_data;
                        tx_busy_reg <= '1';
                    end if;
                when TX_START_BIT =>
                    tx_reg       <= '0';  -- Start bit
                    tx_state     <= TX_DATA_BITS;
                    tx_bit_count <= (others => '0');
                when TX_DATA_BITS =>
                    tx_reg   <= tx_shift(0);
                    tx_shift <= '0' & tx_shift(7 downto 1);
                    if tx_bit_count = 7 then
                        tx_state <= TX_STOP_BIT;
                    else
                        tx_bit_count <= tx_bit_count + 1;
                    end if;
                when TX_STOP_BIT =>
                    tx_reg      <= '1';  -- Stop bit
                    tx_state    <= TX_IDLE;
                    tx_busy_reg <= '0';
                when others =>
                    tx_state    <= TX_IDLE;
                    tx_busy_reg <= '0';
            end case;
        end if;
    end process;

    -- Receiver (simplified - a real one oversamples each bit)
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            rx_data_reg  <= (others => '0');
            rx_ready_reg <= '0';
            rx_state     <= RX_IDLE;
            rx_shift     <= (others => '0');
            rx_bit_count <= (others => '0');
        elsif rising_edge(clk) then
            case rx_state is
                when RX_IDLE =>
                    if rx = '0' then  -- Start bit detected
                        rx_state     <= RX_START_BIT;
                        rx_ready_reg <= '0';
                    end if;
                when RX_START_BIT =>
                    rx_state     <= RX_DATA_BITS;
                    rx_bit_count <= (others => '0');
                when RX_DATA_BITS =>
                    rx_shift <= rx & rx_shift(7 downto 1);
                    if rx_bit_count = 7 then
                        rx_state <= RX_STOP_BIT;
                    else
                        rx_bit_count <= rx_bit_count + 1;
                    end if;
                when RX_STOP_BIT =>
                    rx_data_reg  <= rx_shift;
                    rx_ready_reg <= '1';
                    rx_state     <= RX_IDLE;
                when others =>
                    rx_state     <= RX_IDLE;
                    rx_ready_reg <= '0';
            end case;
        end if;
    end process;

    tx       <= tx_reg;
    tx_busy  <= tx_busy_reg;
    rx_data  <= rx_data_reg;
    rx_ready <= rx_ready_reg;

end architecture rtl;
