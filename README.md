# Phone_IMU_Blender_object_control
video with the full explanation: https://youtu.be/aMQK_xXKQcY


1. Download the SensorStreamer application from the Play store: https://play.google.com/store/apps/details?id=cz.honzamrazek.sensorstreamer&hl=en&gl=US
2. Set the server and package settings in the application.
3. Find the IP adress of your smartphone in the local network
4. adapt the IP adress in the Python script
5. Run the script to see if a TXT file is being generated.
6. Download UPBGE, open the 'moving_phone.blend' file and set the sensor and controller as in the video if neccessary. https://upbge.org/#/
7. Adapt location of the generated 'phone_angles.txt' file in the script in UPBGE.


Start the real time phone mimicking.
1. Start the SensorStreamer session on your martphone.
2. Run the python script.
3. Run the render by pressing 'P'.
