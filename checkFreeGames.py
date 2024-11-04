from selenium import webdriver
from selenium.webdriver.common.by import By


def getEpicGames():
    result = {}
    url = "https://store.epicgames.com/en-US/free-games"
    result["url"] = url
    driver = webdriver.Chrome()
    driver.get(url)

    elements = driver.find_elements(By.XPATH, "//*[@data-component='FreeOfferCard']")
    element_array = [element for element in elements]

    found_games = []
    for idx, element in enumerate(element_array):
        try:
            game = {}

            h6_tag = element.find_element(By.TAG_NAME, 'h6')
            game["title"] = h6_tag.text

            game["url"] = element.find_element(By.XPATH, "./*").get_attribute("href")

            if "Free Now" in element.find_element(By.XPATH, "./*").get_attribute("aria-label"):
                game["free_now"] = True
            else:
                game["free_now"] = False

            found_games.append(game)
        except Exception as e:
            return e

    driver.quit()
    result["games"] = found_games
    return result


if __name__ == "__main__":
    print(getEpicGames())
