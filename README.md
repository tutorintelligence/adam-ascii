# adam-ascii

[![PyPI version](https://badge.fury.io/py/adam-ascii.svg)](https://badge.fury.io/py/adam-ascii)

stateless asyncio python interface for Advantech 6317 and 6052 modules using the UDP ascii interface.

for TCP modbus communication, see [tcp-modbus-aio](https://github.com/tutorintelligence/tcp-modbus-aio): this is probably a better idea for most ADAM use cases, as TCP is both more reliable and supports more devices.

(note: this project was previously misnamed as `adam-modbus`, but in fact has never communicated via the modbus. whaddayaknow.)