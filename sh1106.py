from machine import I2C


class SH1106:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr

        self.pages = height // 8
        self.buffer = bytearray(width * self.pages)

        self.init_display()

    def command(self, cmd):
        self.i2c.writeto(
            self.addr,
            bytearray([0x00, cmd])
        )

    def init_display(self):
        commands = (
            0xAE,       # Display OFF
            0xD5, 0x80, # Clock
            0xA8, 0x3F, # Multiplex
            0xD3, 0x00, # Display offset
            0x40,       # Start line
            0xAD, 0x8B, # Charge pump
            0xA1,       # Segment remap
            0xC8,       # COM scan direction
            0xDA, 0x12, # COM pins
            0x81, 0x80, # Contrast
            0xD9, 0x1F, # Pre-charge
            0xDB, 0x40, # VCOM
            0xA4,       # Display follows RAM
            0xA6,       # Normal display
            0xAF        # Display ON
        )

        for cmd in commands:
            self.command(cmd)

        self.fill(0)
        self.show()

    def fill(self, color):
        value = 0xFF if color else 0x00

        for i in range(len(self.buffer)):
            self.buffer[i] = value

    def pixel(self, x, y, color=1):

        if x < 0 or x >= self.width:
            return

        if y < 0 or y >= self.height:
            return

        index = x + (y // 8) * self.width
        mask = 1 << (y & 7)

        if color:
            self.buffer[index] |= mask
        else:
            self.buffer[index] &= ~mask

    def show(self):

        for page in range(self.pages):

            self.command(0xB0 + page)
            self.command(0x02)
            self.command(0x10)

            start = page * self.width
            end = start + self.width

            self.i2c.writeto(
                self.addr,
                bytearray([0x40]) +
                self.buffer[start:end]
            )

    def line(self, x1, y1, x2, y2, color=1):

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy

        while True:

            self.pixel(x1, y1, color)

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x1 += sx

            if e2 < dx:
                err += dx
                y1 += sy