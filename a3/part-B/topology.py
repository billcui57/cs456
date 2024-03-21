#!/usr/bin/python

"""Topology with 10 switches and 10 hosts
"""

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

class CSLRTopo( Topo ):

        def __init__( self ):
                "Create Topology"

                # Initialize topology
                Topo.__init__( self )

                # Add hosts
                alice = self.addHost( 'alice' )
                bob = self.addHost( 'bob' )
                carol = self.addHost( 'carol' )

                # Add switches
                r1 = self.addSwitch( 'r1', listenPort=6634 )
                r2 = self.addSwitch( 'r2', listenPort=6635 )
                r3 = self.addSwitch( 'r3', listenPort=6636 )

                # Add links between hosts and switches
                self.addLink( alice, r1)
                self.addLink( bob, r2)
                self.addLink( carol, r3)

                # Add links between switches, with bandwidth 100Mbps
                self.addLink( r1, r2, bw=100 )
                self.addLink( r2, r3, bw=100 )
                self.addLink( r1, r3, bw=100 )

def run():
        "Create and configure network"
        topo = CSLRTopo()
        net = Mininet( topo=topo, link=TCLink, controller=None )

        # Set interface IP and MAC addresses for hosts
        alice = net.get( 'alice' )
        alice.intf( 'alice-eth0' ).setIP( '10.1.1.7', 24)
        alice.intf( 'alice-eth0' ).setMAC( '00:00:00:00:00:01')

        bob = net.get( 'bob' )
        bob.intf( 'bob-eth0' ).setIP( '10.4.4.48', 24)
        bob.intf( 'bob-eth0' ).setMAC( '00:00:00:00:00:02')

        carol = net.get( 'carol' )
        carol.intf( 'carol-eth0' ).setIP( '10.6.6.69', 24)
        carol.intf( 'carol-eth0' ).setMAC( '00:00:00:00:00:03')


        # Set interface MAC address for switches (NOTE: IP
        # addresses are not assigned to switch interfaces)
        r1 = net.get( 'r1' )
        r1.intf( 'r1-eth1' ).setMAC( '0A:00:00:01:00:01' )
        r1.intf( 'r1-eth2' ).setMAC( '0A:00:01:01:00:02' )
        r1.intf( 'r1-eth3' ).setMAC( '0A:00:02:01:00:03' )

        r2 = net.get( 'r2' )
        r2.intf( 'r2-eth1' ).setMAC( '0A:00:03:01:00:01' )
        r2.intf( 'r2-eth2' ).setMAC( '0A:00:04:01:00:02' )
        r2.intf( 'r2-eth3' ).setMAC( '0A:00:05:01:00:03' )

        r3 = net.get( 'r3' )
        r3.intf( 'r3-eth1' ).setMAC( '0A:00:06:01:00:01' )
        r3.intf( 'r3-eth2' ).setMAC( '0A:00:07:01:00:02' )
        r3.intf( 'r3-eth3' ).setMAC( '0A:00:08:01:00:03' )

        net.start()

        # Add routing table entries for hosts (NOTE: The gateway
		# IPs 10.0.X.1 are not assigned to switch interfaces)
        alice.cmd( 'route add default gw 10.1.1.14 dev alice-eth0' )
        bob.cmd( 'route add default gw 10.4.4.14 dev bob-eth0' )
        carol.cmd( 'route add default gw 10.6.6.46 dev carol-eth0' )

        # Add arp cache entries for hosts
        alice.cmd( 'arp -s 10.1.1.14 0A:00:00:01:00:01 -i alice-eth0' )
        bob.cmd( 'arp -s 10.4.4.14 0A:00:03:01:00:01 -i bob-eth0' )
        carol.cmd( 'arp -s 10.6.6.46 0A:00:06:01:00:01 -i carol-eth0' )


        # Open Mininet Command Line Interface
        CLI(net)

        # Teardown and cleanup
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
