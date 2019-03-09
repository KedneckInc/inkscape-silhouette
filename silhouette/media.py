import pkg_resources
import ast
from collections import namedtuple

MediaType =  namedtuple('MediaType', [ 'pressure', 'speed', 'cap_color', 'name' ] )

class Media:
    
    def __init__(self, *args, **kw):
        defaults = pkg_resources.resource_filename(__name__,"media.dat")
        self._elements = {}
        with open(defaults,'r') as f:
            s = f.read()
            h = ast.literal_eval(s)
            for (k,(p,s,c,n)) in h.items():
                self._elements[k] = MediaType(p,s,c,n)
    def __getitem__(self, key):
        return self._elements[key]
    def items(self):
        return self._elements.items()
    def __len__(self):
        return len(self._elements)
    
    # MEDIA = {
    #     100: (   27,     10,  "yellow", "Card without Craft Paper Backing"),
    #     101: (   27,     10,  "yellow", "Card with Craft Paper Backing"),
    #     102: (   10,     10,  "blue",   "Vinyl Sticker"),
    #     106: (   14,     10,  "blue",   "Film Labels"),
    #     111: (   27,     10,  "yellow", "Thick Media"),
    #     112: (    2,     10,  "blue",   "Thin Media"),
    #     113: (   10,     10,  "pen",    "Pen"),
    #     120: (   30,     10,  "blue",   "Bond Paper 13-28 lbs (105g)"),
    #     121: (   30,     10,  "yellow", "Bristol Paper 57-67 lbs (145g)"),
    #     122: (   30,     10,  "yellow", "Cardstock 40-60 lbs (90g)"),
    #     123: (   30,     10,  "yellow", "Cover 40-60 lbs (170g)"),
    #     124: (    1,     10,  "blue",   "Film, Double Matte Translucent"),
    #     125: (    1,     10,  "blue",   "Film, Vinyl With Adhesive Back"),
    #     126: (    1,     10,  "blue",   "Film, Window With Kling Adhesive"),
    #     127: (   30,     10,  "red",    "Index 90 lbs (165g)"),
    #     128: (   20,     10,  "yellow", "Inkjet Photo Paper 28-44 lbs (70g)"),
    #     129: (   27,     10,  "red",    "Inkjet Photo Paper 45-75 lbs (110g)"),
    #     130: (   30,      3,  "red",    "Magnetic Sheet"),
    #     131: (   30,     10,  "blue",   "Offset 24-60 lbs (90g)"),
    #     132: (    5,     10,  "blue",   "Print Paper Light Weight"),
    #     133: (   25,     10,  "yellow", "Print Paper Medium Weight"),
    #     134: (   20,     10,  "blue",   "Sticker Sheet"),
    #     135: (   20,     10,  "red",    "Tag 100 lbs (275g)"),
    #     136: (   30,     10,  "blue",   "Text Paper 24-70 lbs (105g)"),
    #     137: (   30,     10,  "yellow", "Vellum Bristol 57-67 lbs (145g)"),
    #     138: (   30,     10,  "blue",   "Writing Paper 24-70 lbs (105g)"),
    #     300: ( None,   None,  "custom", "Custom"),
    # }
    # MEDIA = [
    #     # CAUTION: keep in sync with sendto_silhouette.inx
    #     # media, pressure, speed, cap-color, name
    #     ( 100,   27,     10,  "yellow", "Card without Craft Paper Backing"),
    #     ( 101,   27,     10,  "yellow", "Card with Craft Paper Backing"),
    #     ( 102,   10,     10,  "blue",   "Vinyl Sticker"),
    #     ( 106,   14,     10,  "blue",   "Film Labels"),
    #     ( 111,   27,     10,  "yellow", "Thick Media"),
    #     ( 112,    2,     10,  "blue",   "Thin Media"),
    #     ( 113,   10,     10,  "pen",    "Pen"),
    #     ( 120,   30,     10,  "blue",   "Bond Paper 13-28 lbs (105g)"),
    #     ( 121,   30,     10,  "yellow", "Bristol Paper 57-67 lbs (145g)"),
    #     ( 122,   30,     10,  "yellow", "Cardstock 40-60 lbs (90g)"),
    #     ( 123,   30,     10,  "yellow", "Cover 40-60 lbs (170g)"),
    #     ( 124,    1,     10,  "blue",   "Film, Double Matte Translucent"),
    #     ( 125,    1,     10,  "blue",   "Film, Vinyl With Adhesive Back"),
    #     ( 126,    1,     10,  "blue",   "Film, Window With Kling Adhesive"),
    #     ( 127,   30,     10,  "red",    "Index 90 lbs (165g)"),
    #     ( 128,   20,     10,  "yellow", "Inkjet Photo Paper 28-44 lbs (70g)"),
    #     ( 129,   27,     10,  "red",    "Inkjet Photo Paper 45-75 lbs (110g)"),
    #     ( 130,   30,      3,  "red",    "Magnetic Sheet"),
    #     ( 131,   30,     10,  "blue",   "Offset 24-60 lbs (90g)"),
    #     ( 132,    5,     10,  "blue",   "Print Paper Light Weight"),
    #     ( 133,   25,     10,  "yellow", "Print Paper Medium Weight"),
    #     ( 134,   20,     10,  "blue",   "Sticker Sheet"),
    #     ( 135,   20,     10,  "red",    "Tag 100 lbs (275g)"),
    #     ( 136,   30,     10,  "blue",   "Text Paper 24-70 lbs (105g)"),
    #     ( 137,   30,     10,  "yellow", "Vellum Bristol 57-67 lbs (145g)"),
    #     ( 138,   30,     10,  "blue",   "Writing Paper 24-70 lbs (105g)"),
    #     ( 300, None,   None,  "custom", "Custom"),
    # ]

if __name__ == '__main__':
    media = Media();
    # The idea here is that this code can generate the XML snippet
    # needed in the sendto_sihlouette.inx file, so we don't have to
    # worry so hard about keeping them in sync.  I'm undecided whether
    # this code should generate the entire inx file or just the media
    # portion of it.  Either way, this output can be used.
    
    for (idx, ( pressure, speed, color, name )) in media.items():
        if not speed:
            speed = "S>0"
        else:
            speed = "S=%2i" % speed;
        if not pressure:
            pressure = "P>0"
        else:
            pressure = "P=%2i" % pressure
        print("<item value=\"%i\">[%s,%s] %s</item>" % (idx, pressure, speed, name) );
