import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def dwarf_names(name_type='Realistic', cycles=1000):
    def generate_names(driver, gender, name_type):
        driver.get(url)
        form = driver.find_element_by_id('dice')
        form.find_element_by_xpath("//select[@name='nametype']/option[text()='Both']").click()
        form.find_element_by_xpath("//select[@name='numnames']/option[text()='100']").click()
        form.find_element_by_xpath("//select[@name='gender']/option[text()='%s']" % gender).click()
        form.find_element_by_xpath("//select[@name='surnametype']/option[text()='%s']" % name_type).click()
        time.sleep(1)
        form.find_element_by_css_selector('input[value="Generate!"]').click()

        # find and return names
        parent = driver.find_element_by_class_name('forum')
        child = parent.find_element_by_css_selector('table')
        names_table = child.find_element_by_css_selector('table')
        names = names_table.find_elements_by_css_selector('td')
        return names[1:]

    url = "http://www.rdinn.com/generators/1/dwarven_name_generator.php"
    driver = webdriver.Chrome()

    f_surnames = open('scrapers/names/dwarf_surnames.txt', 'a+')
    start_surnames = set(f_surnames.readlines())
    end_surnames = set()
    for gender in ['Female', 'Male']:
        f_names = open('scrapers/names/dwarf_%s_names.txt' % gender.lower(), 'a+')
        start_names = set(f_names.readlines())
        end_names = set()
        for i in range(1, cycles + 1):
            print("cycle %s/%s" % (i, cycles))
            for full_name in generate_names(driver, gender, name_type):
                name, surname = full_name.text.split(' ')
                end_names.add(name)
                end_surnames.add(name)

        f_names.write('\n'.join(end_names - start_names))
        f_names.close()

    f_surnames.write('\n'.join(end_surnames - start_surnames))
    f_surnames.close()


def elf_names(cycles=1000):
    def generate_names(driver, gender):
        driver.get(url)
        form = driver.find_element_by_id('dice')
        form.find_element_by_xpath("//select[@name='nametype']/option[text()='Both']").click()
        form.find_element_by_xpath("//select[@name='numnames']/option[text()='100']").click()
        form.find_element_by_xpath("//select[@name='gender']/option[text()='%s']" % gender).click()
        time.sleep(1)
        form.find_element_by_css_selector('input[value="Generate!"]').click()

        # find and return names
        parent = driver.find_element_by_class_name('forum')
        child = parent.find_element_by_css_selector('table')
        names_table = child.find_element_by_css_selector('table')
        names = names_table.find_elements_by_css_selector('td')
        return names[1:]

    url = "http://www.rdinn.com/generators/2/elven_name_generator.php"
    driver = webdriver.Chrome()

    f_surnames = open('scrapers/names/elf_surnames.txt', 'a+')
    start_surnames = set(f_surnames.readlines())
    for gender in ['Female', 'Male']:
        f_names = open('scrapers/names/elf_%s_names.txt' % gender.lower(), 'a+')
        start_names = set(f_names.readlines())
        for i in range(1, cycles + 1):
            try:
                print("cycle %s/%s" % (i, cycles))
                for full_name in generate_names(driver, gender):
                    name, surname = full_name.text.split(' ')
                    start_names.add(name)
                    start_surnames.add(surname)
                    f_names.write('%s\n' % name)
                    f_surnames.write('%s\n' % surname)
            except:
                pass

            f_names.close()
            f_surnames.close()


