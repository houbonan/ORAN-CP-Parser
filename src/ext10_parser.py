import src.logs as logs

# Section description for group configuration of multiple ports
# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |                                                  extLen = 0x01 (1 word)                                                   |
# |        beamGroupType        |                                numPortc                                                     |
# |                                                        reserved                                                           |

# or

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |                                                        extLen                                                             |
# |        beamGroupType        |                                numPortc                                                     |
# |   reserved   |                                    2nd port beamID[14:8] (or ueID[14:8])                                   |
# |                                         2nd port beamID[14:8] (or ueID[7:0])                                              |
# |   reserved   |                                    3rd port beamID[14:8] (or ueID[14:8])                                   |
# |                                         3rd port beamID[14:8] (or ueID[7:0])                                              |
# |   reserved   |                                                  ......                                                    |
# |                                                          ......                                                           |
# |   reserved   |                       (numPortc+1)th port beamID[14:8] (or ueID[14:8])                                     |
# |                                    (numPortc+1)th port beamID[7:0] (or ueID[7:0])                                         |
# |                                          filler to ensure 4-byte boundary                                                 |


def parse(section):
    extLen = int(section[0], 16)
    logs.add('extLen', str(extLen))

    beamGroupType = int(section[1], 16) >> 6
    logs.add('beamGroupType', str(beamGroupType))

    numPortc = int(section[1], 16) & 0x3F
    logs.add('numPortc', str(numPortc))

    if beamGroupType == 2:
        for i in range(0, numPortc):
            logs.add('port %d beamID [or ueID]' % (i + 1), str(int(section[i * 2 + 2] + section[i * 2 + 3], 16)))

    logs.add('', '')

    return section[extLen * 4 - 1:]
