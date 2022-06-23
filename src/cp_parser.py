import src.st0_parser as st0
import src.st1_parser as st1
import src.st3_parser as st3
import src.st5_parser as st5
import src.st6_parser as st6

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
    print('Ecpri Header:')
    print('    ecpriConcatenation    :    %d' % (int(ecpri_hdr[0], 16) & 0x1))
    print('          ecpriVersion    :    %d' % (int(ecpri_hdr[0][-2], 16)))
    print('          ecpriMessage    :    %d' % (int(ecpri_hdr[1], 16)))
    print('          ecpriPayload    :    %d' % (int(ecpri_hdr[2] + ecpri_hdr[3], 16)))
    print('ecpriRtcid / ecpriPcid    :    0x' + ecpri_hdr[4] + ecpri_hdr[5])
    print('            ecpriSeqid    :    0x' + ecpri_hdr[6] + ecpri_hdr[7])

    # the bits of DU_Port_ID, BandSector_ID, CC_ID, RU_Port_ID in ecpriRtcid based on design
    # for example, DU_Port_ID 4 bits, BandSector_ID 4 bits, CC_ID 4 bits, RU_Port_ID 4 bits
    print('            DU_Port_ID    :    %d' % (int(ecpri_hdr[4][0], 16)))
    print('         BandSector_ID    :    %d' % (int(ecpri_hdr[4][1], 16)))
    print('                 CC_ID    :    %d' % (int(ecpri_hdr[5][0], 16)))
    print('            RU_Port_ID    :    %d' % (int(ecpri_hdr[5][1], 16)))
    print('')

# |    0 (MSB)   |      1       |      2       |      3       |      4       |      5       |      6       |        7 (LSB)   |
# | dataDirection|              payloadVersion                |                        filterIndex                            |
# |                                                        frameId                                                            |
# |                         subframeId                        |                     slotId[5:2]                               |
# |          slotId             |                                     startSymbolid                                           |
# |                                                    numberOfsections                                                       |
# |                                                       sectionType                                                         |
def parse_application_hdr(application_hdr):
    print('Application Header:')
    dataDirection = ((int(application_hdr[0], 16) >> 7) & 0x1)
    if dataDirection == 1:
        print('         dataDirection    :    1 (DL)')
    else:
        print('         dataDirection    :    0 (UL)')
    print('        payloadVersion    :    %d' % ((int(application_hdr[0], 16) >> 4) & 0x7))
    print('           filterIndex    :    %d' % (int(application_hdr[0], 16) & 0xF))
    print('               frameId    :    %d' % (int(application_hdr[1], 16)))
    print('            subframeId    :    %d' % ((int(application_hdr[2], 16) >> 4) & 0xF))
    print('                slotId    :    %d' % ((int(application_hdr[2] + application_hdr[3], 16) >> 6) & 0x3F))
    print('         startSymbolid    :    %d' % ((int(application_hdr[3], 16) & 0x3F)))

    numberOfsections = int(application_hdr[4], 16)
    print('      numberOfsections    :    %d' % numberOfsections)
    sectionType = int(application_hdr[5], 16)
    print('           sectionType    :    %d' % sectionType)

    if sectionType == 0:
# |                                                   timeOffset[15:8]                                                        |
# |                                                   timeOffset[7:0]                                                         |
# |                                                    frameStructure                                                         |
# |                                                    cpLength[15:8]                                                         |
# |                                                    cpLength[7:0]                                                          |
# |                                                       Reserved                                                            |
        print('            timeOffset    :    %d' % (int(application_hdr[6] + application_hdr[7], 16)))
        print('        frameStructure    :    %d' % (int(application_hdr[8], 16)))
        print('              cpLength    :    %d' % (int(application_hdr[9] + application_hdr[10], 16)))
        print('')
        st0.parse(application_hdr[12:])
    elif sectionType == 1:
# |                                                      udCompHdr                                                            |
# |                                                       Reserved                                                            |
        print('             udCompHdr    :    %d' % (int(application_hdr[6], 16)))
        print('')
        st1.parse(application_hdr[8:])
    elif sectionType == 3:
# |                                                   timeOffset[15:8]                                                        |
# |                                                   timeOffset[7:0]                                                         |
# |                                                    frameStructure                                                         |
# |                                                    cpLength[15:8]                                                         |
# |                                                    cpLength[7:0]                                                          |
# |                                                       udCompHdr                                                            |
        print('            timeOffset    :    %d' % (int(application_hdr[6] + application_hdr[7], 16)))
        print('        frameStructure    :    %d' % (int(application_hdr[8], 16)))
        print('              cpLength    :    %d' % (int(application_hdr[9] + application_hdr[10], 16)))
        print('             udCompHdr    :    %d' % (int(application_hdr[11], 16)))
        print('')
        st3.parse(application_hdr[12:])
    elif sectionType == 5:
# |                                                      udCompHdr                                                            |
# |                                                       Reserved                                                            |
        print('             udCompHdr    :    %d' % (int(application_hdr[6], 16)))
        print('')
        st5.parse(application_hdr[8:])
    elif sectionType == 6:
# |                                                     numberOfUEs                                                           |
# |                                                      ciCompHdr                                                            |
        print('           numberOfUEs    :    %d' % (int(application_hdr[6], 16)))
        print('             ciCompHdr    :    %d' % (int(application_hdr[7], 16)))
        print('')
        st6.parse(application_hdr[8:])


def parse_packet(packet):
    parse_ecpri_hdr(packet[:8])
    parse_application_hdr(packet[8:])


# input data is the array of C-Plane packets
def parse(packets):
    for packet in packets:
        # parse C-Plane information for each packet
        parse_packet(packet)