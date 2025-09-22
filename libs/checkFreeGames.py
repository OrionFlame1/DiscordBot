import requests
import json

def getEpicGames():
    data = None
    try:
        response = requests.get("https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=RO&allowCountries=RO")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Assuming the data is in JSON format
    except requests.exceptions.RequestException as e:
        return e
    
    if data:
        data = json.loads(json.dumps(data))  # Ensure data is a JSON object

    free_games = []
    data = data["data"]
    if data["Catalog"]["searchStore"]["elements"]:
        elements = data["Catalog"]["searchStore"]["elements"]
        for element in elements:
            if element["promotions"] is not None:
                if len(element["promotions"]["promotionalOffers"]) > 0:
                    if element["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["discountSetting"]["discountPercentage"] == 0:
                        this_game_url = "https://store.epicgames.com/en-US/p/"
                        if element["productSlug"]:
                            this_game_url += element["productSlug"]
                        else:
                            this_game_url += element["catalogNs"]["mappings"][0]["pageSlug"]
                        free_games.append({
                            "title": element["title"],
                            "url": this_game_url,
                            "free_now": True,
                        })
                if len(element["promotions"]["upcomingPromotionalOffers"]) > 0:
                    if element["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]["discountSetting"]["discountPercentage"] == 0:
                        this_game_url = "https://store.epicgames.com/en-US/p/"
                        if element["productSlug"]:
                            this_game_url += element["productSlug"]
                        else:
                            this_game_url += element["catalogNs"]["mappings"][0]["pageSlug"]
                        free_games.append({
                            "title": element["title"],
                            "url": this_game_url,
                            "free_now": False,
                        })

    # sort the games by free_now status
    free_games.sort(key=lambda x: x["free_now"], reverse=True)

    return free_games

if __name__ == "__main__":
    print(getEpicGames())
