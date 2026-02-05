"""
fix_id0_servo.py

Fixes a Feetech servo stuck at ID=0 by changing it to ID=1.
IMPORTANT: Connect ONLY the problem servo before running this.

Run from anywhere with your LeRobot conda/venv activated:
    python fix_id0_servo.py
"""

import serial
import time
import sys

# ============ CONFIGURE THIS ============
PORT = "COM7"  # Change to your port (e.g., COM4, COM5)
NEW_ID = 1     # What ID to assign (1-253)
# ========================================

BAUDRATE = 1000000
BROADCAST_ID = 0xFE
CURRENT_ID = 0  # The stuck ID we're trying to fix

# Register addresses (from Feetech protocol)
ADDR_ID = 5           # ID register
ADDR_LOCK = 55        # EPROM lock register (0x37)

def calculate_checksum(packet):
    """Checksum = ~(ID + Length + Instruction + Params) & 0xFF"""
    return (~sum(packet[2:]) & 0xFF)

def build_write_packet(servo_id, address, data):
    """Build a WRITE instruction packet."""
    # FF FF ID LEN INST ADDR DATA... CHECKSUM
    instruction = 0x03  # WRITE
    length = 2 + len(data)  # instruction + addr + data count
    
    packet = [0xFF, 0xFF, servo_id, length, instruction, address] + data
    packet.append(calculate_checksum(packet))
    return bytes(packet)

def build_ping_packet(servo_id):
    """Build a PING instruction packet."""
    instruction = 0x01  # PING
    length = 2  # instruction + checksum info
    
    packet = [0xFF, 0xFF, servo_id, length, instruction]
    packet.append(calculate_checksum(packet))
    return bytes(packet)

def send_and_receive(ser, packet, expect_response=True, timeout=0.1):
    """Send packet and optionally wait for response."""
    ser.reset_input_buffer()
    ser.write(packet)
    
    if not expect_response:
        time.sleep(0.05)
        return None
    
    time.sleep(timeout)
    response = ser.read(ser.in_waiting)
    return response

def main():
    print("=" * 50)
    print("Feetech Servo ID=0 Fix Script")
    print("=" * 50)
    print(f"\nPort: {PORT}")
    print(f"Target: Change ID {CURRENT_ID} -> {NEW_ID}")
    print("\n⚠️  IMPORTANT: Only the problem servo should be connected!")
    print("    Disconnect all other servos from the bus.\n")
    
    input("Press Enter when ready (or Ctrl+C to cancel)...")
    
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
        print(f"\n✓ Opened {PORT} at {BAUDRATE} baud")
    except serial.SerialException as e:
        print(f"\n✗ Failed to open {PORT}: {e}")
        sys.exit(1)
    
    try:
        # Step 1: Try to ping ID=0 directly
        print("\n[1/5] Pinging ID=0...")
        ping_packet = build_ping_packet(CURRENT_ID)
        response = send_and_receive(ser, ping_packet, timeout=0.2)
        
        if response and len(response) >= 6:
            print(f"  ✓ Got response from ID=0: {response.hex()}")
        else:
            print(f"  ? No response from ID=0 (may still work via broadcast)")
        
        # Step 2: Ping via broadcast (servo should respond)
        print("\n[2/5] Pinging via broadcast...")
        ping_broadcast = build_ping_packet(BROADCAST_ID)
        response = send_and_receive(ser, ping_broadcast, timeout=0.2)
        
        if response and len(response) >= 6:
            detected_id = response[2] if len(response) > 2 else "?"
            print(f"  ✓ Servo responded! Detected ID: {detected_id}")
            print(f"    Raw: {response.hex()}")
        else:
            print("  ⚠ No response to broadcast ping (continuing anyway)")
        
        # Step 3: Unlock EPROM (write 0 to lock register)
        print("\n[3/5] Unlocking EPROM...")
        # Try unlocking at ID=0 first
        unlock_packet = build_write_packet(CURRENT_ID, ADDR_LOCK, [0])
        send_and_receive(ser, unlock_packet, expect_response=True)
        # Also try broadcast unlock
        unlock_broadcast = build_write_packet(BROADCAST_ID, ADDR_LOCK, [0])
        send_and_receive(ser, unlock_broadcast, expect_response=False)
        print("  ✓ Unlock commands sent")
        
        time.sleep(0.1)
        
        # Step 4: Write new ID using broadcast
        print(f"\n[4/5] Writing new ID={NEW_ID} via broadcast...")
        write_id_packet = build_write_packet(BROADCAST_ID, ADDR_ID, [NEW_ID])
        print(f"  Packet: {write_id_packet.hex()}")
        send_and_receive(ser, write_id_packet, expect_response=False)
        print("  ✓ ID change command sent")
        
        time.sleep(0.2)
        
        # Step 5: Lock EPROM at new ID
        print(f"\n[5/5] Locking EPROM at new ID={NEW_ID}...")
        lock_packet = build_write_packet(NEW_ID, ADDR_LOCK, [1])
        send_and_receive(ser, lock_packet, expect_response=True)
        print("  ✓ Lock command sent")
        
        time.sleep(0.1)
        
        # Verify: Ping new ID
        print(f"\n[Verify] Pinging new ID={NEW_ID}...")
        verify_ping = build_ping_packet(NEW_ID)
        response = send_and_receive(ser, verify_ping, timeout=0.2)
        
        if response and len(response) >= 6 and response[2] == NEW_ID:
            print(f"  ✓ SUCCESS! Servo now responds at ID={NEW_ID}")
            print(f"    Raw: {response.hex()}")
        else:
            print(f"  ? Could not verify. Try power cycling and scanning in FT Debug.")
            if response:
                print(f"    Got: {response.hex()}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
    finally:
        ser.close()
        print(f"\n✓ Closed {PORT}")
    
    print("\n" + "=" * 50)
    print("Done! Power cycle the servo, then scan in FT SCServo Debug.")
    print("=" * 50)

if __name__ == "__main__":
    main()
# ```

# **To run:**

# 1. **Disconnect all servos except the problem one** from the bus
# 2. Open your terminal with LeRobot environment activated
# 3. Save this script anywhere (e.g., `fix_id0_servo.py`)
# 4. Edit the `PORT = "COM3"` line to match your port
# 5. Run:
# ```
#    python fix_id0_servo.py