from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer
import logging
import helper  
import struct

# Define endianness conversion functions
def to_big_endian(value):
    return struct.unpack('>H', struct.pack('H', value))[0]

def to_little_endian(value):
    little_endian_value = struct.unpack('<H', struct.pack('H', value))[0]
    return little_endian_value

def to_mixed_endian(value):
    high_byte = (value & 0xFF00) >> 8
    low_byte = (value & 0x00FF)
    mixed_value = (low_byte << 8) | high_byte
    return mixed_value

# Parse command-line arguments
args = helper.get_commandline(description="Modbus TCP/RTU Client")

# Enable logging based on the command-line argument
logging.basicConfig()
log = logging.getLogger()   
log.setLevel(getattr(logging, args.log.upper()))

# Configuration settings from parsed arguments
ip_address = args.host
port = args.port
slave_id = args.slave_id
register_address = args.address
value_to_write = args.value
values_to_write = args.values
endian = args.endian
count = args.count
register_type = args.register_type
function = args.function
function_code_write = args.function_code_write
baudrate=args.baudrate
timeout=args.timeout 

# Choose the correct client based on the communication type
if args.comm == "tcp":
    client = ModbusTcpClient(ip_address, port=port)
elif args.comm == "rtu_tcp":
    client = ModbusTcpClient(ip_address, port=port, framer=ModbusRtuFramer)
elif args.comm == "serial":
    client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
else:
    raise ValueError(f"Unsupported communication type: {args.comm}")

# Define functions for reading and writing with endianness handling
def read_holding_registers(client, register_address, count, slave_id, endian='big'):
    try:
        result = client.read_holding_registers(register_address, count, slave_id)
        if result.isError():
            log.warning(f"Error reading registers: {result}")
            return []
        values = result.registers
        if endian == 'little':
            return [to_little_endian(val) for val in values]
        elif endian == 'mixed':
            return [to_mixed_endian(val) for val in values]
        elif endian == 'big':
            return [to_big_endian(val) for val in values]
    except Exception as e:
        log.warning(f"Ignoring CRC error or other issue: {e}")
        return []  # Proceed with empty list if error

def write_holding_register(client, register_address, value_to_write, slave_id, endian='big'):
    try:
        if endian == 'little':
            value_to_write = to_little_endian(value_to_write)
        elif endian == 'mixed':
            value_to_write = to_mixed_endian(value_to_write)
        elif endian == 'big':
            value_to_write = to_big_endian(value_to_write)
        result = client.write_register(register_address, value_to_write, slave_id) 
        if result.isError():
            log.warning(f"Error writing register: {result}")
        return result
    except Exception as e:
        log.warning(f"Ignoring CRC error or other issue: {e}")

def write_multiple_holding_registers(client, register_address, values_to_write, slave_id, endian='big'):
    try:
        if endian == 'little':
            values_to_write = [to_little_endian(val) for val in values_to_write]
        elif endian == 'mixed':
            values_to_write = [to_mixed_endian(val) for val in values_to_write]
        elif endian == 'big':
            values_to_write = [to_big_endian(val) for val in values_to_write]

        result = client.write_registers(register_address, values_to_write, slave_id)
        if result.isError():
            log.warning(f"Error writing registers: {result}")
        return result
    except Exception as e:
        log.warning(f"Ignoring CRC error or other issue: {e}")

# Additional read/write functions follow the same pattern...

if client.connect():
    try:
        if function == 'write':
            if register_type == 'holding':
                if function_code_write == "0x06":
                    # Write a single register
                    write_holding_register(client, register_address, value_to_write, slave_id, endian)
                    print(f"Value {value_to_write} written to register {register_address} with {endian} endian, function code 0x06.")
                elif function_code_write == "0x10":
                    # Write multiple registers
                    write_multiple_holding_registers(client, register_address, values_to_write, slave_id, endian)
                    print(f"Values {values_to_write} written to register {register_address} with {endian} endian, function code 0x10.")

        elif function == 'read':
            if register_type == 'holding':
                result = read_holding_registers(client, register_address, count, slave_id, endian)
                for i, val in enumerate(result):
                    print(f"Read value from holding register {register_address + i}: {val} with {endian} endian.")
            # Additional read cases for other register types...

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
else:
    print("Failed to connect to the Modbus server")
