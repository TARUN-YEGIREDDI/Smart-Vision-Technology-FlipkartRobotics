import requests
from bs4 import BeautifulSoup
import os

# Create a folder to save the images
if not os.path.exists('grocery_images'):
    os.makedirs('grocery_images')

# Function to download images from a URL
def download_image(img_url, img_name):
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(f'grocery_images/{img_name}.jpg', 'wb') as file:
            file.write(response.content)

# Flipkart URL for groceries
url = 'https://www.flipkart.com/safe-harvest-peanut-whole-pesticide-free/p/itmfbd3w54apnrh6?pid=PLSFYPSND9KUXP7B&lid=LSTPLSFYPSND9KUXP7BCM1IPI&marketplace=GROCERY&fm=productRecommendation%2Fsimilar&iid=R%3As%3Bp%3APLSGHF5EKPAGR49Z%3Bl%3ALSTPLSGHF5EKPAGR49ZGCTIEL%3Bpt%3App%3Buid%3Ae3301329-839c-11ef-a57a-d13fd8cdfa96%3B.PLSFYPSND9KUXP7B&ppt=pp&ppn=pp&ssid=z7091fgokw0000001728189522348&otracker=pp_reco_Similar%2BProducts_2_33.productCard.PMU_HORIZONTAL_safe%2Bharvest%2BPeanut%2B%2528Whole%2529%2B%2528Pesticide%2BFree%2529_PLSFYPSND9KUXP7B_productRecommendation%2Fsimilar_1&otracker1=pp_reco_PINNED_productRecommendation%2Fsimilar_Similar%2BProducts_GRID_productCard_cc_2_NA_view-all&cid=PLSFYPSND9KUXP7B'

# Request the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the images (usually in <img> tags with a specific class)
images = soup.find_all('img', {'class': '_396cs4'})

# Loop through the images and download them
for idx, img in enumerate(images):
    img_url = img['src']  # Image URL
    download_image(img_url, f'grocery_item_{idx}')  # Download and save
    print(f"Downloaded: grocery_item_{idx}.jpg")

print("Image scraping completed!")
