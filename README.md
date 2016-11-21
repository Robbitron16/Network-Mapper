# Network-Mapper
Finds and maps the topology of a network.


TODO:
  Step 1: Write a python application that uses ping and traceroute to maps the 
    network of the CSE departmnet using the cornell provided algorithim. (Check
    with Shaym to make sure we're on the correct path)

  Step 2: Optimize application with DNS and SNSP!

  Step 3: More optimization (in-memory database, play with timeouts, custom
    traceroute implementation if time)

  Step 4: Create a visual display after execution of the program.
  
  LINKS:
  1. The Algorithm: https://www.cs.cornell.edu/boom/1999sp/projects/network%20topology/topology.html#Basic-algo
  2. The SCAPY library (Custom ICMP packets, custom ping, etc): http://www.secdev.org/projects/scapy/doc/usage.html
  3. The SNMP library (Only for optimizations, do after DNS): http://pysnmp.sourceforge.net/
