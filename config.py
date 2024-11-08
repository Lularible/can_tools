from PCANBasic import *

# if canfd, it's True.
# if can, it's False
is_can_fd = True

# if need keep_alive, it's True
# if no need keep alive, it's False
need_keep_alive = False

# uds resp msg can id
rx_uds_msg_id = [
    0x6B0,
    0x78B,
]


# timeout for recv the expect msg(milisecond)
rx_timeout = 500

# increase addition time for nrc pending(milisecond)
addition_time_for_pending = 3000

# can msg define
# [tx_canid, rx_canid, can or canfd, content, delay for send next msg(second), description]
# for example
# [0x783, 0x78B, [0x02, 0x10, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], 1, "default_session"]
# from content to get the length
# if expect no resp, then the rx_canid is 0x0
tx_canid_index = 0
rx_canid_index = 1
msg_contend_index = 2
delay_for_send_next_msg_index = 3
description_index = 4

# session_control
switch_to_default_session = [0x783, 0x78B, [0x02, 0x10, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], 0, "default_session"]
switch_to_program_session = [0x783, 0x78B, [0x02, 0x10, 0x02, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], 0, "program_session"]
switch_to_extention_session = [0x783, 0x78B, [0x02, 0x10, 0x03, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], 0, "extention_session"]


