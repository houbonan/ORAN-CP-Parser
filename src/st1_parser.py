import src.ext_parser as ext_parser
import src.logs as logs

def parse(section, section_idx, section_cnt):
    if section_idx == section_cnt:
        return

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |                                                       sectionId                                                           |
# |                         sectionId                         |     rb       |    symInc    |          startPrbc              |
# |                                                       startPrbc                                                           |
# |                                                        numPrbc                                                            |
# |                                                     reMask[11:4]                                                          |
# |                        reMask[3:0]                        |                        numSymbol                              |
# |      ef      |                                              beamId[14:8]                                                  |
# |                                                     beamId[7:0]                                                           |
# |                                         Section Extensions as indicated by “ef”                                           |
    logs.add('Section Header %d:' % (section_idx), '')
    logs.add('sectionId', str(int(section[0] + section[1], 16) >> 4))
    logs.add('rb', str((int(section[1], 16) >> 3) & 0x1))
    logs.add('symInc', str((int(section[1], 16) >> 2) & 0x1))
    logs.add('startPrbc', str(int(section[1] + section[2], 16) & 0x3FF))
    logs.add('numPrbc', str(int(section[3], 16)))
    logs.add('reMask', '0b' + str(bin(int(section[4] + section[5][0], 16))[2:].zfill(12)))
    logs.add('numSymbol', str(int(section[5], 16) & 0xF))

    ef = (int(section[6], 16) >> 7) & 0x1
    logs.add('ef', str(ef))
    logs.add('beamId', str(int(section[6] + section[7], 16) & 0x7FFF))
    logs.add('', '')

    section = section[8:]

    if ef == 1:
        section = ext_parser.parse(section)

    parse(section, section_idx + 1, section_cnt)