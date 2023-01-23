import src.logs as logs

# Dynamic Spectrum Sharing parameters
# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |                                                  extLen = 0x01 (1 word)                                                   |
# |                                                    technology[7:0]                                                        |
# |                                                        reserved                                                           |

def parse(section):
    logs.add('extLen', str(int(section[0], 16)))
    logs.add('technology', str(int(section[1], 16)))
    logs.add('', '')

    return section[3:]

