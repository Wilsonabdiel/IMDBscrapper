import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
# to relearn
def get_imdb_top50(year):
    dataset_location = os.path.realpath(os.path.join(os.path.dirname(__file__), "DataSets"))
    current_year = datetime.datetime.now().year

    if year > current_year:
        print(f"No movies are recorded in the year {year} yet!")
        return

    # Create the output file fd
    output_file_path = os.path.join(dataset_location, f"IMDB_Top50_{year}.txt")

    with open(output_file_path, 'w+') as output_file:
        headers = {'User-agent': 'Mozilla/5.0'}
        url = f"http://www.imdb.com/search/title?release_date={year},{year}&title_type=feature"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find('div', attrs={'class': 'article'}).find('h1')
        print(article.contents[0] + ': ', file=output_file)

        movie_list = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
        for i, div_item in enumerate(tqdm(movie_list, desc=f"Scraping {year} movies")):
            div = div_item.find('div', attrs={'class': 'lister-item-content'})
            print(f"{i + 1}.", file=output_file)
            header = div.findChildren('h3', attrs={'class': 'lister-item-header'})
            movie_title = header[0].findChildren('a')[0].contents[0].encode('utf-8').decode('ascii', 'ignore')
            print(f"Movie: {movie_title}", file=output_file)

if __name__ == "__main__":
    input_year = int(input("Please enter the start year (e.g., 2016): "))
    get_imdb_top50(input_year)
