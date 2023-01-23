import src.ext_parser as ext_parser
import src.logs as logs

NO_COMPRESSION = 0
BLOCK_FLOATING_POINT = 1
BLOCK_SCALING = 2
U_LAW = 3

ANT_NUM = 16

def parse(section, section_idx, section_cnt, ciIqWidth, ciCompMeth, ciCompOpt):
    if section_idx == section_cnt:
        return

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |      ef      |                                              ueId[14:8]                                                    |
# |                                                      ueId[7:0]                                                            |
# |                                                   regularizationFactor                                                    |
# |                         reserved                          |     rb       |    symInc    |          startPrbc              |
# |                                                       startPrbc                                                           |
# |                                                        numPrbc                                                            |
# |                          ciCompParam (for the first PRB or all PRBs of the first UE, not always present)                  |
# |                                         ciIsample (first PRB, first antenna)                                              |
# |                                         ciQsample (first PRB, first antenna)                                              |
# |                                         ciIsample (first PRB, second antenna)                                             |
# |                                         ciQsample (first PRB, second antenna)                                             |
# |                                                         ......                                                            |
# |                                         Section Extensions as indicated by “ef”                                           |
    ef = (int(section[0], 16) >> 7) & 0x1
    logs.add('ef', str(ef))

    logs.add('beamId', str(int(section[0] + section[1], 16) & 0x7FFF))
    logs.add('regularizationFactor', str(int(section[2], 16)))
    logs.add('rb', str((int(section[3], 16) >> 3) & 0x1))
    logs.add('symInc', str((int(section[3], 16) >> 2) & 0x1))

    startPrbc = int(section[3] + section[4], 16) & 0x3FF
    logs.add('startPrbc', str(startPrbc))
    numPrbc = int(section[5], 16)
    logs.add('numPrbc', str(numPrbc))

# for ciCompParam, if ciCompOpt=0, only ciCompParam for all PRBs, if ciCompOpt=1, per ciCompParam per PRB
#                           | 0 (MSB) |    1    |    2    |    3    |    4    |    5    |    6    | 7 (LSB) |
# 000b = no compression     |                                    absent                                     |  0 octet
# 001b = block fl.point     |       reserved(set to all zeros)      |          Exponent(unsigned)           |  1 octet
# 010b = block scaling      |             blockScaler(unsigned, 1integer bit, 7 fractional bits)            |  1 octet
# 011b = u-law              |             compBitWidth              |               compShift               |  1 octet
    byte_cnt = 6

    # if ciCompOpt=0, only ciCompParam for all PRBs
    if ciCompOpt == 0:
        if ciCompMeth == NO_COMPRESSION:
            pass
        elif ciCompMeth == BLOCK_FLOATING_POINT:
            logs.add('Exponent', str(int(section[byte_cnt][1], 16)))
            byte_cnt = byte_cnt + 1
        elif ciCompMeth == BLOCK_SCALING:
            logs.add('blockScaler', '0x' + section[byte_cnt])
            byte_cnt = byte_cnt + 1
        elif ciCompMeth == BLOCK_SCALING:
            logs.add('compBitWidth', str(int(section[byte_cnt][0], 16)))
            logs.add('compShift', str(int(section[byte_cnt][1], 16)))
            byte_cnt = byte_cnt + 1

    # 计算每个PRB占用的byte数，位宽*2（I/Q）*天线数，向上取整
    byte_per_prb = (ciIqWidth * 2 * ANT_NUM + 7) / 8
    for prb_idx in range(startPrbc, numPrbc):
        # if ciCompOpt=1, per ciCompParam per PRB
        if ciCompOpt == 1:
            if ciCompMeth == NO_COMPRESSION:
                pass
            elif ciCompMeth == BLOCK_FLOATING_POINT:
                logs.add(('RB %d Exponent' % prb_idx), str(int(section[byte_cnt][1], 16)))
                byte_cnt = byte_cnt + 1
            elif ciCompMeth == BLOCK_SCALING:
                logs.add(('RB %d blockScaler' % prb_idx), '0x' + section[byte_cnt])
                byte_cnt = byte_cnt + 1
            elif ciCompMeth == BLOCK_SCALING:
                logs.add(('RB %d compBitWidth' % prb_idx), str(int(section[byte_cnt][0], 16)))
                logs.add(('RB %d compShift' % prb_idx), str(int(section[byte_cnt][1], 16)))
                byte_cnt = byte_cnt + 1

        bit_sequence = ''
        # 根据每个PRB的行数，生成二进制序列
        for line_idx in range(byte_cnt, byte_cnt + byte_per_prb):
            for char_idx in range(0, len(section[line_idx])):
                bit_sequence = bit_sequence + str(bin(int(section[line_idx][char_idx], 16))[2:].zfill(4))
        # 每个天线获取I/Q值
        for ant_idx in range(0, ANT_NUM):
            value_I = int(bit_sequence[:ciIqWidth])
            value_Q = int(bit_sequence[ciIqWidth:ciIqWidth*2])
            logs.add(('RB %d Antenna %d ciIsample' % (prb_idx, ant_idx)), str(value_I))
            logs.add(('RB %d Antenna %d ciQsample' % (prb_idx, ant_idx)), str(value_Q))
            bit_sequence = bit_sequence[ciIqWidth*2:]

        byte_cnt = byte_cnt + byte_per_prb

    logs.add('', '')

    section = section[byte_cnt:]

    if ef == 1:
        section = ext_parser.parse(section)

    parse(section, section_idx + 1, section_cnt, ciIqWidth, ciCompMeth, ciCompOpt)