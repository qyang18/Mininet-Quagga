#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
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

    	defaultIP1 = '10.0.5.1/24'  # IP address for r0-eth1
    	defaultIP2 = '10.0.5.2/24'
    	defaultIP3 = '10.0.6.2/24'
    	defaultIP4 = '10.0.7.2/24'
    	router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )
    	router2 = self.addNode( 'r2', cls=LinuxRouter, ip=defaultIP2 )
    	router3 = self.addNode( 'r3', cls=LinuxRouter, ip=defaultIP3 )
    	router4 = self.addNode( 'r4', cls=LinuxRouter, ip=defaultIP4 )


    	h1 = self.addHost( 'h1', ip='10.0.1.100/24', defaultRoute='via 10.0.1.10',dpid='0000000000000001') #define gateway
    	h2 = self.addHost( 'h2', ip='10.0.2.100/24', defaultRoute='via 10.0.2.10',dpid='0000000000000002')
    	h3 = self.addHost( 'h3', ip='10.0.3.100/24', defaultRoute='via 10.0.3.10',dpid='0000000000000003')
    	h4 = self.addHost( 'h4', ip='10.0.4.100/24', defaultRoute='via 10.0.4.10',dpid='0000000000000004')

        self.addLink(router1,router2,intfName1='r1-eth1',intfName2='r2-eth1',params1={'ip':'10.0.5.1/24'},bw=100)
    	self.addLink(router1,router3,intfName1='r1-eth2',intfName2='r3-eth1',params1={'ip':'10.0.6.1/24'},bw=100)
    	self.addLink(router1,router4,intfName1='r1-eth3',intfName2='r4-eth1',params1={'ip':'10.0.7.1/24'},bw=100)
        
        self.addLink(h1,router1,intfName2='r1-eth0',params2={ 'ip' : '10.0.1.10/24' },bw=100)#params2 define the eth2 ip address
        self.addLink(h2,router2,intfName2='r2-eth0',params2={ 'ip' : '10.0.2.10/24' },bw=100)
    	self.addLink(h3,router3,intfName2='r3-eth0',params2={ 'ip' : '10.0.3.10/24' },bw=100)
    	self.addLink(h4,router4,intfName2='r4-eth0',params2={ 'ip' : '10.0.4.10/24' },bw=100)

def run():
    "Test linux router"
    topo = NetworkTopo()
#    net = Mininet(controller = None, topo=topo )
    net = Mininet(controller=RemoteController,topo=topo,link=TCLink)
    c1 = net.addController('c1', ip='192.168.33.101', port=6833)

    r1=net.getNodeByName('r1')
    r2=net.getNodeByName('r2')
    r3=net.getNodeByName('r3')
    r4=net.getNodeByName('r4')
    
    net.start()
    
    r1.cmd('ifconfig r1-eth0 10.0.1.10/24')
    r2.cmd('ifconfig r2-eth0 10.0.2.10/24')
    r3.cmd('ifconfig r3-eth0 10.0.3.10/24')
    r4.cmd('ifconfig r4-eth0 10.0.4.10/24')
    r1.cmd('ifconfig r1-eth2 10.0.6.1/24')
    r1.cmd('ifconfig r1-eth3 10.0.7.1/24')
    
    
    info('starting zebra and ospfd service:\n')
    r1.cmd('zebra -f /usr/local/etc/r1zebra.conf -d -z ~/Desktop/r1zebra.api -i ~/Desktop/r1zebra.pid')
    r2.cmd('zebra -f /usr/local/etc/r2zebra.conf -d -z ~/Desktop/r2zebra.api -i ~/Desktop/r2zebra.pid')
    r3.cmd('zebra -f /usr/local/etc/r3zebra.conf -d -z ~/Desktop/r3zebra.api -i ~/Desktop/r3zebra.pid')
    r4.cmd('zebra -f /usr/local/etc/r4zebra.conf -d -z ~/Desktop/r4zebra.api -i ~/Desktop/r4zebra.pid')
    
    time.sleep(1)#time for zebra to create api socket
    
    r1.cmd('ospfd -f /usr/local/etc/r1ospfd.conf -d -z ~/Desktop/r1zebra.api -i ~/Desktop/r1ospfd.pid')
    r2.cmd('ospfd -f /usr/local/etc/r2ospfd.conf -d -z ~/Desktop/r2zebra.api -i ~/Desktop/r2ospfd.pid')
    r3.cmd('ospfd -f /usr/local/etc/r3ospfd.conf -d -z ~/Desktop/r3zebra.api -i ~/Desktop/r3ospfd.pid')
    r4.cmd('ospfd -f /usr/local/etc/r4ospfd.conf -d -z ~/Desktop/r4zebra.api -i ~/Desktop/r4ospfd.pid')
    
    CLI( net )
    net.stop()
    os.system("killall -9 ospfd zebra")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

