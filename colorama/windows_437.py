# Copyright James Edington Administrator 2025. BSD 3-Clause license, see LICENSE file.

import codecs
from encodings import cp437 as _psf_cp437, normalize_encoding


def _windows_437_search_function(encoding):
    if normalize_encoding(encoding) == 'x_windows_437':
        return _Windows437CodecInfo
    return None

codecs.register(_windows_437_search_function)

# https://github.com/python/cpython/blob/v3.13.2/Lib/encodings/cp437.py#L9
class _Windows437Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,_windows_437_encoding_map)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,_windows_437_decoding_map)

class _Windows437IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,_windows_437_encoding_map)[0]

class _Windows437IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,_windows_437_decoding_map)[0]

class _Windows437StreamWriter(_Windows437Codec,codecs.StreamWriter):
    pass

class _Windows437StreamReader(_Windows437Codec,codecs.StreamReader):
    pass

# https://github.com/python/cpython/blob/v3.13.2/Lib/encodings/cp437.py#L34
_Windows437CodecInfo = codecs.CodecInfo(
    name='x-windows-437',
    encode=_Windows437Codec().encode,
    decode=_Windows437Codec().decode,
    incrementalencoder=_Windows437IncrementalEncoder,
    incrementaldecoder=_Windows437IncrementalDecoder,
    streamreader=_Windows437StreamReader,
    streamwriter=_Windows437StreamWriter,
)


_windows_437_encoding_map = _psf_cp437.encoding_map | {
  0x263a: 0x01,
  0x263b: 0x02,
  0x2665: 0x03,
  0x2666: 0x04,
  0x2663: 0x05,
  0x2660: 0x06,
  0x25cb: 0x09,
  0x2642: 0x0b,
  0x2640: 0x0c,
  0x266b: 0x0e,
  0x263c: 0x0f,
  0x25ba: 0x10,
  0x25c4: 0x11,
  0x2195: 0x12,
  0x203c: 0x13,
  0x00b6: 0x14,
  0x00a7: 0x15,
  0x25ac: 0x16,
  0x21a8: 0x17,
  0x2191: 0x18,
  0x2193: 0x19,
  0x2192: 0x1a,
  0x2190: 0x1b,
  0x221f: 0x1c,
  0x2194: 0x1d,
  0x25b2: 0x1e,
  0x25bc: 0x1d,
}


_windows_437_decoding_map = _psf_cp437.decoding_map | {
  0x01: 0x263a,
  0x02: 0x263b,
  0x03: 0x2665,
  0x04: 0x2666,
  0x05: 0x2663,
  0x06: 0x2660,
  0x09: 0x25cb,
  0x0b: 0x2642,
  0x0c: 0x2640,
  0x0e: 0x266b,
  0x0f: 0x263c,
  0x10: 0x25ba,
  0x11: 0x25c4,
  0x12: 0x2195,
  0x13: 0x203c,
  0x14: 0x00b6,
  0x15: 0x00a7,
  0x16: 0x25ac,
  0x17: 0x21a8,
  0x18: 0x2191,
  0x19: 0x2193,
  0x1a: 0x2192,
  0x1b: 0x2190,
  0x1c: 0x221f,
  0x1d: 0x2194,
  0x1e: 0x25b2,
  0x1d: 0x25bc,
}
