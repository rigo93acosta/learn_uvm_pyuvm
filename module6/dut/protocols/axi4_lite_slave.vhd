--
-- Module 6: AXI4-Lite Slave (VHDL)
--
-- A small AXI4-Lite slave backed by a 1024-word memory, for protocol
-- verification.
--
-- This is NOT a line-by-line port of axi4_lite_slave.v. The Verilog version
-- drives `write_state` from two always blocks (illegal for synthesis, and an
-- unresolved multiple driver in VHDL) and uses AWADDR/ARADDR after the address
-- handshake has finished. This version is a clean re-implementation:
--
--   * Port names are lower case (aclk, awvalid, ...), which is what the Python
--     examples of this module already use (`dut.awvalid`, `dut.rdata`, ...).
--   * AW and W are accepted independently and in any order; address and data
--     are latched on their handshake.
--   * xREADY is a one-cycle pulse, raised one cycle after xVALID is seen.
--   * WSTRB selects which bytes are written.
--   * Addresses are word aligned (bits 1..0 ignored). Bits 11..2 select the
--     word. Any address with bits 31..12 /= 0 is out of range: the access
--     answers SLVERR ("10"), a write is dropped and a read returns 0.
--   * One write and one read can be in flight at the same time (independent
--     channels), but each channel handles a single transaction at a time.
--
-- Write channel timing (clock cycles):
--   awvalid  __/~~~~~\________      wvalid  __/~~~~~\________
--   awready  ______/~\________      wready  ______/~\________
--   bvalid   ___________/~~~~\_ (until bready)
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity axi4_lite_slave is
    port (
        aclk    : in  std_logic := '0';
        aresetn : in  std_logic := '0';

        -- Write Address Channel
        awvalid : in  std_logic := '0';
        awready : out std_logic;
        awaddr  : in  std_logic_vector(31 downto 0) := (others => '0');
        awprot  : in  std_logic_vector(2 downto 0)  := (others => '0');

        -- Write Data Channel
        wvalid  : in  std_logic := '0';
        wready  : out std_logic;
        wdata   : in  std_logic_vector(31 downto 0) := (others => '0');
        wstrb   : in  std_logic_vector(3 downto 0)  := (others => '0');

        -- Write Response Channel
        bvalid  : out std_logic;
        bready  : in  std_logic := '0';
        bresp   : out std_logic_vector(1 downto 0);

        -- Read Address Channel
        arvalid : in  std_logic := '0';
        arready : out std_logic;
        araddr  : in  std_logic_vector(31 downto 0) := (others => '0');
        arprot  : in  std_logic_vector(2 downto 0)  := (others => '0');

        -- Read Data Channel
        rvalid  : out std_logic;
        rready  : in  std_logic := '0';
        rdata   : out std_logic_vector(31 downto 0);
        rresp   : out std_logic_vector(1 downto 0)
    );
end entity axi4_lite_slave;

architecture rtl of axi4_lite_slave is
    constant RESP_OKAY   : std_logic_vector(1 downto 0) := "00";
    constant RESP_SLVERR : std_logic_vector(1 downto 0) := "10";

    type mem_t is array (0 to 1023) of std_logic_vector(31 downto 0);
    signal mem : mem_t := (others => (others => '0'));

    -- Write side
    signal awready_reg : std_logic := '0';
    signal wready_reg  : std_logic := '0';
    signal bvalid_reg  : std_logic := '0';
    signal bresp_reg   : std_logic_vector(1 downto 0) := RESP_OKAY;
    signal aw_got      : std_logic := '0';  -- address latched, waiting for data
    signal w_got       : std_logic := '0';  -- data latched, waiting for address
    signal awaddr_reg  : std_logic_vector(31 downto 0) := (others => '0');
    signal wdata_reg   : std_logic_vector(31 downto 0) := (others => '0');
    signal wstrb_reg   : std_logic_vector(3 downto 0)  := (others => '0');

    -- Read side
    signal arready_reg : std_logic := '0';
    signal rvalid_reg  : std_logic := '0';
    signal rdata_reg   : std_logic_vector(31 downto 0) := (others => '0');
    signal rresp_reg   : std_logic_vector(1 downto 0) := RESP_OKAY;

    function in_range(addr : std_logic_vector(31 downto 0)) return boolean is
    begin
        return unsigned(addr(31 downto 12)) = 0;
    end function;

    function word_index(addr : std_logic_vector(31 downto 0)) return natural is
    begin
        return to_integer(unsigned(addr(11 downto 2)));
    end function;
