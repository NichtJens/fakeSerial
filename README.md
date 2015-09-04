# fakeSerial
 A Python module emulating the serial module

---

Replacing

```python
import serial
```

with

```python
import fakeSerial as serial
```

gives a drop-in replacement for the `serial.Serial` class.

It tries to emulate (and log) most interactions with a serial port. For instance, it stores the open/close state internally, and thus allows opening and closing a port, as well as testing this state via `Serial.isOpen()`. Data written via `Serial.write()` etc. is stored internally, too. Reading via e.g. `Serial.read()` returns random text.