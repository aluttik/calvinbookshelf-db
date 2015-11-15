from json import load, dump
from scrape_booklist import scrape_books
from glob import glob

# finds terms that has books that haven't been scraped for
finished = [x[3:-5] for x in glob('db/*.json')]
terms = [x[5:-5] for x in glob('data/*.json')]
unfinished = sorted(list(set(terms) - set(finished)))[::-1]

# for each of these terms,
for t in unfinished:

    print 'loading class list from: data/%s.json' % t

    # open the appropriate 'section list' json file
    with open('data/%s.json' % t) as in_file:
        classlist = load(in_file)

    # parse out the section data from the classlist
    sections = [c.split('-', 2) for c in classlist]

    # scrape bkstr for a list of books for each section
    print 'scraping books for term=%s...' % t
    booklist = list()
    read_count = 0
    for section in sections:
        booklist.append(scrape_books(t, *section))
        read_count += 1
        print '[%d%%]\t%s' % (int(100*read_count/len(sections)), '-'.join(section))

    # dump the results to a json file in the db folder
    with open('db/%s.json' % t, 'w') as out_file: 
        dump(booklist, out_file, indent=4)
    print 'dumped results to db/%s.json\n' % t

print 'finished\n'
