# Emotion-detection-on-Raspberry-Pi
Timed.py takes in images fed to it from raspberry pi camera module. It then extracts the emotions detected in the faces. The information regarding the the number of people and their corresponding emotions is assembled into a JSON packet as per the protocol set between the client side and server and sends the JSON packet to the server. This occurs periodically every 60 seconds according to the settings of the scheduler in timed.py
