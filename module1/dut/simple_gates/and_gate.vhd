--
-- Module 1: Simple AND Gate (VHDL)
--
-- A basic 2-input AND gate for verification examples.
--
-- Ports:
--   a, b: Input signals
--   y:    Output signal
--
-- Note: inputs default to '0' so the DUT starts in a known state (instead of
-- 'U') when the testbench has not driven them yet. See docs/VHDL_GHDL_es.md.
--
library ieee;
use ieee.std_logic_1164.all;

entity and_gate is
    port (
        a : in  std_logic := '0';
        b : in  std_logic := '0';
        y : out std_logic
    );
end entity and_gate;

architecture rtl of and_gate is
begin

    y <= a and b;

end architecture rtl;
