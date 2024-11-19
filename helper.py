import argparse

def get_commandline(server=True, description=None, cmdline=None):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-c", "--comm", choices=["tcp", "udp", "serial", "tls", "rtu_tcp"], default="tcp"
    )
    parser.add_argument(
        "-f", "--framer", choices=["ascii", "rtu", "socket", "tls"], default="rtu"
    )
    parser.add_argument("-l", "--log", choices=["critical", "error", "warning", "info", "debug"], default="info")
    parser.add_argument("-p", "--port", required=True)
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("-s","--slave_id", type=int, default=1)
    parser.add_argument("--address", type=int, default=128)
    parser.add_argument("--value", type=int, default=0)
    parser.add_argument("--values", type=int, nargs='+', 
                        help="Values to write to registers. Provide multiple values separated by space for writing to multiple registers.")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--endian", choices=['big', 'little', 'mixed'], default='big', 
                        help='Byte order')
    parser.add_argument("--register_type", choices=['holding', 'input', 'coil', 'discrete_input'], default='holding', 
                        help='Register types')
    parser.add_argument("--function", choices=['read', 'write'], default='read')
    parser.add_argument("--function_code_write", choices=["0x06", "0x10"], default="0x06",
                        help="Specify the function code for writing: 0x06 (single register) or 0x10 (multiple registers)")
    
    return parser.parse_args(cmdline)


