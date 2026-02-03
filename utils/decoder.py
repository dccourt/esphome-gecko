import hexdump
import importlib

from config import (
    GeckoAsyncStructure,
    GeckoBoolStructAccessor,
    GeckoByteStructAccessor,
    GeckoEnumStructAccessor,
    GeckoStructAccessor,
    GeckoTempStructAccessor,
    GeckoTimeStructAccessor,
    GeckoWordStructAccessor,
)

class StructParser:
    """Decoder for GeckoAsyncStructures."""

    def __init__(self, filename, classname):
        StructClass = importlib.import_module("config." + filename)
        self.instance = getattr(StructClass, classname)(None)
        self.position_to_info = {}  # position -> accessor list at that position
        self.max_position = None

        for accessor in self.instance.accessors.values():
            position = accessor.position
            if position not in self.position_to_info:
                self.position_to_info[position] = []
            self.position_to_info[position].append(accessor)
            if self.max_position is None or position > self.max_position:
                self.max_position = position

    def get_accessors_for_position(self, position):
        """Get the accessor for a given position."""
        return self.position_to_info.get(position, None)

    def decode_data(self, data_hex, dump_immediately=False, adjust_offset=0):
        """Decode the given data bytes (presented as hex string)."""
        decoded_values = {}

        data_bytes = bytes.fromhex(data_hex)

        print(f"Data length: {len(data_bytes)} bytes")
        print("          00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F")
        hexdump.hexdump(data_bytes)

        for index in range(len(data_bytes)):
            # Hack to make known values align
            adjusted_index = index + adjust_offset

            # These hack affects config only.
            if adjusted_index >= 64:
                adjusted_index -= 3

            if adjusted_index >= 164:
                adjusted_index += 3

            if adjusted_index >= 284:
                adjusted_index -= 3

            if adjusted_index >= 372:
                adjusted_index -= 3
            # Not quite right - we repeat UdAux, but it's close.

            # No point in going past the position definitions we have
            if adjusted_index > self.max_position:
                break

            if adjusted_index in self.position_to_info:
                accessors = self.position_to_info[adjusted_index]
                for accessor in accessors:
                    value = accessor.decode(data_bytes, index)
                    decoded_values[accessor.path] = value
                    if dump_immediately:
                        print(f"At byte {index:04x}->{adjusted_index:04x}: {accessor.path} = {value}")
        return decoded_values

config_plus_log_hex = "000013024904000006000000060003010C0B000000000000000000000E00000000000101011E0F07000100000000000000000000110001281E3C3C0128CA003B02041200280073010E02D00001040100000100020F02F500020002010103030305050404010306140F180F0F14060606060606F0011000010000002200761E011E000A3040800083000000000100000004000000000000000000000000000000000000000000000000000002FE170A000000170A010001000001060701C0010203040507090B0C1011121314781579187C197D1F2021222325262728FFFF3B01000E0000000C000504060000000000FFFFFF03000249024900000000000000400E000A4B003D36004141019C0800001E00000000000000000384000074013B0000024B00000000000000000000000000000000000000000000000000000000000000000000000001830800752100000000FF730000000009C914710176000000000000000000020000000000007FFF27"
# Skip the first 4 characters (2 bytes) of header
config_plus_log_hex = config_plus_log_hex[4:]

print("\nDecoding config structure:")
CfgStruct = StructParser("inyt-cfg-65", "GeckoConfigStruct")
CfgStruct.decode_data(
    config_plus_log_hex,
    dump_immediately=True)

print("\nDecoding log structure:")
LogStruct = StructParser("inyt-log-65", "GeckoLogStruct")
LogStruct.decode_data(
    config_plus_log_hex,
    dump_immediately=True,
    adjust_offset=33)
