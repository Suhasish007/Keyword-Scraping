import logging
import requests
from bs4 import BeautifulSoup
import csv
import time

# Set up logging
log_file_path = '/Users/suhasishbasak/InstagramHashtagPredictor/scraper.log'  # Update this to a valid path
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_to_int(value):
    if 'M' in value:
        return int(float(value.replace('M', '')) * 1_000_000)
    elif 'K' in value:
        return int(float(value.replace('K', '')) * 1_000)
    else:
        return int(value.replace(',', ''))

def scrape_instagram_hashtag(hashtag):
    try:
        url = f'https://www.instagram.com/explore/tags/{hashtag}/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tag = soup.find('meta', attrs={'property': 'og:description'})
            if meta_tag:
                content = meta_tag['content']
                post_count = content.split(' ')[0]
                return convert_to_int(post_count)
        return None
    except Exception as e:
        logging.error(f"Error while scraping {hashtag}: {e}")
        return None

def collect_data(hashtags, filename="hashtag_data.csv"):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for hashtag in hashtags:
                post_count = scrape_instagram_hashtag(hashtag)
                if post_count is not None:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"Scraped data for {hashtag}: {timestamp}, {post_count}")
                    writer.writerow([timestamp, hashtag, post_count])
                else:
                    logging.error(f"Failed to scrape post count for {hashtag}.")
    except Exception as e:
        logging.error(f"Error during data collection: {e}")

if __name__ == "__main__":
    hashtags = [
        "digitalfashion", "virtualfashion", "ARgarment", "VRgarment", "ARclothing",
        "VRclothing", "ARfashion", "VRfashion", "digitalgarment", "digifash",
        "metaversefashion", "web3fashion", "web4fashion", "fashionNFT", "NFTfashion",
        "fashionAI", "AIfashion", "cryptofashion", "augmentedfashion", "gamingfashion",
        "gamefashion", "fashiongaming", "augmentedrealityfashion", "virtualrealityfashion",
        "spatialrealityfashion", "webgarment", "web3garment", "web4garment",
        "metaversegarment", "fashionskin"
    ]
    collect_data(hashtags)
