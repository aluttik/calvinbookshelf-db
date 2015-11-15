from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

url = 'http://www.bkstr.com/calvinstore/CourseMaterialsResultsView'

def scrape_books(term, department, course, section):
    response = requests.get(url, params={
        'storeId': 371905,
        'termId': term,
        'departmentDisplayName': department,
        'courseDisplayName': course,
        'sectionDisplayName': section
    })
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        return {
            'term': term,
            'department': department,
            'course': course,
            'section': section,
            'instructor': find_instructor(soup),
            'books': find_books(soup.select('[id^=fldset-adoption]'))
        }
    except ValueError as e:
        print '-'.join([term, department, course, section]), find_instructor(soup)
        raise e

def find_instructor(soup):
    return soup.select_one('.efCourseName').text.split(':')[-1].strip()

def find_books(fields, required=True):
    books = list()
    for field in fields:
        if is_choice_list(field):
            options = field.select('.choice-list-content')
            choices = find_books(options, required=False)
            books.extend(choices)
        else:
            books.append({
                'required': required,
                'author': find_author(field),
                'edition': find_edition(field),
                'isbn': find_isbn(field),
                'title': find_title(field),
                'store_price': find_store_price(field),
                'thumbnail': find_thumbnail(field)
            })
    return books

def is_choice_list(f):
    return 'choice-title' in f.select_one('.material-group-title')['class']

def _find_detail(f, _id):
    tag = f.select_one('.material-group-edition').find(id=_id)
    if tag is None: return None
    text = tag.text.split(':', 1)[1].strip()    
    return text if text != 'N/A' else None

def find_title(f):
    return f.select_one('.material-group-title').text.splitlines()[0]

def find_author(f): 
    return _find_detail(f, 'materialAuthor')

def find_edition(f):
    return _find_detail(f, 'materialEdition')

def find_isbn(f):
    isbn_string = _find_detail(f, 'materialISBN')
    return int(isbn_string) if isbn_string is not None else None

def find_store_price(f):
    rows = f.select_one('.material-group-table').table.find_all('tr')[1:]
    column = lambda x: [row.find_all('td')[x-1].text.strip() for row in rows]
    offers = filter(lambda x: x[0] != 'Digital', zip(column(2), column(8)))
    try:
        return min([float(x[1][1:]) for x in offers]) if offers else None
    except ValueError as e:
        print f
        raise e
def find_thumbnail(f):
    return 'http:' + f.find(id='materialTitleImage').img['src']

if __name__ == '__main__':
    from json import dumps
    from sys import argv
    terms = {
        '15/FA': 100038417,
        '16/IN': 100039643,
        '16/SP': 100039644
    }
    term = terms[argv.pop(1)] if argv[1] in terms.keys() else terms['15/FA']
    assert(len(argv) > 2)
    if len(argv) == 3: argv.append('A')
    print dumps(scrape_books(term, *argv[1:]), indent=4)
