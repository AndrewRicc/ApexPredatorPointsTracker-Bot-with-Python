from bs4 import BeautifulSoup
from PIL import Image
import irc.bot, requests, time, pystray, psutil, threading, os

tLock = threading.Lock()

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel.lower()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json',
                   'Authorization': 'oauth:' + token}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username.lower(), username.lower())


    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        print('Joined ' + self.channel)
        print("Wrote: \"Connected!\"")

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection

        if cmd == "predator":
            try:
                page0 = requests.get("https://apex.tracker.gg/apex/leaderboards/stats/origin/RankScore?page=5")
                page1 = requests.get("https://apex.tracker.gg/apex/leaderboards/stats/origin/RankScore?page=1")
                url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
                headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
                r = requests.get(url, headers=headers).json()
                soup0 = BeautifulSoup(page0.content, "html.parser")
                soup1 = BeautifulSoup(page1.content, "html.parser")
                l_predator = soup0.find("table").find("tbody").find_all("tr")[-1].find_all("td")[-2]
                l_predator = str(l_predator)[-24:-22] + str(l_predator)[-21:-18]
                print(l_predator)
                c.privmsg(self.channel, f"L'ultimo predator sta a {l_predator}RP")
            except:
                print("Non trovato")
                c.privmsg(self.channel, "Classifica non trovata")
            finally:
                time.sleep(3)

        elif "rank" in cmd:
            try:
                username = cmd.split(" ")[1]
                page = requests.get("https://apex.tracker.gg/apex/profile/origin/"+username+"/overview")
                soup = BeautifulSoup(page.content, "html.parser")
                divVector = soup.find("div", "text").find_all("div")
                rank = divVector[0].string
                points = divVector[1]
                pos = divVector[2].string
                points = str(points).split(",")[0][-4:].strip() + str(points).split(",")[1][:4].strip()
                print(rank, points, pos)
                c.privmsg(self.channel, f"{username} è {rank} alla posizione {pos} ed il suo punteggio è {points}")
            except:
                try:
                    username = cmd.split(" ")[1]
                    page = requests.get("https://apex.tracker.gg/apex/profile/psn/"+username+"/overview")
                    soup = BeautifulSoup(page.content, "html.parser")
                    divVector = soup.find("div", "text").find_all("div")
                    rank = divVector[0].string
                    points = divVector[1]
                    pos = divVector[2].string
                    points = str(points).split(",")[0][-4:].strip() + str(points).split(",")[1][:4].strip()
                    print(rank, points, pos)
                    c.privmsg(self.channel, f"{username} è {rank} alla posizione {pos} ed il suo punteggio è {points}")
                except:
                    try:
                        username = cmd.split(" ")[1]
                        page = requests.get("https://apex.tracker.gg/apex/profile/xbl/"+username+"/overview")
                        soup = BeautifulSoup(page.content, "html.parser")
                        divVector = soup.find("div", "text").find_all("div")
                        rank = divVector[0].string
                        points = divVector[1]
                        pos = divVector[2].string
                        points = str(points).split(",")[0][-4:].strip() + str(points).split(",")[1][:4].strip()
                        print(rank, points, pos)
                        c.privmsg(self.channel, f"{username} è {rank} alla posizione {pos} ed il suo punteggio è {points}")
                    except:
                        print("Non trovato")
                        c.privmsg(self.channel, f"{username} non trovato")
            finally:
                time.sleep(3)

        elif cmd == "check":
            c.privmsg(self.channel, "Bot funzionante")
            time.sleep(3)




def action():
    print("Closing program")
    for process in psutil.process_iter():
        if process.name() == "chatbot.exe":
            process.kill()

def iconThread():
    tLock.locked()
    cThread = threading.current_thread()
    item = pystray.MenuItem
    if os.path.isfile("images.png"):
        image = Image.open("images.png")
        menu = (item(YourNameIcon_PLACEHOLDER, lambda : action()), item("Exit", lambda: action()))
        icon = pystray.Icon(YourNameIcon_PLACEHOLDER, image, YourNameIcon_PLACEHOLDER, menu)
        print("Icon run...")
        icon.run()
    else:
        print("Immagine non trovata")
    tLock.release()

def main():
    check = 0
    for process in psutil.process_iter():
        if process.name() == "chatbot.exe":
            check += 1
            break

    if os.path.isfile("data.txt"):
        if check == 1:
            f = open("data.txt", "r")
            nickname = f.read()
            threading._start_new_thread(iconThread, ())
            bot = TwitchBot(YourBotNickname_PLACEHOLDER, YourAppCliendID_PLACEHOLDER, YourBotoAuthCode_PLACEHOLDER, nickname)
            bot.start()
    else:
        print("File non trovato")


if __name__ == "__main__":
    main()
