"""Module Initialization, includes dummy accessors."""

# Dummy classes for Gecko accessors
class GeckoAsyncStructure:
    """Dummy class to store constructor parameters."""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class GeckoStructAccessor:
    """Dummy base class to store constructor parameters."""
    def __init__(self, struct, path, position, access):
        self.struct = struct
        self.path = path
        self.position = position
        self.access = access

    def __repr__(self):
        return (f"{self.__class__.__name__}(struct={self.struct}, path={self.path}, "
                f"position={self.position}, access={self.access})")
    
    def __str__(self):
        return self.path

class GeckoBoolStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, bit, access):
        super().__init__(struct, path, position, access)
        self.bit = bit

    def decode(self, bytes, index):
        # extract the bit from the byte at position
        byte_value = bytes[index]
        return (byte_value & (1 << self.bit)) != 0

class GeckoByteStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, access):
        super().__init__(struct, path, position, access)

    def decode(self, bytes, index):
        # simple - we just want the byte value.
        return bytes[index]

class GeckoEnumStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, bitpos, values, size, maxitems, access):
        super().__init__(struct, path, position, access)
        self.bitpos = bitpos
        self.values = values
        self.size = size
        self.maxitems = maxitems

    def decode(self, bytes, index):
        # Dereference the value list using a single byte value as array index
        data = bytes[index]
        rawdata = data
        if self.bitpos is not None:
            data = (data >> self.bitpos) 
        if self.maxitems is not None:
            data = data & (self.maxitems - 1)
        try:
            assert self.values is not None
            data = self.values[data]
        except IndexError:
            print(
                "Enum accessor %s out-of-range for %s. Value is %s (raw byte:%s). Position is %d." % (
                    self.path,
                    self.values,
                    data,
                    rawdata,
                    self.position
                )
            )
            print("bitpos:", self.bitpos, " maxitems:", self.maxitems)
            data = "Unknown"
        return data

class GeckoTempStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, access):
        super().__init__(struct, path, position, access)

    def decode(self, bytes, index):
        # take big-endian 2-byte word, divide by 18.0 for Celsius
        value = bytes[index + 1] + (bytes[index] << 8)
        return str(value / 18.0) + " °C"

class GeckoTimeStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, access):
        super().__init__(struct, path, position, access)

    def decode(self, bytes, index):
        # take two bytes, represent as HH:MM
        hours = bytes[index]
        minutes = bytes[index + 1]
        return f"{hours:02}:{minutes:02}"

class GeckoWordStructAccessor(GeckoStructAccessor):
    """Dummy class to store constructor parameters."""
    def __init__(self, struct, path, position, access):
        super().__init__(struct, path, position, access)

    def decode(self, bytes, index):
        # take big-endian 2-byte word
        value = bytes[index + 1] + (bytes[index] << 8)
        return value

__all__ = [
    "GeckoAsyncStructure",
    "GeckoBoolStructAccessor",
    "GeckoByteStructAccessor",
    "GeckoEnumStructAccessor",
    "GeckoStructAccessor",
    "GeckoTempStructAccessor",
    "GeckoTimeStructAccessor",
    "GeckoWordStructAccessor",
]
