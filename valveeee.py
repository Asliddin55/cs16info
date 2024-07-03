import valve.source
import valve.source.a2s
import valve.source.master_server
import valve
from valve.source.rcon import RCON

SERVER_ADDRESS = ("185.217.131.10", 27777)
PASSWORD = "112233"

with RCON(SERVER_ADDRESS, PASSWORD) as rcon:
    print(rcon("echo Hello, world!"))
    print(rcon("status"))
    print(rcon("say Goodbye, world!"))
    print(rcon("quit"))
    print(rcon("disconnect"))
with valve.source.master_server.MasterServerQuerier() as msq:
    try:
        for address in msq.find(region=[u"eu", u"as"],
                                gamedir=u"tf",
                                map=u"ctf_2fort"):
            with valve.source.a2s.ServerQuerier(address) as server:
                info = server.info()
                players = server.players()
            print("{player_count}/{max_players} {server_name}".format(**info))
            for player in sorted(players["players"],
                                 key=lambda p: p["score"], reverse=True):
                print("{score} {name}".format(**player))
    except valve.source.NoResponseError:
        print ("Master server request timed out!")