--
-- Module 2: Simple Finite State Machine (VHDL)
--
-- A basic state machine with 4 states: IDLE -> START -> WORK -> DONE -> IDLE.
--
-- Ports:
--   clk:    Clock signal
--   rst_n:  Active-low asynchronous reset
--   start:  Start signal (sampled only in IDLE)
--   done:   Done pulse, high for one cycle when the FSM returns to IDLE
--   state:  Current state output ("00" IDLE, "01" START, "10" WORK, "11" DONE)
--
-- Note: VHDL is case-insensitive, so the state constants cannot be called
-- START/DONE as in the Verilog version (they would clash with the ports
-- `start` and `done`). They carry the ST_ prefix instead.
--
library ieee;
use ieee.std_logic_1164.all;

entity simple_fsm is
    port (
        clk   : in  std_logic := '0';
        rst_n : in  std_logic := '0';
        start : in  std_logic := '0';
        done  : out std_logic;
        state : out std_logic_vector(1 downto 0)
    );
end entity simple_fsm;

architecture rtl of simple_fsm is
    -- State encoding (kept as an explicit vector so the testbench can read it)
    constant ST_IDLE  : std_logic_vector(1 downto 0) := "00";
    constant ST_START : std_logic_vector(1 downto 0) := "01";
    constant ST_WORK  : std_logic_vector(1 downto 0) := "10";
    constant ST_DONE  : std_logic_vector(1 downto 0) := "11";

    signal state_reg : std_logic_vector(1 downto 0) := ST_IDLE;
    signal done_reg  : std_logic := '0';
begin

    process(clk, rst_n)
    begin
        if rst_n = '0' then
            state_reg <= ST_IDLE;
            done_reg  <= '0';
        elsif rising_edge(clk) then
            case state_reg is
                when ST_IDLE =>
                    if start = '1' then
                        state_reg <= ST_START;
                        done_reg  <= '0';
                    end if;
                when ST_START =>
                    state_reg <= ST_WORK;
                    done_reg  <= '0';
                when ST_WORK =>
                    state_reg <= ST_DONE;
                    done_reg  <= '0';
                when ST_DONE =>
                    state_reg <= ST_IDLE;
                    done_reg  <= '1';
                when others =>
                    state_reg <= ST_IDLE;
                    done_reg  <= '0';
            end case;
        end if;
    end process;

    state <= state_reg;
    done  <= done_reg;

end architecture rtl;
