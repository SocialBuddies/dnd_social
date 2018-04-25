import json
import re
import time
from selenium import webdriver


class Looks(object):
    def __init__(self):
        self.fields = ['base', 'body', 'face', 'hair', 'marks', 'other', 'disability', 'physical_skills',
                       'conflict_style_physical', 'conflict_style_verbal', 'emotional_expressions', 'personality_quirks']

        # set all attributes
        for field in self.fields:
            setattr(self, field, open('scrapers/looks/%s.txt' % field, 'a+'))
            setattr(self, "start_" + field, set(getattr(self, field).readlines()))
            setattr(self, "end_" + field, set())

    def scrape_parts(self, table):
        for key, values in table.items():
            to_add = []
            for val in values:
                if not val:
                    continue

                parts = val.split('\n')
                to_add += parts
            for v in to_add:
                getattr(self, "end_" + key).add(v)

    def save_fields(self):
        for field in self.fields:
            f = getattr(self, field)

            lines = getattr(self, "end_" + field) - getattr(self, "start_" + field)
            for l in lines:
                f.write('%s\n' % l)
            f.close()


def scrape_looks():
    """
    scrapes all spells from https://www.5thsrd.org/spellcasting/spell_indexes/spells_by_name/
    classes of who cna cast it will be added later
    """

    url = "http://klh.karinoyo.com/generate/character/"
    driver = webdriver.Chrome()
    driver.get(url)

    # load all parts
    looks = Looks()

    for i in range(100):
        print(i)
        # click 4 buttons
        buttons = driver.find_elements_by_css_selector('.btn.btn-default')
        for button in buttons:
            button.click()
        
        # extract the parts
        raw_table = driver.find_element_by_css_selector("tbody")
        rows = raw_table.find_elements_by_css_selector("tr")
        table = {}
        for row in rows[1:]:
            cells = row.find_elements_by_css_selector("td")
            key = cells[0].text.replace(",", "").replace(" ", "_").lower()
            tmp = []
            for cell in cells[1:]:
                ps = cell.find_elements_by_css_selector('p')
                divs = cell.find_elements_by_css_selector('div')
                if ps:
                    tmp += [p.text for p in ps]
                elif divs:
                    tmp += [d.text for d in divs]
                else:
                    tmp.append(cell.text)
            table[key] = tmp

        looks.scrape_parts(table)
    looks.save_fields()