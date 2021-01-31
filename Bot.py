import os, sys, traceback
import selenium, time, math, random
from selenium import webdriver


class Bot:

    def __init__(self):

        # Idle Bool
        self.idle = False

        # Bot Bools
        self.enemy_selected = False
        self.safe_mode = False

        # Bot Stats
        self.shot_count = 0
        self.enemies_killed = 0
        self.damage_dealt = 0

        # Enemies Killed
        self.normal_enemies_killed = 0
        self.shielded_enemies_killed = 0
        self.agile_enemies_killed = 0
        self.tough_enemies_killed = 0
        self.angry_enemies_killed = 0
        self.mad_enemies_killed = 0

        # Player stats
        self.primary_shot = 0
        self.special_shot = 0
        self.destructive_shot = 0

        # More Player Stats
        self.player_level = 0
        self.xp_before_fight = 0
        self.xp_after_fight = 0
        self.xp_gained = 0

        # Special Ammo Count
        self.special_ammo = 0

        # Level Variable String
        self.enemy_level = 'lv39'
        self.enemy_xpath = f'//div[contains(text(), "{self.enemy_level}")]'

        # Bot Account Info
        self.account_name = 'ACCOUNT NAME HERE'
        self.account_password = 'ACCOUNT PASSWORD HERE'

        # Browser Initiation
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.browser.set_window_size(800, 1440)
        self.browser.get('https://cybercodeonline.com/preLogin-l/login')

        # Browser login
        name = self.browser.find_elements_by_xpath('//input[@type = "email"]')[0]
        name.send_keys(self.account_name)

        password = self.browser.find_elements_by_xpath('//input[@type = "password"]')[0]
        password.send_keys(self.account_password)

        login_button = self.browser.find_elements_by_xpath(
            '/html/body/div/ion-app/ion-router-outlet/div/ion-content/div/div[2]/div[3]/div[2]/a')[0]
        login_button.click()

        time.sleep(5)

        music_button = self.browser.find_elements_by_xpath(
            '/html/body/div/ion-app/ion-router-outlet/div/ion-tabs/div/ion-router-outlet/div/ion-header/div/span/span')[
            0]
        music_button.click()

        tut = self.browser.find_elements_by_xpath('//span[contains(text(), "Tutorial")]')[0]
        tut.click()

    def calculate_xp_difference(self):
        self.add_xp = self.xp_after_fight - self.xp_before_fight
        pass

    def set_xp_after_fight(self):
        try:
            self.xp_after_fight = 0
            xp_before_fight = self.browser.find_elements_by_xpath(
                '//div[contains(@class, "absolute h-full w-full flex-1 justify-center items-center text-black-dark ")]/p')[
                0]
            xp_before_fight_list = xp_before_fight.text.split("/")
            self.xp_after_fight = int(xp_before_fight_list[0])
        except:
            print("CANT")

    def set_xp_before_fight(self):
        try:
            self.xp_before_fight = 0
            xp_before_fight = self.browser.find_elements_by_xpath(
                '//div[contains(@class, "absolute h-full w-full flex-1 justify-center items-center text-black-dark ")]/p')[
                0]
            xp_before_fight_list = xp_before_fight.text.split("/")
            self.xp_before_fight = int(xp_before_fight_list[0])
        except:
            print("CANT")

    def set_player_level(self):
        try:
            player_level_xpath = self.browser.find_elements_by_xpath("//div/span[contains(@class, 'text-sm pb-1')]")[0]
            self.player_level = player_level_xpath.text
        except:
            pass

    def scroll_to_top(self):
        try:
            self.browser.execute_script("self.browser.scrollTo(0, document.body.scrollHeight);")
        except:
            pass

    def refresh_enemies(self):
        try:
            enemy_refresh = self.browser.find_elements_by_xpath('//span[contains(text(), "Refresh Enemies")]')[0]
            enemy_refresh.click()
        except:
            pass

    def try_to_close_tut(self):
        try:
            tut = self.browser.find_elements_by_xpath('//span[contains(text(), "Tutorial")]')[0]
            tut.click()
        except:
            pass

    def main_loop(self):
        while True:
            if not self.idle:
                self.try_to_close_tut()
                self.scroll_to_top()
                if not self.enemy_selected:
                    try:
                        time.sleep(random.randint(1, 3))
                        # enemy = browser.find_elements_by_xpath('//*[@id="root"]/ion-app/ion-router-outlet/div/ion-tabs/div/ion-router-outlet/div/ion-content/div/div/div[2]/div[1]')[0]
                        enemy = self.browser.find_elements_by_xpath(self.enemy_xpath)[0]
                        enemy_name = enemy.find_elements_by_xpath(f'{self.enemy_xpath}/following::span')[0]
                        enemy.click()
                        self.enemy_selected = True
                        print('[SELECTED ENEMY]')
                        self.enemies_killed += 1

                        if 'Angry' in enemy_name.text:
                            self.angry_enemies_killed += 1

                        if 'Tough' in enemy_name.text:
                            self.tough_enemies_killed += 1

                        if 'Shielded' in enemy_name.text:
                            self.shielded_enemies_killed += 1

                        if 'Agile' in enemy_name.text:
                            self.agile_enemies_killed += 1

                        if 'Mad' in enemy_name.text:
                            self.mad_enemies_killed += 1

                        if not 'Angry' in enemy_name.text and not 'Tough' in enemy_name.text and not 'Shielded' in enemy_name.text:
                            self.normal_enemies_killed += 1




                    except:
                        print('[NO ENEMY]')
                        self.refresh_enemies()

                    self.try_to_close_tut()

                    time.sleep(random.randint(1, 2))
                elif self.enemy_selected:

                    self.try_to_close_tut()

                    time.sleep(random.randint(1, 3))

                    try:

                        self.special_ammo_xpath = self.browser.find_elements_by_xpath(
                            '//div[contains(@class, "flex-1 flex-row justify-around items-center text-primary")]/span[1]')[
                            0]
                        self.special_ammo = self.special_ammo_xpath.text

                        health = self.browser.find_elements_by_xpath(
                            '//div/p[contains(text(), "Health:")]/following::p[position() <=1]')
                        enemy_health = health[0]
                        player_health = health[1]

                        split_string_player_health = player_health.text
                        split_string_enemy_health = enemy_health.text

                        player_health_split = split_string_player_health.split('/')
                        enemy_health_split = split_string_enemy_health.split('/')

                        player_health_percentage_float = int(player_health_split[0]) / int(player_health_split[1])
                        player_health_percentage = math.floor(player_health_percentage_float * 100)

                        enemy_health_percentage_float = int(enemy_health_split[0]) / int(enemy_health_split[1])
                        enemy_health_percentage = math.floor(enemy_health_percentage_float * 100)

                        print('[ENEMY HEALTH PERCENTAGE]: ' + str(enemy_health_percentage),
                              '[PLAYER HEALTH PERCENTAGE]: ' + str(player_health_percentage))


                        time.sleep(0.5)

                        try:
                            if enemy_health_percentage >= 99:
                                print(enemy_health_percentage)
                                gun = self.browser.find_elements_by_xpath('//span[contains(text(), "destruct")]')[0]
                        except:
                            print('[NO ANTI-MATTER CHARGE]')

                        if int(enemy_health_split[0]) <= 1500:
                            gun = self.browser.find_elements_by_xpath('//span[contains(text(), "primary")]')[0]

                        elif int(enemy_health_split[0]) > 1500:
                            gun = self.browser.find_elements_by_xpath('//span[contains(text(), "special")]')[0]

                        if enemy_health_percentage <= 60 and player_health_percentage >= 75:
                            gun = self.browser.find_elements_by_xpath('//span[contains(text(), "primary")]')[0]


                    except:
                        pass

                    try:
                        gun.click()
                        if gun.text == 'PRIMARY':
                            print("PRIMARY")
                            self.primary_shot += 1
                        elif gun.text == 'SPECIAL':
                            print("SPECIAL")
                            self.special_shot += 1
                        elif gun.text == 'DESTRUCT.':
                            print("DESTRUCT.")
                            self.destructive_shot += 1

                        self.shot_count += 1
                        time.sleep(1)
                    except:
                        print('[NO ENEMY]')
                        self.enemy_selected = False
                        time.sleep(random.randint(1, 2))

                        self.refresh_enemies()

                        self.try_to_close_tut()

                        try:
                            take_all = self.browser.find_elements_by_xpath('//span[contains(text(), "Take all")]')[0]
                            take_all.click()
                        except:
                            [print("[NO LOOT]")]
