
class PlayerStats:
    def __init__(self, Requests, log, config):
        self.Requests = Requests
        self.log = log
        self.config = config

    def get_stats(self, puuid):
        if not self.config.get_table_flag("headshot_percent") and not self.config.get_table_flag("kd"):
            return {
                "kd": "N/a",
                "hs": "N/a"
            }

        response = self.Requests.fetch('pd', f"/mmr/v1/players/{puuid}/competitiveupdates?startIndex=0&endIndex=1&queue=competitive", "get")
        try:
            r = self.Requests.fetch('pd', f"/match-details/v1/matches/{response.json()['Matches'][0]['MatchID']}", "get")
            if r.status_code == 404: 
                return {
                "kd": "N/a",
                "hs": "N/a"
            }

            total_hits = 0
            total_headshots = 0
            for rround in r.json()["roundResults"]:
                for player in rround["playerStats"]:
                    if player["subject"] == puuid:
                        for hits in player["damage"]:
                            total_hits += hits["legshots"]
                            total_hits += hits["bodyshots"]
                            total_hits += hits["headshots"]
                            total_headshots += hits["headshots"]

            for player in r.json()["players"]:
                if player["subject"] == puuid:
                    kills = player["stats"]["kills"]
                    deaths = player["stats"]["deaths"]

            if deaths == 0:
                kd = kills
            elif kills == 0:
                kd = 0
            else:
                kd = round(kills/deaths, 2)
            final = {
                "kd": kd,
                "hs": "N/a"
            }


            if total_hits == 0: 
                return final
            hs = int((total_headshots/total_hits)*100)
            final["hs"] = hs
            return final
        except IndexError: 
            return {
                "kd": "N/a",
                "hs": "N/a"
            }


if __name__ == "__main__":
    from constants import version
    from requestsV import Requests
    from logs import Logging
    from errors import Error
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    Logging = Logging()
    log = Logging.log

    ErrorSRC = Error(log)

    Requests = Requests(version, log, ErrorSRC)

    r = PlayerStats(Requests, log, "a")

    res = r.get_stats("963ad672-61e1-537e-8449-06ece1a5ceb7")
    print(res)
