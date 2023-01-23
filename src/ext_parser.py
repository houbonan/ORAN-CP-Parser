import src.ext1_parser as ext1_parser
import src.ext2_parser as ext2_parser
import src.ext3_parser as ext3_parser
import src.ext4_parser as ext4_parser
import src.ext5_parser as ext5_parser
import src.ext6_parser as ext6_parser
import src.ext7_parser as ext7_parser
import src.ext8_parser as ext8_parser
import src.ext9_parser as ext9_parser
import src.ext10_parser as ext10_parser
import src.ext11_parser as ext11_parser
import src.ext12_parser as ext12_parser
import src.ext13_parser as ext13_parser
import src.ext14_parser as ext14_parser
import src.ext15_parser as ext15_parser
import src.ext16_parser as ext16_parser
import src.ext17_parser as ext17_parser
import src.ext18_parser as ext18_parser
import src.logs as logs

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |     ef       |                                                extType                                                     |
def parse(section):
    ef = (int(section[0], 16) >> 7) & 0x1
    extType = int(section[0], 16) & 0x7F
    logs.add('ef', str(ef))
    logs.add('extType', str(extType))

    if extType == 1:
        section = ext1_parser.parse(section[1:])
    elif extType == 2:
        section = ext2_parser.parse(section[1:])
    elif extType == 3:
        section = ext3_parser.parse(section[1:])
    elif extType == 4:
        section = ext4_parser.parse(section[1:])
    elif extType == 5:
        section = ext5_parser.parse(section[1:])
    elif extType == 6:
        section = ext6_parser.parse(section[1:])
    elif extType == 7:
        section = ext7_parser.parse(section[1:])
    elif extType == 8:
        section = ext8_parser.parse(section[1:])
    elif extType == 9:
        section = ext9_parser.parse(section[1:])
    elif extType == 10:
        section = ext10_parser.parse(section[1:])
    elif extType == 11:
        section = ext11_parser.parse(section[1:])
    elif extType == 12:
        section = ext12_parser.parse(section[1:])
    elif extType == 13:
        section = ext13_parser.parse(section[1:])
    elif extType == 14:
        section = ext14_parser.parse(section[1:])
    elif extType == 15:
        section = ext15_parser.parse(section[1:])
    elif extType == 16:
        section = ext16_parser.parse(section[1:])
    elif extType == 17:
        section = ext17_parser.parse(section[1:])
    elif extType == 18:
        section = ext18_parser.parse(section[1:])

    if ef == 1:
        section = parse(section)

    return section