from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from django.core.management.base import BaseCommand
from products.models import products
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
url = 'https://www.zara.com/kz/en/man-jeans-slim-l675.html?v1=2205369' 

class Command(BaseCommand):
    def handle(self, *args, **options):
        help='scraping products as an example from the zara website'
        options=Options()
        options.add_argument('--headless')
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(service=Service( 
	ChromeDriverManager().install()), options=options) 
 
        driver.get(url)
        time.sleep(10)
        prices = driver.find_elements(By.CLASS_NAME, 'money-amount__main')  
        titles=driver.find_elements(By.TAG_NAME, "h3")
        pid=driver.find_elements(By.XPATH,"//*[@data-productid]")

        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)
        time.sleep(10)
        elements = driver.find_elements(By.XPATH, '//li[@class ="product-grid-block-carousel__secondary-products product-grid-block-carousel__secondary-products--fitting"]')

        # Extract the URLs of the pictures
        a=0
        for element in elements:
            picture_elements = element.find_elements(By.XPATH,  '//img[@class = "media-image__image media__wrapper--media"]')
        print(len(titles))
        common_length = min(len(pid), len(prices), len(titles))
        for amount in range(common_length):
            temp=pid[amount].get_attribute("data-productid")
            picture_url = picture_elements[amount].get_attribute('src')
            if(('transparent-background' in picture_url)==False and products.objects.filter(pid=temp,title=titles[amount].text).exists()==True):
                response = requests.get(picture_url)
                picture=os.path.join(r"media/images", f'image_{temp}.jpg')
                with open(picture, "wb") as file:
                    file.write(response.content)
                products.objects.filter(pid=temp).update(image=f'images/image_{temp}.jpg' )
            if(len(prices[amount].text)!=0 and len(titles[amount].text)!=0 and products.objects.filter(pid=temp,title=titles[amount].text).exists()==False):
                obj=products()
                obj.price=prices[amount].text
                obj.title=titles[amount].text
                obj.shop='zara'
                obj.pid=temp
                obj.category="jeans"
                if(('transparent-background' in picture_url)==False):
                    obj.image=f'images/image_{temp}.jpg'
                obj.save()
            else:
                a+=1
        print(a)
        driver.quit()
