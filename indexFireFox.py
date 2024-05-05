import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do WebDriver para Firefox
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0")
options.add_argument("--width=920")
options.add_argument("--height=680")

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 20)

try:
    all_products_details = {}
    total_pages = 2  # Total de páginas conhecidas

    for current_page in range(1, total_pages + 1):
        print(f"Accessing page {current_page} of {total_pages}...")
        driver.get(f"https://spacesportsfut.com.br/collections/futsal?page={current_page}")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.product-item__info-inner")))
        
        products = driver.find_elements(By.CSS_SELECTOR, 'a.product-item__title')
        product_links = [product.get_attribute('href') for product in products if product.get_attribute('href')]

        print(f"Found {len(product_links)} products on page {current_page}. Extracting details...")

        for link in product_links:
            driver.get(link)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.product-meta__title')))
            product_title = driver.find_element(By.CSS_SELECTOR, 'h1.product-meta__title').text
            
            description_container = driver.find_element(By.CSS_SELECTOR, 'div.rte.text--pull')
        
            # Check for images in the description
            description_images = description_container.find_elements(By.TAG_NAME, 'img')
            description_img_urls = [img.get_attribute('src') for img in description_images]

            # Extract text description if no images
            description_text = ""
            if not description_img_urls:
                description_text = description_container.get_attribute('innerHTML')   # This will get all the text within the container

            price = '109,90'

            size_variations = []
            size_options = driver.find_elements(By.CSS_SELECTOR, "label.block-swatch__item")
            for option in size_options[:6]:
                size_text = option.find_element(By.CSS_SELECTOR, "span.block-swatch__item-text").text
                size_variations.append(size_text)

            images = driver.find_elements(By.CSS_SELECTOR, 'img.product-gallery__image')
            image_urls = [img.get_attribute('data-zoom') for img in images if img.get_attribute('data-zoom')]

            print(f"Extracted details for {product_title}.")
            all_products_details[product_title] = {
                'title': product_title,
                'price': price,
                'sizes': size_variations,
                'description_images': description_img_urls,
                'description_text': description_text,
                'imagens': image_urls
            }

finally:
    driver.quit()
    # Salvando os detalhes em um arquivo JSON
    with open('product_details.json', 'w', encoding='utf-8') as f:
        json.dump(all_products_details, f, indent=4, ensure_ascii=False)
    print("Product details saved in 'product_details.json'")
    print("All pages processed.")
