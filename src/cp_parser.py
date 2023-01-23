import src.st0_parser as st0
import src.st1_parser as st1
import src.st3_parser as st3
import src.st5_parser as st5
import src.st6_parser as st6
import src.logs as logs

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# |                      ecpriVersion                         |              ecpriReserved                 |ecpriConcatenation|
# |                                                     ecpriMessage                                                          |
# |                                                  ecpriPayload[15:8]                                                       |
# |                                                  ecpriPayload[7:0]                                                        |
# |                                               ecpriRtcid / ecpriPcid[15:8]                                                |
# |                                               ecpriRtcid / ecpriPcid[7:0]                                                 |
# |                                                   ecpriSeqid[15:8]                                                        |
# |                                                   ecpriSeqid[7:0]                                                         |
def parse_ecpri_hdr(ecpri_hdr):
    logs.add('Ecpri Header:', '')
    logs.add('ecpriConcatenation', str(int(ecpri_hdr[0], 16) & 0x1))
    logs.add('ecpriVersion', str(int(ecpri_hdr[0][-2], 16)))
    logs.add('ecpriMessage', str(int(ecpri_hdr[1], 16)))
    logs.add('ecpriPayload', str(int(ecpri_hdr[2] + ecpri_hdr[3], 16)))
    logs.add('ecpriRtcid / ecpriPcid', '0x' + ecpri_hdr[4] + ecpri_hdr[5])
    logs.add('ecpriSeqid', '0x' + ecpri_hdr[6] + ecpri_hdr[7])

    # the bits of DU_Port_ID, BandSector_ID, CC_ID, RU_Port_ID in ecpriRtcid based on design
    # for example, DU_Port_ID 4 bits, BandSector_ID 4 bits, CC_ID 4 bits, RU_Port_ID 4 bits
    logs.add('DU_Port_ID', str(int(ecpri_hdr[4][0], 16)))
    logs.add('BandSector_ID', str(int(ecpri_hdr[4][1], 16)))
    logs.add('CC_ID', str(int(ecpri_hdr[5][0], 16)))
    logs.add('RU_Port_ID', str(int(ecpri_hdr[5][1], 16)))
    logs.add('', '')

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# | dataDirection|              payloadVersion                |                        filterIndex                            |
# |                                                        frameId                                                            |
# |                         subframeId                        |                     slotId[5:2]                               |
# |          slotId             |                                     startSymbolid                                           |
# |                                                    numberOfsections                                                       |
# |                                                       sectionType                                                         |
def parse_application_hdr(application_hdr):
    logs.add('Application Header:', '')
    dataDirection = ((int(application_hdr[0], 16) >> 7) & 0x1)
    if dataDirection == 1:
        logs.add('dataDirection', '1 (DL)')
    else:
        logs.add('dataDirection', '0 (UL)')
    logs.add('payloadVersion', str((int(application_hdr[0], 16) >> 4) & 0x7))
    logs.add('filterIndex', str(int(application_hdr[0], 16) & 0xF))
    logs.add('frameId', str(int(application_hdr[1], 16)))
    logs.add('subframeId', str((int(application_hdr[2], 16) >> 4) & 0xF))
    logs.add('slotId', str((int(application_hdr[2] + application_hdr[3], 16) >> 6) & 0x3F))
    logs.add('startSymbolid', str((int(application_hdr[3], 16) & 0x3F)))

    numberOfsections = int(application_hdr[4], 16)
    logs.add('numberOfsections', str(numberOfsections))
    sectionType = int(application_hdr[5], 16)
    logs.add('sectionType', str(sectionType))

    if sectionType == 0:
# |                                                   timeOffset[15:8]                                                        |
# |                                                   timeOffset[7:0]                                                         |
# |                                                    frameStructure                                                         |
# |                                                    cpLength[15:8]                                                         |
# |                                                    cpLength[7:0]                                                          |
# |                                                       Reserved                                                            |
        logs.add('timeOffset', str(int(application_hdr[6] + application_hdr[7], 16)))
        logs.add('frameStructure', str(int(application_hdr[8], 16)))
        logs.add('cpLength', str(int(application_hdr[9] + application_hdr[10], 16)))
        logs.add('', '')
        st0.parse(application_hdr[12:], 0, numberOfsections)
    elif sectionType == 1:
# |                                                      udCompHdr                                                            |
# |                                                       Reserved                                                            |
        logs.add('udCompHdr', str(int(application_hdr[6], 16)))
        logs.add('', '')
        st1.parse(application_hdr[8:], 0, numberOfsections)
    elif sectionType == 3:
# |                                                   timeOffset[15:8]                                                        |
# |                                                   timeOffset[7:0]                                                         |
# |                                                    frameStructure                                                         |
# |                                                    cpLength[15:8]                                                         |
# |                                                    cpLength[7:0]                                                          |
# |                                                       udCompHdr                                                           |
        logs.add('timeOffset', str(int(application_hdr[6] + application_hdr[7], 16)))
        logs.add('frameStructure', str(int(application_hdr[8], 16)))
        logs.add('cpLength', str(int(application_hdr[9] + application_hdr[10], 16)))
        logs.add('udCompHdr', str(int(application_hdr[11], 16)))
        logs.add('', '')
        st3.parse(application_hdr[12:], 0, numberOfsections)
    elif sectionType == 5:
# |                                                      udCompHdr                                                            |
# |                                                       Reserved                                                            |
        logs.add('udCompHdr', str(int(application_hdr[6], 16)))
        logs.add('', '')
        st5.parse(application_hdr[8:], 0, numberOfsections)
    elif sectionType == 6:
# |                                                     numberOfUEs                                                           |
# |                                                      ciCompHdr                                                            |
        logs.add('numberOfUEs', str(int(application_hdr[6], 16)))

        ciCompHdr = int(application_hdr[7], 16)
        logs.add('ciCompHdr', str(ciCompHdr))

        ciIqWidth = ciCompHdr >> 4
        logs.add('ciIqWidth', str(ciIqWidth))
        ciCompMeth = (ciCompHdr >> 1) & 0x7
        logs.add('ciCompMeth', str(ciCompMeth))
        ciCompOpt = ciCompHdr & 0x1
        logs.add('ciCompOpt', str(ciCompOpt))
        logs.add('', '')
        st6.parse(application_hdr[8:], 0, numberOfsections, ciIqWidth, ciCompMeth, ciCompOpt)


def parse_packet(packet):
    parse_ecpri_hdr(packet[:8])
    parse_application_hdr(packet[8:])


# input data is the array of C-Plane packets
def parse(packets):
    for packet in packets:
        # parse C-Plane information for each packet
        parse_packet(packet)