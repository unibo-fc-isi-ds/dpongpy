# Uncomment the following line to enable packet dropping
#export UDP_DROP_RATE := "0.2"

server:
    poetry run dpongpy -m centralised -r coordinator

client1:
    poetry run dpongpy -m centralised -r terminal --side left --keys wasd --host 127.0.0.1

client2:
    poetry run dpongpy -m centralised -r terminal --side right --keys arrows --host 127.0.0.1
