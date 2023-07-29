# Based on factor_vm::load_image in vm/image.cpp
import sys, struct

with open(sys.argv[1], "rb") as f:
    f.seek(-0x10, 2)
    footer = f.read()
    magic, offset = struct.unpack("QQ", footer)
    assert magic == 0x0f0e0d0c
    f.seek(offset, 0)
    header = f.read(0x2f8)
    special_object_count = 85
    magic, version, data_base, data_size, code_base, code_size, _, _, _, _, *special_objects = struct.unpack("Q" * (10 + special_object_count), header)
    assert magic == 0x0f0e0d0c
    data = f.read(data_size)
    code = f.read(code_size)

with open("image.bin", "wb") as f:
    f.write(header + data + code + footer)
# Now you can modify the VM to dump more information