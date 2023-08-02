import requests
from bs4 import BeautifulSoup
import json
import string


def find_word_count(chap_link):
    """
    Find word counts for the provided chapter link
    :param chap_link:
    :return:
    """

    chapter_data = requests.get(chap_link)

    chapter_content = BeautifulSoup(chapter_data.content, 'html.parser')

    div = chapter_content.find('div', class_='entry-content')

    paragraphs = div.find_all('p')

    total_words = 0
    for paragraph in paragraphs:
        # remove punctuation from getting counted
        translator = str.maketrans('', '', string.punctuation)
        text_without_punctuation = paragraph.get_text().translate(translator)

        # turn to a list to find the amount of words
        words = text_without_punctuation.split()
        words_in_paragraph = len(words)

        total_words += words_in_paragraph

    return total_words


def update_chapter_count(file_name, chapters_size):
    """

    :param file_name: the name of the .json file that carries the current # of chapters
    :param chapters_size: the amount of chapters currently out right now
    :return: the number of new chapters (usually is 1 but sometimes can be more)
    """

    new_chaps = 0

    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            chapter_count = data.get('chapter_count', 0)
            if chapters_size > chapter_count:
                new_chaps = (chapters_size - chapter_count)  # increment the chapter count
                chapter_count = chapters_size
                data['chapter_count'] = chapter_count
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error updating chapter count")

    with open(file_name, 'w') as file:
        json.dump({'chapter_count': chapter_count}, file, indent=4)

    return new_chaps


def get_newest_chapters():
    """
    Get the newest chapters' titles and word counts
    :return: dictionary with the new chapters and their associated word counts
    """

    file_name = 'chapter_count.json'

    url = 'https://witchculttranslation.com/arc-8/'

    # scrape website data, specifically the li elements (chapters)
    data = requests.get(url)

    chapters = []

    if data.status_code == 200:
        arc_content = BeautifulSoup(data.content, 'html.parser')
        div = arc_content.find('div', class_='entry-content')
        items = div.find_all('li')
        print()
        # not all li elements are chapters, so we have to filter
        for item in items:
            if item.text.startswith("Chapter"):
                chapters.append(item)
    else:
        print('Error')

    new_chapter_count = update_chapter_count(file_name, len(chapters))

    new_chapters_wc = {}  # dictionary containing chapters as keys and word count as values

    if new_chapter_count > 0:
        for ch in chapters[-new_chapter_count:]:
            ch_link = ch.find('a')['href']
            new_chapters_wc[ch.get_text()] = find_word_count(ch_link)

    return new_chapters_wc
