# Covert Channel Communication System

This project implements a covert channel communication system that hides messages within network packet payload sizes. Instead of sending messages directly, this system encodes information in the varying sizes of network packets, making the communication less detectable.

## Project Description

The core idea behind this covert channel is simple yet effective: we encode binary data ('0's and '1's) by manipulating the size of packet payloads. When sending a '1', we create a packet with a larger payload size, and when sending a '0', we use a smaller payload size. This creates a pattern that can be interpreted by the receiver to reconstruct the original message.

The system consists of two main components: a sender and a receiver. The sender converts messages into binary form and transmits them using carefully sized packets. The receiver captures these packets, analyzes their sizes, and reconstructs the original message.

## Parameters

The covert channel code is identified as "CSC-PSV-IP" and uses the following parameters:

### Sender Parameters
- `log_file_name`: Name of the log file where sent messages are recorded (default: "sent_message.log")
- `min_length`: Minimum length for the random binary message (default: 10)
- `max_length`: Maximum length for the random binary message (default: 1000) (We do not guarantee it works for too big values since memory managament and limitations of different systems)
- `threshold`: Value used to differentiate between '0' and '1' bits (default: 28) (must be greater or equal 2)

### Receiver Parameters
- `parameter1`: Threshold value that must match the sender's threshold (default: 28) 
- `log_file_name`: Name of the log file where received messages are recorded (default: "received_message.log")

Note: These parameters can be adjusted based on your specific needs, but ensure the threshold values match between sender and receiver for proper communication.

## Performance

Our implementation has been tested extensively, and the results show that it takes approximately 2.65 seconds to transmit a message consisting of 16 characters. Since each character requires 8 bits for transmission, this means we're sending 128 bits (16 characters × 8 bits) in 2.65 seconds, achieving a transmission rate of about 48.7 bits per second. This rate demonstrates a reasonable balance between reliability and speed for covert communication.

## Technical Details

The system works by creating packets with specific payload sizes. When encoding a '1', it creates a packet with a payload size between the threshold and twice the threshold. For a '0', it uses a size between half the threshold and just below the threshold.

### Why Threshold Must Be At Least 2

The minimum threshold requirement of 2 is crucial for the proper functioning of our system. Here's why:

Let's break down how payload sizes are calculated:
- For bit '0': payload_size = random(threshold/2, threshold-1)
- For bit '1': payload_size = random(threshold, 2*threshold)

If we used a threshold of 1:
- For bit '0': payload_size = random(0.5, 0)
  - This is impossible as we can't have a payload size less than 1 byte
- For bit '1': payload_size = random(1, 2)
  - This would work but provide very limited range

With a threshold of 2:
- For bit '0': payload_size = random(1, 1)
  - This gives us at least 1 byte to work with
- For bit '1': payload_size = random(2, 4)
  - This provides enough distinction from '0' bits

Therefore, a threshold of at least 2 ensures that:
1. We never attempt to create packets with invalid (zero or fractional) payload sizes
2. There's a clear distinction between packets representing '0' and '1'
3. We have enough range to add randomness to our payload sizes, making the channel more covert

## Important Considerations

The system is designed to stop receiving when it detects a period (.) at the end of the decoded message. This helps ensure complete message transmission and provides a clean way to terminate the communication.

The implementation filters out ICMP packets and only processes packets that contain both IP and Raw layers. This helps reduce noise and improve reliability.

## Requirements

To use this system, you'll need:
- Python 3.10.12
- Scapy library 
- Network access and appropriate permissions
- The CovertChannelBase class (included in the project)

Remember that network conditions and system configurations can affect the reliability of the covert channel. It's recommended to test the system in your specific environment and adjust the threshold values accordingly.

This implementation provides a foundation for covert communication, but you can extend and modify it to suit your specific needs. Feel free to experiment with different threshold values and message lengths to find the optimal configuration for your use case.