begin

    -- Write channels (AW, W, B)
    write_proc : process(aclk, aresetn)
    begin
        if aresetn = '0' then
            awready_reg <= '0';
            wready_reg  <= '0';
            bvalid_reg  <= '0';
            bresp_reg   <= RESP_OKAY;
            aw_got      <= '0';
            w_got       <= '0';
        elsif rising_edge(aclk) then
            -- Address handshake: one-cycle awready pulse, then latch
            if awready_reg = '1' then
                awready_reg <= '0';
                if awvalid = '1' then
                    awaddr_reg <= awaddr;
                    aw_got     <= '1';
                end if;
            elsif awvalid = '1' and aw_got = '0' and bvalid_reg = '0' then
                awready_reg <= '1';
            end if;

            -- Data handshake: one-cycle wready pulse, then latch
            if wready_reg = '1' then
                wready_reg <= '0';
                if wvalid = '1' then
                    wdata_reg <= wdata;
                    wstrb_reg <= wstrb;
                    w_got     <= '1';
                end if;
            elsif wvalid = '1' and w_got = '0' and bvalid_reg = '0' then
                wready_reg <= '1';
            end if;

            -- Both halves received: perform the write and send the response
            if aw_got = '1' and w_got = '1' and bvalid_reg = '0' then
                if in_range(awaddr_reg) then
                    for i in 0 to 3 loop
                        if wstrb_reg(i) = '1' then
                            mem(word_index(awaddr_reg))(8 * i + 7 downto 8 * i)
                                <= wdata_reg(8 * i + 7 downto 8 * i);
                        end if;
                    end loop;
                    bresp_reg <= RESP_OKAY;
                else
                    bresp_reg <= RESP_SLVERR;
                end if;
                bvalid_reg <= '1';
                aw_got     <= '0';
                w_got      <= '0';
            elsif bvalid_reg = '1' and bready = '1' then
                bvalid_reg <= '0';
            end if;
        end if;
    end process write_proc;

    -- Read channels (AR, R)
    read_proc : process(aclk, aresetn)
    begin
        if aresetn = '0' then
            arready_reg <= '0';
            rvalid_reg  <= '0';
            rdata_reg   <= (others => '0');
            rresp_reg   <= RESP_OKAY;
        elsif rising_edge(aclk) then
            if arready_reg = '1' then
                arready_reg <= '0';
                if arvalid = '1' then
                    if in_range(araddr) then
                        rdata_reg <= mem(word_index(araddr));
                        rresp_reg <= RESP_OKAY;
                    else
                        rdata_reg <= (others => '0');
                        rresp_reg <= RESP_SLVERR;
                    end if;
                    rvalid_reg <= '1';
                end if;
            elsif arvalid = '1' and rvalid_reg = '0' then
                arready_reg <= '1';
            elsif rvalid_reg = '1' and rready = '1' then
                rvalid_reg <= '0';
            end if;
        end if;
    end process read_proc;

    awready <= awready_reg;
    wready  <= wready_reg;
    bvalid  <= bvalid_reg;
    bresp   <= bresp_reg;
    arready <= arready_reg;
    rvalid  <= rvalid_reg;
    rdata   <= rdata_reg;
    rresp   <= rresp_reg;

end architecture rtl;
