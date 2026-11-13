--
-- Module 2: Simple FIFO (VHDL)
--
-- A basic 16-entry FIFO with read/write pointers.
--
-- Ports:
--   clk:      Clock signal
--   rst_n:    Active-low asynchronous reset
--   write_en: Write enable
--   read_en:  Read enable
--   data_in:  Write data
--   data_out: Read data (registered, valid the cycle after read_en)
--   full:     FIFO full flag
--   empty:    FIFO empty flag
--
-- IMPORTANT: this is a cycle-exact port of simple_fifo.v, design flaws
-- included, because finding them is a good verification exercise
-- (see docs/ROADMAP_es.md, Module 2):
--   * full/empty are registered from the *previous* value of `count`, so
--     they lag one cycle behind the real occupancy.
--   * On a simultaneous read and write, the last assignment to `count`
--     wins (count - 1), so the occupancy counter drifts.
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity simple_fifo is
    port (
        clk      : in  std_logic := '0';
        rst_n    : in  std_logic := '0';
        write_en : in  std_logic := '0';
        read_en  : in  std_logic := '0';
        data_in  : in  std_logic_vector(7 downto 0) := (others => '0');
        data_out : out std_logic_vector(7 downto 0);
        full     : out std_logic;
        empty    : out std_logic
    );
end entity simple_fifo;

architecture rtl of simple_fifo is
    type mem_t is array (0 to 15) of std_logic_vector(7 downto 0);

    signal mem          : mem_t := (others => (others => '0'));
    signal write_ptr    : unsigned(4 downto 0) := (others => '0');
    signal read_ptr     : unsigned(4 downto 0) := (others => '0');
    signal count        : unsigned(4 downto 0) := (others => '0');
    signal data_out_reg : std_logic_vector(7 downto 0) := (others => '0');
    signal full_reg     : std_logic := '0';
    signal empty_reg    : std_logic := '1';
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            write_ptr <= (others => '0');
            read_ptr  <= (others => '0');
            count     <= (others => '0');
            full_reg  <= '0';
            empty_reg <= '1';
        elsif rising_edge(clk) then
            -- Write operation
            if write_en = '1' and full_reg = '0' then
                mem(to_integer(write_ptr(3 downto 0))) <= data_in;
                write_ptr <= write_ptr + 1;
                count     <= count + 1;
            end if;

            -- Read operation
            if read_en = '1' and empty_reg = '0' then
                data_out_reg <= mem(to_integer(read_ptr(3 downto 0)));
                read_ptr     <= read_ptr + 1;
                count        <= count - 1;
            end if;

            -- Update flags (uses the value of count *before* this edge)
            if count = 16 then
                full_reg <= '1';
            else
                full_reg <= '0';
            end if;

            if count = 0 then
                empty_reg <= '1';
            else
                empty_reg <= '0';
            end if;
        end if;
    end process;

    data_out <= data_out_reg;
    full     <= full_reg;
    empty    <= empty_reg;

end architecture rtl;
