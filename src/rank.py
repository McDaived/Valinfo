
class Rank:
    def __init__(self, Requests, log, content, ranks_before):
        self.Requests = Requests
        self.log = log
        self.ranks_before = ranks_before
        self.content = content

    def get_rank(self, puuid, seasonID):
        response = self.Requests.fetch('pd', f"/mmr/v1/players/{puuid}", "get")
        final = {
            "rank": None,
            "rr": None,
            "leaderboard": None,
            "peakrank": None,
            "wr": None,
            "numberofgames": 0,
            "peakrankact": None,
            "peakrankep": None,
            "statusgood": None,
            "statuscode": None,
            }
        try:
            if response.ok:
                r = response.json()
                rankTIER = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["CompetitiveTier"]
                if int(rankTIER) >= 21:

                    final["rank"] = rankTIER
                    final["rr"] = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["RankedRating"]
                    final["leaderboard"] = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["LeaderboardRank"]
                elif int(rankTIER) not in (0, 1, 2):
                    final["rank"] = rankTIER
                    final["rr"] = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["RankedRating"]
                    final["leaderboard"] = 0

                else:
                    final["rank"] = 0
                    final["rr"] = 0
                    final["leaderboard"] = 0

            else:
                self.log("failed getting rank")
                self.log(response.text)
                final["rank"] = 0
                final["rr"] = 0
                final["leaderboard"] = 0
        except TypeError:
            final["rank"] = 0
            final["rr"] = 0
            final["leaderboard"] = 0
        except KeyError:
            final["rank"] = 0
            final["rr"] = 0
            final["leaderboard"] = 0
        max_rank = final["rank"]
        max_rank_season = seasonID
        seasons = r["QueueSkills"]["competitive"].get("SeasonalInfoBySeasonID")
        if seasons is not None:
            for season in r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"]:
                if r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][season]["WinsByTier"] is not None:
                    for winByTier in r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][season]["WinsByTier"]:
                        if season in self.ranks_before:
                            if int(winByTier) > 20:
                                winByTier = int(winByTier) + 3
                        if int(winByTier) > max_rank:
                            max_rank = int(winByTier)
                            max_rank_season = season
            final["peakrank"] = max_rank
        else:
            final["peakrank"] = max_rank
        try:
            wins = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["NumberOfWinsWithPlacements"]
            total_games = r["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["NumberOfGames"]
            final["numberofgames"] = total_games
            try:
                wr = int(wins / total_games * 100)
            except ZeroDivisionError: 
                wr = 100
        except (KeyError, TypeError): 
            wr = "N/a"


        final["wr"] = wr
        final["statusgood"] = response.ok
        final["statuscode"] = response.status_code
        

        peak_rank_act_ep = self.content.get_act_episode_from_act_id(max_rank_season)
        final["peakrankact"] = peak_rank_act_ep["act"]
        final["peakrankep"] = peak_rank_act_ep["episode"]
        return final


if __name__ == "__main__":
    from constants import before_ascendant_seasons, version, NUMBERTORANKS
    from requestsV import Requests
    from logs import Logging
    from errors import Error
    import urllib3
    import pyperclip
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    Logging = Logging()
    log = Logging.log

    ErrorSRC = Error(log)

    Requests = Requests(version, log, ErrorSRC)
    
    s_id = "67e373c7-48f7-b422-641b-079ace30b427" 

    r = Rank(Requests, log, before_ascendant_seasons)

    res = r.get_rank("", s_id)
    print(res)
   
