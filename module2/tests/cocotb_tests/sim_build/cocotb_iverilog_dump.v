module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/simple_register.fst");
    $dumpvars(0, simple_register);
end
endmodule
