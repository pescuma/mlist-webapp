import StringIO
import struct
from zlib import decompressobj

def getSWFSize(f):
    magic, version, datasz = struct.unpack("<3s1B1L", f.read(8))
    if ( magic != 'FWS' and magic != 'CWS' ) or datasz < 9:
		raise "Invalid format"
    datasz -= 8
    if magic == 'FWS':
        data = f.read(min(datasz, 32))
    else:
        d = decompressobj()
        data = ''
        while len( data ) < min(datasz, 32):
            data += d.decompress(f.read(64))
    data = struct.unpack('%dB' % len(data), data)
    nbits = data[0] >> 3
    coord = {}
    q = 0
    r = 5
    for p in ('sx', 'ex', 'sy', 'ey'):
        c = nbits
        v = 0
        while c > 8:
            v <<= 8
            v |= (data[q] << r) & 0xff
            c -= 8
            q += 1
            v |= data[q] >> (8 - r)
        m = min(c, 8)
        v <<= m
        r = m - (8 - r)
        if r > 0:
            v |= (data[q] << r) & 0xff
            q += 1
            v |= data[q] >> (8 - r)
        else:
            v |= (data[q] >> -r) & ((1 << m) - 1)
            r = 8 + r
        coord[p] = v
    return int(float(coord['ex'] - coord['sx']) / 20), int(float(coord['ey'] - coord['sy']) / 20)


def getImageInfo(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO.StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass
    
    # handle SWF
    elif (size >= 28) and data[:3] in ('FWS', 'CWS'):
        try:
	        width, height = getSWFSize(StringIO.StringIO(data))
	        content_type = 'application/x-shockwave-flash'
        except:
	        pass


    return content_type, width, height
