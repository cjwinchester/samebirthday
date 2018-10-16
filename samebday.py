import argparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL_BASE = 'https://en.wikipedia.org'


def generate_url(date):
    '''
    given a yyyy-mm-dd date, return a tuple with two things =>
        the year
        the correct wikipedia URL
    '''

    # 🎵 cut my date into pieces
    # this is my last resort 🎵
    year, month, day = [int(x) for x in date.split('-')]

    # format in the Wikipedia Way
    formatted_date = datetime(2018, month, day).strftime('%B_%d')

    # return year and URL
    return (year, f'{URL_BASE}/wiki/{formatted_date}')


def parse_wiki_bday(target_year, url):
    '''
    parse birthday list on the wikipedia page

    returns a tuple with two lists of data =>
        list of lists of peeps w/ *exact* same bday
        list of list of peeps w/ same bday different year
    '''

    # fetch the page
    r = requests.get(url)

    # turn it into soup
    soup = BeautifulSoup(r.text, 'html.parser')

    # target the correct list items
    birthdays = soup.find('span', {'id': 'Births'}) \
                    .parent.next_sibling.next_sibling \
                    .find_all('li')

    # make a couple of output lists
    exact_same_b = []
    other_b = []

    # loop over list items on the page
    for b in birthdays:

        # split out year born and person strings
        year, human = [x.strip() for x in b.text.split('–')]

        # grab the wikipedia link from the last `a`
        # tag inside that element
        href = b.find_all('a')[-1]['href']

        # turn it into a fully qualified URL
        url = f'{URL_BASE}{href}'

        # here the stuff is!
        data_out = [year, human, url]

        # after killing out "BC", does this person's
        # birthday year match the input year?
        # either way, append accordingly to an output list
        if int(year.replace('BC', '').strip()) == target_year:
            exact_same_b.append(data_out)
        else:
            other_b.append(data_out)

    # return those two lists
    return (exact_same_b, other_b)


if __name__ == '__main__':

    # load up that parser, baby
    parser = argparse.ArgumentParser()

    # add the one positional argument
    parser.add_argument('date', help='date in yyyy-mm-dd format')
    args = parser.parse_args()

    # grab the year and wikipedia URL
    yearurl = generate_url(args.date)

    # parse the page
    output = parse_wiki_bday(*yearurl)

    # assign the output to new variables
    exact_same_b, other_b = output

    # add up total records
    total = len(output[0]) + len(output[1])

    # then boom print out all the junk here
    print('')
    print(f'Found {total:,} famous birthday buds')
    print('🥓'*15)
    print('')

    print('🎉 EXACT SAME BIRTHDAY 🎉')
    for sb in exact_same_b:
        print(' - '.join(sb))

    print('')

    print('👉 same birthday different year 👈')
    for sb in other_b:
        print(' - '.join(sb))
