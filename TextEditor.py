# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print("Please enter the number to choose which protocol you want to proceed with?\n\
      1. USER\n\
      2. PASS\n\
      3. WRITE\n\
      4. APPEND\n\
      5. UPDATE\n\
      6. EXIT")
      
protocol = input()

if protocol== 1:
    USER()
elif protocol==2:
    PASS()
elif protocol==3:
    WRITE()
elif protocol==4:
    APPEND()
elif protocol==5:
    UPDATE()
elif protocol==6:
    EXIT()
else :
    print("Invalid. Please try again.")
    
def USER(username):
    command = ("USER", username,"\r\n")
    converted = ascii(command)
    return converted

