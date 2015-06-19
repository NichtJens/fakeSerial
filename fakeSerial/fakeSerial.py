
import random, string

def rndText(letters=15, lines=3, spaces=5):
    return "\n".join("".join((random.choice(string.letters + ' ' * spaces) for _ in xrange(letters))) for _ in xrange(lines))


RESET = '\x1b[0m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = ['\x1b[1;{}m'.format(30+i) for i in range(8)]



import serial as realSerial


class Serial(object):

    def __init__(self, port=None, baudrate=9600, bytesize=realSerial.EIGHTBITS,
                 parity=realSerial.PARITY_NONE, stopbits=realSerial.STOPBITS_ONE,
                 timeout=None, xonxoff=False, rtscts=False, writeTimeout=None,
                 dsrdtr=False, interCharTimeout=None):

        self.port             = port
        self.baudrate         = baudrate
        self.bytesize         = bytesize
        self.parity           = parity
        self.stopbits         = stopbits
        self.timeout          = timeout
        self.xonxoff          = xonxoff
        self.rtscts           = rtscts
        self.writeTimeout     = writeTimeout
        self.dsrdtr           = dsrdtr
        self.interCharTimeout = interCharTimeout

        self.BAUDRATES = realSerial.Serial.BAUDRATES
        self.BYTESIZES = realSerial.Serial.BYTESIZES
        self.PARITIES  = realSerial.Serial.PARITIES
        self.STOPBITS  = realSerial.Serial.STOPBITS

        self._isOpen  = True if port is not None else False
        self.dataIn  = ""
        self.dataOut = rndText()
        self.debug   = True

        self.log("Created:\n{}".format(self))


    def __str__(self):
        """Return a string representation mimicking that of the serial class"""

        data = (hex(id(self)), self._isOpen)
        head = "id={}, open={}".format(*data)

        data = (self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.timeout, self.xonxoff, self.rtscts, self.dsrdtr)
        data = map(repr, data)
        body = "port={}, baudrate={}, bytesize={}, parity={}, stopbits={}, timeout={}, xonxoff={}, rtscts={}, dsrdtr={}".format(*data)

        return "Serial<{}>({})".format(head, body)


    __repr__ = __str__ # Return str(self), like the serial class


    def open(self):
        """
        Open the port
        Actually sets the state variable _isOpen to True
        """
        self.log("open")
        self._isOpen = True

    def close(self):
        """
        Close the port
        Actually sets the state variable _isOpen to False
        """
        self.log("close")
        self._isOpen = False

    def isOpen(self):
        """
        Test if the port is open
        Actually tests the state variable _isOpen
        """
        self.log("port is {}".format(self.state))
        return self._isOpen


    def write(self, data):
        """
        Write data to the port
        Actually appends data to dataIn
        """
        self.raiseIfClosed()
        self.log('write: "{}"'.format(data), color=GREEN)
        self.dataIn += data

    def writelines(self, sequence):
        """Write a list of strings to the port"""
        self.log("writelines")
        for s in sequence:
            self.write(s)

    def read(self, size=1):
        """
        Read and return size bytes from the port
        Actually, the bytes are read from dataOut
        """
        self.raiseIfClosed()
        data, self.dataOut = self.dataOut[:size], self.dataOut[size:]
        self.log('read: "{}"'.format(data), color=RED)
        return data

    def readline(self, limit=None, eol='\n'):
        """
        Read and return a line from the port
        If limit is specified, at most limit bytes will be read
        The recognized line terminator(s) can be set via newlines
        Actually, the line is read from dataOut
        """
        self.raiseIfClosed()
        size = min((self.dataOut.index(nl) for nl in eol))

        if size == -1:
            return ""

        size += 1
        if limit is not None:
            size = min(size, limit)

        data, self.dataOut = self.dataOut[:size], self.dataOut[size:]
        self.log('readline: "{}"'.format(data.rstrip(eol)), color=RED)
        return data


    next = readline # Return the next line, like the serial class
    __iter__ = lambda self: self


    def inWaiting(self):
        """
        Return the number of chars in the receive buffer
        Actually returns length of dataOut
        """
        self.log("inWaiting")
        return len(dataOut)

    def outWaiting(self):
        """
        Return the number of chars in the output buffer
        Actually returns length of dataIn
        """
        self.log("outWaiting")
        return len(dataIn)

    def flushInput(self):
        """
        Clear input buffer
        Actually discards content of dataIn
        """
        self.dataIn = ""
        self.log("flushInput")

    def flushOutput(self):
        """
        Clear output buffer
        Actually discards content of dataOut
        """
        self.dataOut = ""
        self.log("flushOutput")

    def readinto(self, b):
        """
        Read up to len(b) bytes into bytearray b and return the number of bytes read
        Actually, reads from dataOut
        """
        size = len(b)
        b, self.dataOut = self.dataOut[:size], self.dataOut[size:]
        self.log('readinto: "{}"'.format(b), color=RED)
        return size


    # the following methods do nothing but log
    flush             = lambda self: self.log("flush")
    nonblocking       = lambda self: self.log("nonblocking")
    rtsToggle         = lambda self: self.log("rtsToggle")
    getSettingsDict   = lambda self: self.log("getSettingsDict")
    applySettingsDict = lambda self, d: self.log("applySettingsDict")
    setBreak          = lambda self, level=True: self.log("setBreak")
    setDTR            = lambda self, level=True: self.log("setDTR")
    setRTS            = lambda self, level=True: self.log("setRTS")
    setXON            = lambda self, level=True: self.log("setXON")
    flowControlOut    = lambda self, enable: self.log("flowControlOut")

    # should these raise IOError?
    isatty            = lambda self: self.log("isatty")
    tell              = lambda self: self.log("tell")
    seek              = lambda self, pos, whence=0: self.log("seek")
    truncate          = lambda self, n=None: self.log("truncate")

    # should these sleep?
    sendBreak         = lambda self, duration=0.25: self.log("sendBreak")
    readlines         = lambda self, sizehint=None, eol='\n': self.log("readlines")
    xreadlines        = lambda self, sizehint=None: self.log("xreadlines")


    # the following methods log and always return True/False

    def getCTS(self):
        self.log("getCTS")
        return True

    def getDSR(self):
        self.log("getDSR")
        return True

    def getRI(self):
        self.log("getRI")
        return True

    def getCD(self):
        self.log("getCD")
        return True

    def readable(self):
        self.log("readable")
        return True

    def writable(self):
        self.log("writable")
        return True

    def seekable(self):
        self.log("seekable")
        return False

    def fileno(self):
        self.log("fileno")
        return 1


    # the following methods are not part of the real serial

    def log(self, string, color=BLUE):
        """Print debugging log"""
        if self.debug:
            print color + string + RESET

    @property
    def state(self):
        """Return state of the port as string ("open"/"closed")"""
        if self._isOpen:
            return "open"
        else:
            return "closed"

    def raiseIfClosed(self):
        """Raise ValueError if port is closed"""
        if not self._isOpen:
            raise ValueError



