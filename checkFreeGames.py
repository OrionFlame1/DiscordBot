from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback


def getEpicGames():
    result = {}
    url = "https://store.epicgames.com/en-US/free-games"
    result["url"] = url
    driver = webdriver.Chrome()
    driver.get(url)

    elements = driver.find_elements(By.CSS_SELECTOR, "[data-component='FreeOfferCard'], [data-component='VaultOfferCard']")
    element_array = [element for element in elements]

    found_games = []
    for idx, element in enumerate(element_array):
        try:
            game = {}

            try:
                h6_tag = element.find_element(By.TAG_NAME, 'h6')
            except:
                continue

            game["title"] = h6_tag.text

            game["url"] = element.find_element(By.XPATH, "./*").get_attribute("href")
            # try:
            #     if "Free Now" in element.find_element(By.XPATH, "./*").get_attribute("aria-label"):
            #         game["free_now"] = True
            #     else:
            #         game["free_now"] = False
            # except Exception as e:
            #     traceback.print_exc()
            #     return e
            try:
                if element.find_element(By.XPATH, ".//span[contains(text(), 'Free Now')]"):
                    game["free_now"] = True
            except:
                game["free_now"] = False

            print(f"IDX: {idx} GAME: {game}")

            found_games.append(game)
        except Exception as e:
            traceback.print_exc()
            return e

    driver.quit()
    result["games"] = found_games
    return result


if __name__ == "__main__":
    print(getEpicGames())
