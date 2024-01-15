#run script: collector.sh <filename.pcapng>
filename = $1

rwp2yaf2silk --in=$filename --out=temp_file_1.rw
rwcut --fields=1,2,3,4,5,6,7,8,10 --ip-format=decimal --integer-tcp-flags --no-titles --delimited=',' --epoch-time temp_file_1.rw >> file_1.csv

#Add header on file_1.csv:
#   sIP, dIP, sPort, dPort, Proto, Packets, Bytes, Flags, Duration