# read_did_external
read_did_0104_external = [0x783, 0x78B, [0x03, 0x22, 0x01, 0x04, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0104"]
read_did_0105_external = [0x783, 0x78B, [0x03, 0x22, 0x01, 0x05, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0105"]
read_did_0108_external = [0x783, 0x78B, [0x03, 0x22, 0x01, 0x08, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0108"]
read_did_0109_external = [0x783, 0x78B, [0x03, 0x22, 0x01, 0x09, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0109"]
read_did_010B_external = [0x783, 0x78B, [0x03, 0x22, 0x01, 0x0B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "010B"]
read_did_F187_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x87, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F187"]
read_did_F189_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x89, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F189"]
read_did_F18B_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x8B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18B"]
read_did_F18C_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x8C, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18C"]
read_did_F191_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x91, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F191"]
read_did_F193_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x93, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F193"]
read_did_F195_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x95, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F195"]
read_did_F197_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0x97, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F197"]
read_did_F1A0_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xA0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A0"]
read_did_F1A1_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xA1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A1"]
read_did_F1B0_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xB0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B0"]
read_did_F1B1_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xB1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B1"]
read_did_F1B2_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xB2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B2"]
read_did_F1B3_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xB3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B3"]
read_did_F1C1_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xC1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C1"]
read_did_F1C2_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xC2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C2"]
read_did_F1C3_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xC3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C3"]
read_did_F1EF_external = [0x783, 0x78B, [0x03, 0x22, 0xF1, 0xEF, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1EF"]


# read_did_internal
read_did_0104_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0x01, 0x04, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0104"]
read_did_0105_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0x01, 0x05, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0105"]
read_did_0108_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0x01, 0x08, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0108"]
read_did_0109_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0x01, 0x09, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0109"]
read_did_010B_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0x01, 0x0B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "010B"]
read_did_F187_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x87, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F187"]
read_did_F189_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x89, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F189"]
read_did_F18B_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x8B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18B"]
read_did_F18C_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x8C, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18C"]
read_did_F191_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x91, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F191"]
read_did_F193_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x93, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F193"]
read_did_F195_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x95, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F195"]
read_did_F197_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0x97, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F197"]
read_did_F1A0_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xA0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A0"]
read_did_F1A1_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xA1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A1"]
read_did_F1B0_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xB0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B0"]
read_did_F1B1_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xB1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B1"]
read_did_F1B2_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xB2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B2"]
read_did_F1B3_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xB3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B3"]
read_did_F1C1_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xC1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C1"]
read_did_F1C2_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xC2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C2"]
read_did_F1C3_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xC3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C3"]
read_did_F1EF_internal = [0x6D1, 0x6B0, [0x03, 0x22, 0xF1, 0xEF, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1EF"]


# read_did_function_address
read_did_0104_function = [0x7DF, 0x78B, [0x03, 0x22, 0x01, 0x04, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0104"]
read_did_0105_function = [0x7DF, 0x78B, [0x03, 0x22, 0x01, 0x05, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0105"]
read_did_0108_function = [0x7DF, 0x78B, [0x03, 0x22, 0x01, 0x08, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0108"]
read_did_0109_function = [0x7DF, 0x78B, [0x03, 0x22, 0x01, 0x09, 0xAA, 0xAA, 0xAA, 0xAA], 0, "0109"]
read_did_010B_function = [0x7DF, 0x78B, [0x03, 0x22, 0x01, 0x0B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "010B"]
read_did_F187_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x87, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F187"]
read_did_F189_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x89, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F189"]
read_did_F18B_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x8B, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18B"]
read_did_F18C_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x8C, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F18C"]
read_did_F191_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x91, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F191"]
read_did_F193_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x93, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F193"]
read_did_F195_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x95, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F195"]
read_did_F197_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0x97, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F197"]
read_did_F1A0_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xA0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A0"]
read_did_F1A1_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xA1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1A1"]
read_did_F1B0_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xB0, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B0"]
read_did_F1B1_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xB1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B1"]
read_did_F1B2_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xB2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B2"]
read_did_F1B3_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xB3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1B3"]
read_did_F1C1_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xC1, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C1"]
read_did_F1C2_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xC2, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C2"]
read_did_F1C3_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xC3, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1C3"]
read_did_F1EF_function = [0x7DF, 0x78B, [0x03, 0x22, 0xF1, 0xEF, 0xAA, 0xAA, 0xAA, 0xAA], 0, "F1EF"]


msg_keep_alive = [0x783, 0x0, [0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], 0, "keep_alive"]


msg_flow_control = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF4, 0x9C]

key_27_12_first_frame = [0x10, 0x0A, 0x27, 0x12, 0xAA, 0xAA, 0xAA, 0xAA]
key_27_12_second_frame = [0x21, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA] 

channel_open = [
    [0x72, 0x0, [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xDF, 0xC0, 0xE7, 0x06, 0xFF, 0xFC, 0xFF, 0xFF, 0xFF, 0xFF, 0xEF, 0xFF, 0xEF, 0xFF, 0xFF, 0xFF], 1, "output channel mask"],
    [0x73, 0x0, [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x17, 0x02, 0xF3, 0xFF, 0x0F, 0xC7, 0xFF, 0x03, 0x0F, 0x00, 0xC0, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], 1, "AMP_unmute-SPDIFunmute-FM"],
    [0x76, 0x0, [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xC0, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 0, "MainVolumeSet byte 8"]
]


switch_session_sequence = [
    switch_to_default_session,
    switch_to_program_session,
    switch_to_extention_session,
]


read_all_external_did_sequence = [
    read_did_0104_external,
    read_did_0105_external,
    read_did_0108_external,
    read_did_0109_external,
    read_did_010B_external,
    read_did_F187_external,
    read_did_F189_external,
    read_did_F18B_external,
    read_did_F18C_external,
    read_did_F191_external,
    read_did_F193_external,
    read_did_F195_external,
    read_did_F197_external,
    read_did_F1A0_external,
    read_did_F1A1_external,
    read_did_F1B0_external,
    read_did_F1B1_external,
    read_did_F1B2_external,
    read_did_F1B3_external,
    read_did_F1C1_external,
    read_did_F1C2_external,
    read_did_F1C3_external,
    read_did_F1EF_external,
]

read_all_internal_did_sequence = [
    read_did_0104_internal,
    read_did_0105_internal,
    read_did_0108_internal,
    read_did_0109_internal,
    read_did_010B_internal,
    read_did_F187_internal,
    read_did_F189_internal,
    read_did_F18B_internal,
    read_did_F18C_internal,
    read_did_F191_internal,
    read_did_F193_internal,
    read_did_F195_internal,
    read_did_F197_internal,
    read_did_F1A0_internal,
    read_did_F1A1_internal,
    read_did_F1B0_internal,
    read_did_F1B1_internal,
    read_did_F1B2_internal,
    read_did_F1B3_internal,
    read_did_F1C1_internal,
    read_did_F1C2_internal,
    read_did_F1C3_internal,
    read_did_F1EF_internal,
]

read_all_function_did_sequence = [
    read_did_0104_function,
    read_did_0105_function,
    read_did_0108_function,
    read_did_0109_function,
    read_did_010B_function,
    read_did_F187_function,
    read_did_F189_function,
    read_did_F18B_function,
    read_did_F18C_function,
    read_did_F191_function,
    read_did_F193_function,
    read_did_F195_function,
    read_did_F197_function,
    read_did_F1A0_function,
    read_did_F1A1_function,
    read_did_F1B0_function,
    read_did_F1B1_function,
    read_did_F1B2_function,
    read_did_F1B3_function,
    read_did_F1C1_function,
    read_did_F1C2_function,
    read_did_F1C3_function,
    read_did_F1EF_function,
]


##################################################################################
#### the following is discarded!!! ####
##################################################################################

beep_1 = ["beep", [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00]]
beep_2 = ["beep", [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00]]

# security control
security_11 = ["security", [0x02, 0x27, 0x11, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]
security_12_1 = ["security", [0x10, 0x0A, 0x27, 0x12, 0xAA, 0xAA, 0xAA, 0xAA]]
security_12_2 = ["security", [0x21, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]
security_13 = ["security", [0x02, 0x27, 0x13, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]
security_14_1 = ["security", [0x11, 0x02, 0x27, 0x14, 0xAA, 0xAA, 0xAA, 0xAA]]
security_14_2 = ["security", [0x21, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]




# session control
default_session = ["session", [0x02, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]]
program_session = ["session", [0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00]]
extended_session = ["session", [0x02, 0x10, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00]]


# read did
read_iDTC = ["did", [0x03, 0x22, 0xf1, 0x21, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_iDTC_USB = ["did", [0x03, 0x22, 0xf1, 0x22, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F120 = ["did", [0x03, 0x22, 0xf1, 0x20, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F1EF = ["did", [0x03, 0x22, 0xf1, 0xef, 0x00, 0x00, 0x00, 0x00], "multi_frame"]

read_0104 = ["did", [0x03, 0x22, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_0105 = ["did", [0x03, 0x22, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_0108 = ["did", [0x03, 0x22, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_0109 = ["did", [0x03, 0x22, 0x01, 0x09, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_010B = ["did", [0x03, 0x22, 0x01, 0x0B, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_010C = ["did", [0x03, 0x22, 0x01, 0x0C, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_010D = ["did", [0x03, 0x22, 0x01, 0x0D, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F187 = ["did", [0x03, 0x22, 0xF1, 0x87, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F189 = ["did", [0x03, 0x22, 0xF1, 0x89, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F18B = ["did", [0x03, 0x22, 0xF1, 0x8B, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F18C = ["did", [0x03, 0x22, 0xF1, 0x8C, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F191 = ["did", [0x03, 0x22, 0xF1, 0x91, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F193 = ["did", [0x03, 0x22, 0xF1, 0x93, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F195 = ["did", [0x03, 0x22, 0xF1, 0x95, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F1A0 = ["did", [0x03, 0x22, 0xF1, 0xA0, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1A1 = ["did", [0x03, 0x22, 0xF1, 0xA1, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1B0 = ["did", [0x03, 0x22, 0xF1, 0xB0, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1B1 = ["did", [0x03, 0x22, 0xF1, 0xB1, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1B2 = ["did", [0x03, 0x22, 0xF1, 0xB2, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1B3 = ["did", [0x03, 0x22, 0xF1, 0xB3, 0x00, 0x00, 0x00, 0x00], "single_frame"]
read_F1C1 = ["did", [0x03, 0x22, 0xF1, 0xC1, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F1C2 = ["did", [0x03, 0x22, 0xF1, 0xC2, 0x00, 0x00, 0x00, 0x00], "multi_frame"]
read_F1C3 = ["did", [0x03, 0x22, 0xF1, 0xC3, 0x00, 0x00, 0x00, 0x00], "multi_frame"]

read_multi_did = ["did", [0x05, 0x22, 0xF1, 0xB1, 0x01, 0x0c, 0x00, 0x00], "multi_frame"]




# dtc
start_booster_diag = ["dtc", [0x05, 0x31, 0x01, 0xA0, 0x00, 0x00, 0xAA, 0xAA]]
read_booster_dtc = ["dtc", [0x03, 0x19, 0x02, 0x08, 0xAA, 0xAA, 0xAA, 0xAA]]
clear_iDTC = ["dtc", [0x04, 0x14, 0xff, 0xff, 0x0ff, 0x00, 0x00, 0x00]]

# signal
ACU_CRSHACTVSTA_VALID_0 = ["signal", [0x10, 0x08, 0xff, 0xff, 0x00, 0x01, 0x00, 0x00]]
ACU_CRSHACTVSTA_VALID_1 = ["signal", [0x21, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]
ACU_CRSHACTVSTA_INVALID_0 = ["signal", [0x10, 0x08, 0xff, 0xff, 0x00, 0x03, 0x00, 0x00]]
ACU_CRSHACTVSTA_INVALID_1 = ["signal", [0x21, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]


# request upload
request_upload_first = ["upload", [0x10, 0x0B, 0x35, 0x00, 0x44, 0x00, 0x00, 0x00]]
request_upload_second = ["upload", [0x21, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00]]


# transfer
# send 01 once
transfer_data_once = ["transfer_data", [0x02, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 1, [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF4, 0x9C]]
# send 96 times, 01 ~ 96
transfer_data_sys_log = ["transfer_data", [0x02, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 96, [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF4, 0x9C]]


# transfer exit
transfer_exit = ["transfer_exit", [0x01, 0x37, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]

# can flow control
can_flow_control = ["can_flow_control", [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF4, 0x9C]]

# keep alive
keep_alive = ["keep_alive", [0x02, 0x3E, 0x80, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]

# reset
reset = ["reset", [0x02, 0x11, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]]


# get temp
get_temp_DSPCORE0_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_DSPCORE0_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x0C, 0x0D, 0x00, 0x00]]

get_temp_DSPCORE1_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_DSPCORE1_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x0D, 0x0D, 0x00, 0x00]]

get_temp_POWERIC0_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_POWERIC0_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x0E, 0x0D, 0x00, 0x00]]

get_temp_POWERIC1_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_POWERIC1_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x0F, 0x0D, 0x00, 0x00]]

get_temp_POWERIC2_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_POWERIC2_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x10, 0x0D, 0x00, 0x00]]

get_temp_POWERIC3_first = ["get_temp", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
get_temp_POWERIC3_second = ["get_temp", [0x21, 0x2A, 0x00, 0x29, 0x11, 0x0D, 0x00, 0x00]]


# ap manufacoty
get_f1_first = ["ap_manufacoty", [0x10, 0x0C, 0x31, 0x01, 0xFE, 0xFE, 0x08, 0xFF]]
get_f1_second = ["ap_manufacoty", [0x21, 0xF1, 0x01, 0x05, 0x06, 0x6D, 0x0D, 0x00]]

get_f2_first = ["ap_manufacoty", [0x10, 0x09, 0x31, 0x01, 0xFE, 0xFE, 0x05, 0xFF]]
get_f2_second = ["ap_manufacoty", [0x21, 0x2F, 0x04, 0x0D, 0xAA, 0xAA, 0xAA, 0xAA]]

mute_ctrl_first = ["ap_manufacoty", [0x10, 0x09, 0x31, 0x01, 0xFE, 0xFE, 0x05, 0xFF]]
mute_ctrl_second = ["ap_manufacoty", [0x21, 0x5D, 0x01, 0x0D, 0xAA, 0xAA, 0xAA, 0xAA]]

volume_ctrl_enable_first = ["ap_manufacoty", [0x10, 0x0D, 0x31, 0x01, 0xFE, 0xFE, 0x09, 0xFF]]
volume_ctrl_enable_second = ["ap_manufacoty", [0x21, 0x5E, 0x01, 0x01, 0x4B, 0x00, 0x64, 0x0D]]

volume_ctrl_get_status_first = ["ap_manufacoty", [0x10, 0x0D, 0x31, 0x01, 0xFE, 0xFE, 0x09, 0xFF]]
volume_ctrl_get_status_second = ["ap_manufacoty", [0x21, 0x5E, 0x00, 0x01, 0x4B, 0x00, 0x64, 0x0D]]


volume_ctrl_set_first = ["ap_manufacoty", [0x10, 0x0D, 0x31, 0x01, 0xFE, 0xFE, 0x09, 0xFF]]
volume_ctrl_set_second = ["ap_manufacoty", [0x21, 0x5E, 0x02, 0x01, 0x4B, 0x00, 0x64, 0x0D]]

cyber_security_handle_first = ["ap_manufacoty", [0x10, 0x0B, 0x31, 0x01, 0xFE, 0xFE, 0x07, 0xFF]]
cyber_security_handle_second = ["ap_manufacoty", [0x21, 0x07, 0x01, 0x02, 0x01, 0x0D, 0xAA, 0xAA]]


serial_number_handle_1 = ["serial_number", [0x10, 0x1B, 0x31, 0x01, 0xFE, 0xFE, 0x17, 0xFF]]
serial_number_handle_2 = ["serial_number", [0x21, 0xF1, 0x01, 0x00, 0x02, 0x48, 0x61, 0x72]]
serial_number_handle_3 = ["serial_number", [0x22, 0x6D, 0x61, 0x6E, 0x5F, 0x4B, 0x6F, 0x72]]
serial_number_handle_4 = ["serial_number", [0x23, 0x65, 0x61, 0x40, 0x32, 0x32, 0x21, 0x0D]]
serial_number_handle_5 = ["serial_number", [0x10, 0x11, 0x31, 0x01, 0xFE, 0xFE, 0x0D, 0xFF]]
serial_number_handle_6 = ["serial_number", [0x21, 0xF1, 0x01, 0x08, 0x02, 0x12, 0x34, 0x56]]
serial_number_handle_7 = ["serial_number", [0x22, 0x78, 0x9A, 0xBC, 0x0D, 0xAA, 0xAA, 0xAA]]

date_number_handle_1 = ["date_number", [0x10, 0x0F, 0x31, 0x01, 0xFE, 0xFE, 0x0D, 0xFF]]
date_number_handle_2 = ["date_number", [0x21, 0xF1, 0x01, 0x08, 0x03, 0x20, 0x24, 0x08]]
date_number_handle_3 = ["date_number", [0x22, 0x12, 0x0D, 0xBC, 0x0D, 0xAA, 0xAA, 0xAA]]


cabin_set_value = ["cabin", [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]
cabin_enable = ["cabin", [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]]

serial_number_sequence = [
    serial_number_handle_1,
    serial_number_handle_2,
    serial_number_handle_3,
    serial_number_handle_4,
    can_flow_control,
    serial_number_handle_5,
    serial_number_handle_6,
    serial_number_handle_7,
    can_flow_control,
    read_F18C,
    can_flow_control,
    date_number_handle_1,
    date_number_handle_2,
    date_number_handle_3,
    can_flow_control,
    read_F18B,
]


manufacoty_f1_sequence = [
    get_f1_first,
    get_f1_second
]

manufacoty_f2_sequence = [
    get_f2_first,
    get_f2_second
]

mute_ctrl_sequence = [
    mute_ctrl_first,
    mute_ctrl_second
]

volume_ctrl_enable_sequence = [
    volume_ctrl_enable_first,
    volume_ctrl_enable_second,
    can_flow_control
]

volume_ctrl_get_status_sequence = [
    volume_ctrl_get_status_first,
    volume_ctrl_get_status_second,
    can_flow_control
]

volume_ctrl_set_sequence = [
    volume_ctrl_set_first,
    volume_ctrl_set_second,
    can_flow_control
]

cyber_security_handle_sequence = [
    cyber_security_handle_first,
    cyber_security_handle_second,
    can_flow_control
]

# iDTC sequence
iDTC_sequence = [
    extended_session,
    read_iDTC,
    request_upload_first,
    request_upload_second,
    transfer_data_once,
    transfer_exit
]

# iDTC USB sequence
iDTC_USB_sequence = [
    extended_session,
    read_iDTC_USB,
    request_upload_first,
    request_upload_second,
    transfer_data_sys_log,
    transfer_exit
]

# syslog sequence
syslog_sequence = [
    extended_session,
    # read_syslog,
    # request_upload_first,
    # request_upload_second,
    # transfer_data_sys_log,
    # transfer_exit
]

read_F1EF_sequence = [
    read_F1EF,
    can_flow_control,
]

read_all_did_sequence = [
    read_0104,
    can_flow_control,
    read_0105,
    can_flow_control,
    read_0108,
    can_flow_control,
    read_010B,
    can_flow_control,
    read_010C,
    can_flow_control,
    read_010D,
    can_flow_control,
    read_F120,
    read_F187,
    can_flow_control,
    read_F189,
    read_F18B,
    read_F18C,
    can_flow_control,
    read_F191,
    read_F193,
    read_F195,
    can_flow_control,
    read_F1A0,
    read_F1A1,
    read_F1B0,
    read_F1B1,
    read_F1B2,
    read_F1B3,
    read_F1C1,
    can_flow_control,
    read_F1C2,
    can_flow_control,
    read_F1C3,
    can_flow_control,
    read_F1EF,
    can_flow_control,
]

read_DSPCORE0_temp = [
    extended_session,
    get_temp_DSPCORE0_first,
    get_temp_DSPCORE0_second,
    can_flow_control
]

read_DSPCORE1_temp = [
    extended_session,
    get_temp_DSPCORE1_first,
    get_temp_DSPCORE1_second,
    can_flow_control
]

read_POWERIC0_temp = [
    extended_session,
    get_temp_POWERIC0_first,
    get_temp_POWERIC0_second,
    can_flow_control
]

read_POWERIC1_temp = [
    extended_session,
    get_temp_POWERIC1_first,
    get_temp_POWERIC1_second,
    can_flow_control
]

read_POWERIC2_temp = [
    extended_session,
    get_temp_POWERIC2_first,
    get_temp_POWERIC2_second,
    can_flow_control
]

read_POWERIC3_temp = [
    extended_session,
    get_temp_POWERIC3_first,
    get_temp_POWERIC3_second,
    can_flow_control
]

read_010B_sequence = [
    read_010B,
    can_flow_control
]

# session_swich_sequence = [
#     default_session,
#     program_session,
#     default_session
# ]

security_sequence = [
    default_session,
    extended_session,
    security_11,
    can_flow_control,
    security_12_1,
    security_12_2,
    security_11,
    can_flow_control,
    security_12_1,
    security_12_2,
    # extended_session,
    security_11,
    can_flow_control,
    security_12_1,
    security_12_2,
    security_11,
]

read_booster_dtc_sequence = [
    start_booster_diag,
    can_flow_control,
    can_flow_control,
    read_booster_dtc,
    can_flow_control,
    clear_iDTC,
    can_flow_control,
    reset
]

read_F187_sequence = [
    read_F187,
    can_flow_control
]

request_upload_sequence = [
    extended_session,
    request_upload_first,
    request_upload_second,
]

fbl_1001_test = [
    program_session,
    can_flow_control,
    default_session
]

read_dsp0_checksum = [
    read_0108,
    can_flow_control,
    can_flow_control,
    read_0109,
    can_flow_control,
    can_flow_control,
]

read_dsp_checksum = [
    read_0108,
    can_flow_control,
    # can_flow_control,
    # read_0109,
    # can_flow_control,
    # can_flow_control,
]

read_F1B1_F183 = [
    read_F1B1,
    can_flow_control,
    read_F1B2,
    can_flow_control,
    read_F1B3,
    can_flow_control,
]

signal_sequence = [
    ACU_CRSHACTVSTA_VALID_0,
    ACU_CRSHACTVSTA_VALID_1,
]

read_0108 = [
    read_0108,
    can_flow_control,
    can_flow_control,
    can_flow_control,
    can_flow_control,
]

read_0109 = [
    read_0109,
    can_flow_control,
    can_flow_control,
    can_flow_control,
    can_flow_control,
]

read_multi_did = [
    read_multi_did,
    can_flow_control,
]

beep_sequence = [
    beep_1,
    beep_2
]