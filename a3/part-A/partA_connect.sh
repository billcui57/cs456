#!/usr/bin/env bash

#h1 <-> h4

# Sets bridge s1 to use OpenFlow 1.3
ovs-vsctl set bridge s1 protocols=OpenFlow13
ovs-vsctl set bridge s2 protocols=OpenFlow13
ovs-vsctl set bridge s3 protocols=OpenFlow13
ovs-vsctl set bridge s4 protocols=OpenFlow13

# Print the protocols that each switch supports
for switch in s1 s2 s3 s4;
do
    protos=$(ovs-vsctl get bridge $switch protocols)
    echo "Switch $switch supports $protos"
done

# Avoid having to write "-O OpenFlow13" before all of your ovs-ofctl commands.
ofctl='ovs-ofctl -O OpenFlow13'

# OVS rules for switch 1
$ofctl add-flow s1 \
    in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0C:01:00:03,mod_dl_dst:0A:00:0D:01:00:03,output=3

$ofctl add-flow s2 \
    in_port=3,ip,nw_src=10.0.1.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

$ofctl add-flow s3 \
    in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:0E:FE:00:02,output=3

$ofctl add-flow s4 \
    in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:04:01:00:01,mod_dl_dst:0A:00:04:02:00:00,output=1


# Print the flows installed in each switch
for switch in s1 s2 s3 s4;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
