#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf
from mininet.link import TCLink
import time
import os

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()
	
class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        defaultIP1 = '10.0.1.10/24'  # IP address for r0-eth1
        
        router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )
        
        h1 = self.addHost( 'h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.10') #define gateway

#	self.addLink(router1,router2,intfName1='r1-eth1',intfName2='r2-eth1')
	self.addLink(h1,router1,intfName2='r1-eth1',params2={ 'ip' : '10.0.1.10/24' },bw=100)#params2 define the address eth2 ip


def run():
	topo = NetworkTopo()
	net = Mininet(controller = None, topo=topo, link=TCLink)	
	r1=net.getNodeByName('r1')
	Intf('eth0', node=r1)

	net.start()

	info('starting zebra and ospfd service:\n')
	r1.cmd('ifconfig eth0 10.0.3.10/24')
	r1.cmd('zebra -f /usr/local/etc/zebra.conf -d -z ~/Desktop/zebra.api -i ~/Desktop/r1zebra.interface')
	time.sleep(1)#time for zebra to create api socket
	r1.cmd('ospfd -f /usr/local/etc/r1ospfd.conf -d -z ~/Desktop/zebra.api -i ~/Desktop/r1ospfd.interface')


    
    
	CLI( net )
	net.stop()
	os.system("killall -9 ospfd zebra")
	os.system("rm -f *api*")
	os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

