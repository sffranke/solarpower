#!/usr/bin/env python3
# siehe https://github.com/svalouch/python-rctclient
import socket, select, sys
from rctclient.frame import ReceiveFrame, make_frame
from rctclient.registry import REGISTRY as R
from rctclient.types import Command
from rctclient.utils import decode_value

import paho.mqtt.client as mqtt

# open the socket and connect to the remote device:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.6', 8899))

# query information about an object ID:
#object_info = R.get_by_name('battery.soc')
#object_info = R.get_by_name('g_sync.p_ac_grid_sum_lp')
#object_infoB = R.get_by_name('dc_conv.dc_conv_struct[1].p_dc_lp')
def getval(val):
    object_info = R.get_by_name(val)
    # construct a byte stream that will send a read command for the object ID we want, and send it
    send_frame = make_frame(command=Command.READ, id=object_info.object_id)
    sock.send(send_frame)

    #send_frameB = make_frame(command=Command.READ, id=object_infoA.object_id)
    #sock.send(send_frameB)

    # loop until we got the entire response frame
    frame = ReceiveFrame()
    while True:
        ready_read, _, _ = select.select([sock], [], [], 2.0)
        if sock in ready_read:
            # receive content of the input buffer
            buf = sock.recv(256)
            # if there is content, let the frame consume it
            if len(buf) > 0:
                frame.consume(buf)
                # if the frame is complete, we're done
                if frame.complete():
                    break
            else:
                # the socket was closed by the device, exit
                #sys.exit(1)
                return (0)

    # decode the frames payload
    return decode_value(object_info.response_data_type, frame.data)

valA = getval('dc_conv.dc_conv_struct[0].p_dc_lp')
valB = getval('dc_conv.dc_conv_struct[1].p_dc_lp')
sumval = valA+valB

print(f'Response value: {sumval}')
client = mqtt.Client()
client.connect("localhost", 1893, 60)

client.publish("pythonrct/power_ges",int(sumval))
client.disconnect()
