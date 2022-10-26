import socket
import time, sys
import math


    
file_name='phone_angles.txt'

#clear txt file of previous angles
open(file_name, 'w').close()
    

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to connect to phone')
    sys.exit()

print('Socket Created')

phone_IP= "192.168.0.10"
phone_PORT = 3211
#Connect to the TCP server on the phone using IP address and port 
client.connect((phone_IP,phone_PORT))

print('Socket Connected to ' + phone_IP )
msg_count=0
write_rate=1 #every X messages are written into the txt file, could be used to downsample the IMU data
roll_x_zero, pitch_y_zero, yaw_z_zero=[0,0,0]  #default angle values

 
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        link: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = round(math.atan2(t0, t1)*1000)/1000
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = round(math.asin(t2)*1000)/1000
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = round(math.atan2(t3, t4)*1000)/1000
     
        return roll_x, pitch_y, yaw_z # in radians

# realtime communication with phone
while True:
    try:
        msg = client.recv(1024).decode('ascii') #raw message
        print("message "+str(msg_count)+":"+msg)
        
        start_char='"value":['
        end_char=']}}'
        angles=(msg.split(start_char)[1].split(end_char)[0]).split(',')
        print("angles_x= "+angles[0])
        print("angles_y= "+angles[1])
        print("angles_z= "+angles[2])
        
        if msg_count==1:            #zero all angles form the rotation vector, second datstet since something first data package is wrong
            roll_x_zero, pitch_y_zero, yaw_z_zero=euler_from_quaternion(float(angles[0]),float(angles[1]),float(angles[2]),1)
              
        if len(msg)==0:    ## if length of message is zero, this means there is no message
            print("No data received, communication terminated on servers end.")
            sys.exit()
            
        elif msg_count % write_rate==0: #write every x messages the latest coordinates
            roll_x, pitch_y, yaw_z=euler_from_quaternion(float(angles[0]),float(angles[1]),float(angles[2]), 1)
            yaw_z-=yaw_z_zero  #zero orientation
            yaw_z=round(yaw_z*1000)/1000
            with open(file_name, 'a') as f:
                f.write(str(roll_x)+';'+str(pitch_y)+';'+str(yaw_z)+"\n")
        msg_count+=1
    except KeyboardInterrupt:
        print("Communication terminated on clients end.")
        sys.exit()
        
        

