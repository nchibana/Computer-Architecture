"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value


    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(2)
        
        filename = sys.argv[1]

        with open(filename) as file:
            for line in file:
                comment_split = line.split("#")
                number_string = comment_split[0].strip()

                if number_string == '':
                    continue

                num = int(number_string, 2)
                # print("{:08b} is {:d}".format(num, num))
                # print(f"{num:>08b} is {num:>0d}")
                self.ram[address] = num
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running is True:
        
            command = self.ram_read(self.pc)
            operand_A = self.ram_read(self.pc + 1)
            operand_B = self.ram_read(self.pc + 2)
        
            if command == 0b10000010: #LDI
                self.reg[operand_A] = operand_B
                self.pc += ( command >> 6 ) + 1
        
            elif command == 0b01000111: #PRN
                print(self.reg[operand_A])
                self.pc += ( command >> 6 ) + 1

            elif command == 0b10100010: #MUL
                self.reg[operand_A] = self.reg[operand_A] * self.reg[operand_B]
                self.pc += ( command >> 6 ) + 1
        
            elif command == 0b00000001: #HLT
                running = False
        
            else:
                print("Error!")
                sys.exit(1)