def fantasynamegenerators(race, cycles=1000):
    def generate_names():
        div = driver.find_element_by_id("nameGen")
        driver.execute_script("return arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-10);", div)
        inputs = div.find_elements_by_css_selector("input")
        if len(inputs) > 1:
            if gender == "female":
                inputs[1].click()
            else:
                inputs[0].click()
        else:
            inputs[0].click()
        # try:
        #     driver.find_element_by_css_selector('input[value="Get %s names"]' % gender).click()
        # except Exception as exc:
        #     driver.find_element_by_css_selector('input[value="%s names"]' % gender.title()).click()
        time.sleep(0.3)
        result = driver.find_element_by_id('result').text

        print(len(result.split('\n')))
        return result.split('\n')

    RACES = {
        'aasimar': [
            'http://www.fantasynamegenerators.com/dnd-aasimar-names.php',
        ],
        'dwarf': [],
        'halfling': [
            'http://www.fantasynamegenerators.com/dnd-halfling-names.php',
            # 'http://www.fantasynamegenerators.com/pathfinder-halfling-names.php',
            # 'http://www.fantasynamegenerators.com/the-witcher-halfling-names.php'
        ],
        'elf': [
            'http://www.fantasynamegenerators.com/dnd-elf-names.php'
        ],
        "gnoll": ["http://www.fantasynamegenerators.com/gnoll-names.php"],
        'human': [
            'http://www.fantasynamegenerators.com/dnd-human-names.php',
        ],
        'orc': [
            'http://www.fantasynamegenerators.com/dnd-orc-names.php'
        ],
        'dragonborn': [
            'http://www.fantasynamegenerators.com/dnd-dragonborn-names.php'
        ],
        "merfolk": ["http://www.fantasynamegenerators.com/mtg-merfolk-names.php"],
        'gnome': [
            'http://www.fantasynamegenerators.com/dnd-gnome-names.php'
        ],
        'half_orc': [
            'http://www.fantasynamegenerators.com/dnd-half-orc-names.php'
        ],
        'deep_gnome': [
            'http://www.fantasynamegenerators.com/dnd-deep-gnome-names.php'
        ],
        'thiefling': [
            'http://www.fantasynamegenerators.com/pathfinder-tiefling-names.php'
        ],
        "drow": [
            "http://www.fantasynamegenerators.com/dnd-drow-names.php"
        ],
        "giant": ["http://www.fantasynamegenerators.com/giant-names.php"],
        "kobold": ["http://www.fantasynamegenerators.com/pathfinder-kobold-names.php"],
        "goliath": ["http://www.fantasynamegenerators.com/dnd-goliath-names.php"],
        "goblin": ['http://www.fantasynamegenerators.com/goblin-names.php', "http://www.fantasynamegenerators.com/goblin_wow_names.php"]

    }

    driver = webdriver.Chrome()
    f_surnames = open('scrapers/names/fng_%s_surnames.txt' % race, 'a+')
    start_surnames = set(f_surnames.readlines())
    f_nicknames = open('scrapers/names/fng_%s_surnames.txt' % race, 'a+')
    start_nicknames = set(f_surnames.readlines())
    for gender in ['female', 'male']:
        f_names = open('scrapers/names/fng_%s_%s_names.txt' % (race, gender), 'a+')
        start_names = set(f_names.readlines())
        for url in RACES[race]:
            driver.get(url)

            time.sleep(1)
            for i in range(1, cycles + 1):
                try:
                    print("cycle %s/%s" % (i, cycles))
                    for full_name in generate_names():
                        if len(full_name.split(" ")) == 3:
                            name, nickname, surname = full_name.split(" ")
                        elif len(full_name.split(" ")) == 1:
                            name = full_name
                            nickname, surname = None, None
                        else:
                            name, surname = full_name.split(' ')
                            nickname = None

                        start_names.add(name)
                        f_names.write('%s\n' % name)
                        if surname:
                            start_surnames.add(surname)
                            f_surnames.write('%s\n' % surname)
                        if nickname:
                            start_nicknames.add(nickname)
                            f_nicknames.write('%s\n' % nickname)
                except Exception as exc:
                    print(exc)

        f_names.close()
    f_surnames.close()
    f_nicknames.close()
fantasynamegenerators.RACES = [
    'aasimar',
    'dwarf',
    'halfling',
    'elf',
    'human',
    'orc',
    'dragon_born',
    'gnome',
    'half_orc',
    'deep_gnome',
    'thiefling',
]