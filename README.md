# COMPX234-A4
20233006400 MiaoKeyan‘s Assignment4

How to test my networked system? ^_^
// Start the server
cd Server
python UDPserver.py 51234

// Start the client
cd Client
python UDPclient.py localhost 51234 files.txt

// MD5
Run "md5sum -b *" over the set of files and compare the hash with the files in the server.

// Start multiple clients
Open multiple terminal windows and run the client in each terminal at the same time.
cd Client
python UDPclient.py localhost 51234 files.txt
cd Client2
python UDPclient.py localhost 51234 files.txt