from actr import rpc_interface 


comet_socket = rpc_interface.start_connection()    
#comet_socket.setblocking(0)


move_socket = rpc_interface.start_connection()
#move_socket.setblocking(0)


