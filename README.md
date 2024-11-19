---

# Complete Modbus Communication
Supports Modbus RTU over TCP/IP, Modbus TCP, and Serial Communication

## Description
A personalized script for reading and writing Modbus registers, with a focus on Modbus RTU over TCP/IP communication. Supports Modbus TCP, RTU over TCP, and Serial communication types.

This script allows reading and writing Modbus registers with customizable endianness settings.

- **Input Registers** and **Discrete Input Registers** are read-only.
- **Holding Registers** and **Coils** can be both read and written.

## Author
rashidobaid9@gmail.com

## Date
2024-06-04

## Copyright
MPL 2.0

## Installation

1. Install `pymodbus`:
   ```bash
   pip install pymodbus
   ```

2. Download this repository, navigate to the folder in the terminal, and run the script as shown in the examples below (adjust parameters as needed).

### Examples

### For Serial RTU (using COM ports):

Read up to 50 registers at once. Reading more than 90 registers at once may not work, though up to 125 registers can typically be read using TCP.

```bash
python modbus_read_write.py --comm serial --port COM6 --baudrate 9600 --log debug --slave_id 1 --address 1100 --function read --register_type holding --count 50 --endian little
```

Write registers using function code 16 (`0x10`) for multiple registers (default function code is `0x06`):

```bash
python modbus_read_write.py --comm serial --port COM6 --baudrate 9600 --log debug --slave_id 1 --address 166 --function write --register_type holding --count 1 --endian little --values 60 --function_code_write 0x10
```

### For RTU over TCP/IP

**Note**: Adjust parameters as required (e.g., `host`, `port`, `address`).

Read Holding Registers:

```bash
python modbus_read_write.py --comm rtu_tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 128 --endian little --function read
```

Write to a Holding Register:

```bash
python modbus_read_write.py --comm rtu_tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 128 --endian little --function write --value 1
```

### For TCP Communication:

Read Holding Registers:

```bash
python modbus_read_write.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function read --register_type holding --endian little --count 10
```

Read Coils:

```bash
python modbus_read_write.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function read --register_type coil --count 10
```

Read Input Registers:

```bash
python modbus_read_write.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 2 --function read --register_type input --endian little --count 1
```

Write to a Holding Register:

```bash
python modbus_read_write.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function write --value 10000 --register_type holding --endian little --count 1
```

Write to a Coil:

```bash
python modbus_read_write.py --comm tcp --host 127.0.0.1 --port 502 --log debug --slave_id 1 --address 3 --function write --value 1 --register_type coil --count 1
```

## Usage
The script supports three types of communication: `tcp`, `rtu_tcp` (RTU over TCP), and `serial`. Adjust arguments as needed based on the communication type and device configuration. 

--- 
