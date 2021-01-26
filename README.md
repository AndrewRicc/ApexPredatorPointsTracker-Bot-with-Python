# ApexPredatorPointsTracker-Bot-with-Python
Python program to make a bot which you can receive Apex Legends ranked data

This program is made up to read the nickname of the channel in a file called "data.txt" in the same folder.
You should also add in the same folder an icon called "images.png"

If you want to create your own bot in the same way you have to create a new dedicated account and you have to registred it on https://twitchapps.com/tmi/ to get your own oauth token
Then you have to go on https://dev.twitch.tv/console and log in with your account bot and add a new application put in the oauth fields "https://localhost/<youroauthtoken>", call it how you want and save for you the oauth token and the clientID code.

Finally you can put insted of the placeholder your data and it will work

The program is made up to become a .exe file with PyInstaller librery. 
If you had any kind of problem with the .exe try to use this command to make your .exe:

py -m PyInstaller -F --hidden-import "pystray._win32" chatbot.py --noconsole --onefile

This shoud appens because some python module didn't import in the right way

If you had other problems with the .exe try to use this command:

py -m PyInstaller chatbot.py

Then let's run it on the cmd and see and import in the previous command the missing module 
