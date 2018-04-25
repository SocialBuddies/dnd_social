import json
import re
import time
from selenium import webdriver


def phb_spells():
    """
    scrapes all spells from https://www.5thsrd.org/spellcasting/spell_indexes/spells_by_name/
    classes of who cna cast it will be added later
    """

    url = "https://www.5thsrd.org/spellcasting/spell_indexes/spells_by_name/"
    driver = webdriver.Chrome()
    driver.get(url)

    # gather all spell urls
    spells_urls = []
    parts = driver.find_element_by_css_selector('div.col-md-9[role="main"')
    by_letter = parts.find_elements_by_css_selector('p')
    for letter in by_letter:
        spells = letter.find_elements_by_css_selector('a')
        for spell in spells:
            spells_urls.append(spell.get_attribute('href'))

    spells = []
    for url in spells_urls:
        driver.get(url)
        obj = driver.find_element_by_css_selector('div.col-md-9[role="main"')

        level = obj.find_elements_by_css_selector('p')[0].text
        found = re.findall(r'[0-9]+', level)
        if len(found) == 1:
            level = int(found[0])

        problem_found = []
        stats = obj.find_elements_by_css_selector('p')[1]

        casting_time = ""
        range = ""
        components = ""
        duration = ""
        description = ""
        try:
            parts = stats.text.splitlines()
            pieces = {"casting time": '',
                      "components": '',
                      "range": '',
                      "duration": ''}
            for i in parts:
                try:
                    pik = i.split(":")
                    if len(pik) > 1:
                        pieces[pik[0].lower()] = (" ".join(pik[1:]))
                except KeyError:
                    problem_found.append(url)

            try:
                spell_name = obj.find_element_by_css_selector('h1').text
            except:
                problem_found.append(url)
                spell_name = url

            try:
                description = obj.find_elements_by_css_selector('p')[2].text
            except IndexError:
                problem_found.append(url)
                try:
                    description = stats.find_elements_by_css_selector('strong')[3].text
                except IndexError:
                    description = ''
                    spell_name = url

            try:
                higher = obj.find_elements_by_css_selector('p')[4].text
            except IndexError:
                problem_found.append(url)
                extra = ''

            if extra:
                try:
                    extra = higher.find_elements_by_css_selector('strong')[0].text
                except IndexError:
                    problem_found.append(url)
                    extra = higher.text
        except:
            problem_found.append(url)
            spell_name = url

        spells.append({
            "name": spell_name,
            "url": url,
            "level": level,
            # klasses = models.ManyToManyField()
            "casting_time": pieces['casting time'],
            "range": pieces['range'],
            "components": pieces['components'],
            "duration": pieces['duration'],
            "description": description,
            "higher_level": extra,
        })

        time.sleep(0.3)

    with open('scrapers/spells/phb_spells.json', 'w') as s:
        s.write(json.dumps(spells))

    with open('scrapers/spells/phb_spell_problems.json', 'w') as s:
        s.write(json.dumps(problem_found))
