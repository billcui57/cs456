# OVS rules for switch 0

1. $ofctl add-flow s0 \
in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0A:FE:00:02,output=2

Add a new flow entry to the flow table of switch 0. The flow entry matches IP datagrams with the following fields:
- The input port is 1
- The source IP address is 10.0.0.2
- The destination IP address is 10.0.1.2

The actions to be performed on the matched packets are:
- Modify the source MAC address to 0A:00:0A:01:00:02
- Modify the destination MAC address to 0A:00:0A:FE:00:02
- Forward the datagram to port 2


2. $ofctl add-flow s0 \
in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1

Add a new flow entry to the flow table of switch 0. The flow entry matches IP datagrams with the following fields:
- The input port is 2
- The source IP address is 10.0.1.2
- The destination IP address is 10.0.0.2 

The actions to be performed on the matched packets are:
- Modify the source MAC address to 0A:00:00:01:00:01
- Modify the destination MAC address to 0A:00:00:02:00:00
- Forward the datagram to port 1

# OVS rules for switch 1
1. $ofctl add-flow s1 \
in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1

Add a new flow entry to the flow table of switch 1. The flow entry matches IP datagrams with the following fields:
- The input port is 2
- The source IP address is 10.0.0.2
- The destination IP address is 10.0.1.2

The actions to be performed on the matched packets are:
- Modify the source MAC address to 0A:00:01:01:00:01
- Modify the destination MAC address to 0A:00:01:02:00:00
- Forward the datagram to port 1

2. $ofctl add-flow s1 \
in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0A:FE:00:02,mod_dl_dst:0A:00:0A:01:00:02,output=2

Add a new flow entry to the flow table of switch 1. The flow entry matches IP datagrams with the following fields:
- The input port is 1
- The source IP address is 10.0.1.2
- The destination IP address is 10.0.0.2

The actions to be performed on the matched packets are:
- Modify the source MAC address to 0A:00:0A:FE:00:02
- Modify the destination MAC address to 0A:00:0A:01:00:02
- Forward the datagram to port 2
