from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as is_clickable 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from locale import setlocale, LC_ALL, strcoll
from functools import cmp_to_key
from json import dump
from time import sleep
from sys import argv
from os import environ

# opens a new chromedriver window
driver = webdriver.Chrome(executable_path=environ['CHROMEDRIVER_PATH'])
url = 'http://www.bkstr.com/calvinstore/shop/textbooks-and-course-materials'

select_tag_hierarchy = [
    'termId',
    'departmentId',
    'courseId',
    'sectionId'
]

def wait_until_clickable(element_name):
    locator = (By.NAME, element_name)
    return WebDriverWait(driver, 3).until(is_clickable(locator))

def get_options(select_name):
    def wrapper():
        has_placeholder = lambda x: x[0].text.startswith('Select')
        opts = Select(wait_until_clickable(select_name)).options
        return opts[1:] if opts and has_placeholder(opts) else opts
    return wrapper

def select_option(s_name, value):
    Select(wait_until_clickable(s_name)).select_by_value(value)

def scrape_classes(**kwargs):
    try:
        # opens a browser and go to bookstore website
        driver.get(url)
        # scrapes for the class list
        data = scrape(**kwargs)
        # prepares and returns the scraped data
        print 'preparing class list data...',
        classlist = prepare_list(data)
        print 'done'
        return classlist
    finally:
        # closes the browser
        driver.quit()

def scrape(depth=0, indent=4, delay=0.8):
    # let elements load
    sleep(delay)
    this_select = select_tag_hierarchy[depth]
    opts = get_options(this_select)
    # base case
    if this_select == 'sectionId': return [o.text for o in opts()]
    # recursive step
    next_select = select_tag_hierarchy[depth+1]
    options = {}
    for o in opts():
        value = o.get_attribute('value')
        select_option(this_select, value)
        print '\n%s%s' % (' '*depth*indent, value),
        options.update({value : scrape(depth=depth+1, delay=delay)})
    return options

def dump_terms(data):
    for t, term in data.iteritems():
        results = list()
        for d, dept in term.iteritems():
            for c, course in dept.iteritems():
                for s in course:
                    results.append('-'.join([d, c, s]))
        with open('data/%s.json' % t, 'w') as out_file:
            dump(sort_list(results), out_file, indent=4)
        print 'dumped term list to data/%s.json' % t

def prepare_list(data):
    setlocale(LC_ALL, 'en_US.UTF-8')
    sort_list = lambda x: sorted(x, key=cmp_to_key(strcoll))
    results = dict()
    for t, term in data.iteritems():
        classes = list()
        for d, dept in term.iteritems():
            for c, course in dept.iteritems():
                for s in course:
                    classes.append('-'.join([d, c, s]))
        results.update(classes)
    print 'done'
    return results

if __name__ == '__main__':
    if len(argv) > 1:
        data = scrape_classes(delay=float(argv[1]))
    else:
        data = scrape_classes()
    dump_terms(data)
    print 'finished\n'
