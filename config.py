# config.py
#
# Contains all global cross-code constants and variables

# Change the value of UMD_IOT_PASSWORD to the password provided
# during your umd-iot device registration process
UMD_IOT_PASSWORD = '7JMQVzdpDp4K'

# WiFi ssid / password pairs -- you can add more networks as 
# separate (ssid,pass) entries in the list
WIFI_NETWORKS = [('umd-iot', UMD_IOT_PASSWORD)]
