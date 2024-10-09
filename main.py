import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

NYT_URL = 'https://www.nytimes.com/interactive/2024/books/best-books-21st-century.html'


def get_data(url):
    try:
        resp = requests.get(url)
        html = BeautifulSoup(resp.content, 'html.parser')
        return html

    except requests.HTTPError as http_ex:
        print(f"error! http exception: {http_ex}")

    except Exception as ex:
        print(f"error! other exception: {ex}")


def get_filtered_summary_list(summary_list):
    filtered_summary_list = []

    for summary in summary_list:
        summary_str = summary.text.strip()
        matches = re.search("^(Liked it?)|(Interested?)\w*", summary_str)

        if not matches:
            filtered_summary_list.append(summary_str)

    return filtered_summary_list


def populate_titles_and_authors(title_list, author_list):
    index = 0
    booklist_df = pd.DataFrame(columns=["title", "author"])

    for title in title_list:
        if index == 0:
            booklist_df.loc[index] = [title.text.strip(), None]
        else:
            booklist_df.loc[index] = [title.text.strip(), 
                                      author_list[index - 1].text.strip()]
        index += 1

    return booklist_df


def main():
    print("------------ starting script ------------")

    html_soup = get_data(NYT_URL)

    title = html_soup.title
    book_list = html_soup.find(id="all-books")
    title_list = book_list.find_all("h2")
    author_list = book_list.find_all("span", class_="author")
    # summary_list = book_list.find_all("p", class_="g-text")

    # filtered_summary_list = get_filtered_summary_list(summary_list)
    booklist_df = populate_titles_and_authors(title_list, author_list)
    booklist_df.to_csv("2024-nyt-best-books.csv", index=False)


main()

