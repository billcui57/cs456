#!/usr/bin/env bash

# Sets bridges to use OpenFlow 1.3
ovs-vsctl set bridge r1 protocols=OpenFlow13
ovs-vsctl set bridge r2 protocols=OpenFlow13
ovs-vsctl set bridge r3 protocols=OpenFlow13

# Print the protocols that each switch supports
for switch in r1 r2 r3;
do
    protos=$(ovs-vsctl get bridge $switch protocols)
    echo "Switch $switch supports $protos"
done

# Avoid having to write "-O OpenFlow13" before all of your ovs-ofctl commands.
ofctl='ovs-ofctl -O OpenFlow13'

#alice <-> bob
echo "Setting up alice <-> bob"

# OVS rules for switch alice->bob
$ofctl add-flow r1 \
    ip,nw_src=10.1.1.7nw_dst=10.4.4.48,actions=output=2

$ofctl add-flow r2 \
    ip,nw_src=10.1.1.7nw_dst=10.4.4.48,actions=,output=1

# OVS rules for switch bob->alice
$ofctl add-flow r2 \
    ip,nw_src=10.4.4.48,nw_dst=10.1.1.7,actions=,output=2

$ofctl add-flow r1 \
    ip,nw_src=10.4.4.48,nw_dst=10.1.1.7,actions=,output=1


# Print the flows installed in each switch
for switch in r1 r2;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
