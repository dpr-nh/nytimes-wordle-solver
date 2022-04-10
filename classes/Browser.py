from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class Browser:
    def __init__(self):
        self.words_entered = 0
        self.firefox = self.open_wordle()
        self.game_rows = self.get_game_rows()

        self.close_overlays()

    def __del__(self):
        self.firefox.close()

    def delete_element(self, element):
        self.firefox.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
        """, element)

    def close_overlays(self):
        # gdpr
        gdpr_banner = self.firefox.find_element(by=By.ID, value="pz-gdpr")
        self.delete_element(gdpr_banner)

        # instructions
        game_theme_manager = self.firefox.execute_script('''return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager")''')
        game_div = game_theme_manager.find_element(by=By.ID, value="game")
        game_modal = game_div.find_element(by=By.TAG_NAME, value="game-modal")
        self.delete_element(game_modal)

    def get_game_rows(self):
        return self.firefox.execute_script('''
            const rowsWithShadowRoots = document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelectorAll("game-row");
            return rows = [...rowsWithShadowRoots].map((row) => row.shadowRoot.children[1]);
        ''')

    def open_wordle(self):
        firefox = webdriver.Firefox()
        firefox.get("https://www.nytimes.com/games/wordle/index.html")
        assert "Wordle" in firefox.title

        return firefox

    def type_word(self, word):
        actions = ActionChains(self.firefox)
        actions.send_keys(word)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def get_word_results(self, word):
        self.type_word(word)
        time.sleep(2) # TODO: check animation has finished instead
        self.words_entered += 1

        # results
        current_row = self.game_rows[self.words_entered - 1]
        tiles = current_row.find_elements(by=By.TAG_NAME, value="game-tile")
        
        evaluations = []
        for tile in tiles:
            evaluations.append(tile.get_attribute("evaluation"))

        return evaluations
