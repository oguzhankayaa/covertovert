from scapy.all import IP, Raw, sniff, ICMP
import random
import time
from CovertChannelBase import CovertChannelBase

class MyCovertChannel(CovertChannelBase):
    def __init__(self):
    
        pass

    def send(self, log_file_name,min_length , max_length,threshold):

        # Generate a random binary message based on the parameters
        binary_message = self.generate_random_binary_message_with_logging(
            log_file_name, min_length, max_length
        )
        #print(binary_message)
        
        #i=True #-> This is for capacity calculation.
        
        # Each bit in the binary message will correspond to a packet size.
        for bit in binary_message:
            # Determine packet size based on the bit value.
            if bit == '1':
                payload_size = random.randint(threshold, 2*threshold)  # Random size >= threshold   IMPORTANT: Threshold should be at least 2.
            else:
                payload_size = random.randint(int(threshold/2), threshold-1)   # threshold/2<= Random size < threshold
            # Create the packet with the chosen payload size
            packet = IP(dst="172.18.0.3")/Raw(b"\x00" * payload_size)  # Raw data of the chosen size
           

            
            """if(i):
                start_time = time.time() #---------> this is also for time calculations
                i=False
            """
            
            # Send the packet
            super().send(packet)
            
            
        #end_time = time.time()-(start_time) #for time calculations
        #print("end_time:", end_time)  #for time calculations


    def receive(self, parameter1, log_file_name):
        """
        - This function will receive the packets and decode the size to retrieve the binary message.
        """
        self.log_message("", log_file_name)
        
        decoded_message = ""  #----------->>this is the binary encoded message
        message="" #----------->>this is the char encoded message
        
        try:
            threshold = int(parameter1)  #Input validation check
        except ValueError:
            self.log_message("Error: Invalid parameter values for threshold.", log_file_name)
            return

        def stopfilter(x):    
            """
                Stop filter function for stopping sniffing
            """


            if len(message)>0 and message[-1]==".":   #If message ends with a dot log it and return true to stop sniffing. 
                #print(f"Decoded message: {decoded_message}")
                #print(f"message: {message}")
                self.log_message(message, log_file_name)
                return True
            return False

        def packet_callback(packet):
            """
                Message decoder function using payload size
            """
            nonlocal decoded_message 
            nonlocal message
            # Log callback invocation
            #print("Callback called")
            #print(packet)
            
            # If Packet has IP and Raw layers, process that packet.
            if packet.haslayer(IP) and packet.haslayer(Raw):
                #print("Raw layer detected")
                payload_size = len(packet[Raw])  #get size
                #print(f"Payload size: {payload_size}")
                
                # check for ICMP layer and if such layers exists, ignore that packet
                if packet.haslayer(ICMP):
                    return False



                # Decode message in bit level using payload size
                if threshold <= payload_size:
                    decoded_message += '1'
                else:
                    decoded_message += '0'
                
                #print(len(decoded_message))


                
                if len(decoded_message)%8==0:  ##For each 8 bits, get char value and add to message.
                    message+=self.convert_eight_bits_to_character(decoded_message[-8:])
            
            return True
        
        print("Starting sniffing...")
        sniff(prn=packet_callback, store=0,stop_filter=stopfilter) #do sniffing and stop according to stopfilter function
