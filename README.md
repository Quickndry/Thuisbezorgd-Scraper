
# Thuisbezorgd Scraper

This is a Scrapy spider for scraping restaurant and menu information from the website thuisbezorgd.nl.

## Setup

### Installation
    1. Clone this repository to your local machine.
    2. Navigate to the root of the repository.
    3. Run the command pip install -r requirements.txt to install the necessary dependencies.

### Usage
    1. cd Thuizbezongd
    2. python run.py
    3. Select a province in the Netherlands from the list presented (default is Noord-Holland).
    
    The script will start scraping data from the website.

Note: The script uses the GenSpider class from Thuizbezongd.gen_spider module and PROVINCES constant to provide a list of provinces in the Netherlands to select from.

### Legal and Ethical considerations
Please be aware that this spider is scraping a website that is not open for scraping. It is important to check the terms of service of any website before scraping it. It is also important to respect the website's rate limits and not to scrape too aggressively.
Disclaimer
This spider is for educational and research purposes only. The creators of this spider are not responsible for any misuse or damage caused by this software. Use at your own risk.


### Contact
If you have any questions or feedback, please reach out to me at ncpasik@gmail.com

## Code

### Introduction

When scraping the website thuisbezorgd.nl, I discovered that the site utilizes Ajax requests to retrieve data. Instead of using traditional web scraping methods such as Selenium or Splash in combination with Scrapy, I decided to scrape the API directly.

For restaurants, the API call is in the following format:
```
get https://cw-api.takeaway.com/api/v33/restaurants?deliveryAreaId={}&postalCode={}&lat={}lng={}&limit=0&isAccurate=true '

```
It's worth noting that the API returns the same results whether you use the postalCode or deliveryAreaId parameter.

For menus, the API call is in the following format:

For menus: 
```
get https://cw-api.takeaway.com/api/v33/restaurant?slug={}
```

The "slug" parameter is returned as a response from a restaurant API call.

### Creating a table for postcodes

To aid in this scraping process, I also created a table for postcodes using data from the CBS (Central Bureau of Statistics) in the Netherlands. I downloaded a CSV file that contains all postcodes (pc4) for each province and used the Python script create_table_ps4.py to create the table. The script opens the CSV file, creates a CSV reader object, and uses a SQL INSERT statement to insert the data into the table. The script skips the first row, which contains the header information.
```python
  create_table_ps4.py
```

```python
# Open the CSV file
with open("Netherlands-postcode-pc4.csv") as a file:
    # Create a CSV reader object
    reader = CSV.reader(file)
    # Skip the first row (header)
    next(reader)
    # Iterate over the rows
    for row in reader:
        # Insert the data into the table
        cursor.execute("INSERT INTO netherlands_pc4 (X, Y, PC_4, Year, Gemeente_code, Provincie_code, Provincie_name, Gemeente_name) VALUES (?,?,?,?,?,?,?,?)", row)
```


### Thuisbezongd Scraper
This script is a Scrapy spider that is used to scrape restaurant data from the website thuisbezorgd.nl. The spider uses the requests and scrapy libraries to make GET requests to the website's API, using specific headers and a proxy to access the data.

The spider is initialized with several parameters, including a link to the API endpoint(links which generated using postalCodes), a minimum sleep duration between requests, a proxy and a number of attempts. These parameters can be set to customize the spider's behavior.

The spider uses the link parameter to make GET requests to the API endpoint, passing the headers and the proxy as well as a callback function to handle the response. With the min_sleep_duration parameter you can set a minimum sleep duration between requests, to prevent being blocked by the website. The use_proxy parameter determines if the spider should use a proxy or not, and the number_of_attempts parameter determines how many times the spider should retry a request in case of failure.

### RestaurantPipeline

This is a pipeline for the Scrapy spider that is used to store the scraped data in a sqlite3 database. The pipeline is designed to handle the data storage process for the spider, making it easy to store and retrieve the scraped data.

The pipeline includes several methods to handle the data storage process. The create_connection method is used to create a connection to the sqlite3 database, and the create_table method is used to create two tables in the database: "restaurants" and "menus".

The process_item method is used to determine whether the item passed to the pipeline is an instance of the RestaurantItem class or the MenuItem class. If the item is an instance of the RestaurantItem class, the store_restaurant method is called to store the data in the "restaurants" table. If the item is an instance of the MenuItem class, the store_menu method is called to store the data in the "menus" table.

The store_restaurant method takes the item as an input and insert the data into the 'restaurants' table in the sqlite3 database. The store_menu method takes the item as an input and insert the data into the 'menus' table in the sqlite3 database.

### GenSpider

To use the GenSpider class, you need to import it and create an instance of it by passing in a region. The region parameter is optional and defaults to "Noord-Holland" if not provided.

```
GenSpider("province")
```

The get_links() (in utils.py) function is used to retrieve api links based on the provided region.

```
curr.execute("""SELECT PC_4 FROM netherlands_pc4 WHERE Provincie_name = ? COLLATE NOCASE""", (province_name,))
```  


Once the links are obtained, the spider will start generating for each link. The spider generation process is done using the generate_spider() function, which takes a single link as a parameter. The function sets up the Scrapy settings using crawler_settings and starts the spider using the CrawlerProcess class.

After the spider is generated, the script will wait before generating the next spider.


### run.py
The user can choose from the list of provinces provided in the PROVINCES variable. The script will prompt the user to select a province from the list, and will return the selected province. If the user does not provide any input, the script will return the default province, which is set to Noord-Holland.

The script also includes a spider configuration section, where the user can customize the the Spider by setting the sleep duration, whether to use a proxy or not, the proxy url and number of attempts. 
## Concurrent Approaches

### TaskQueue

This code utilizes multiple concurrent approaches to scrape data from the thuisbezorgd.nl  website. The code uses a combination of multiprocessing, sqlite3, threading, and the concurrent.futures library to run multiple instances of the ThuizSpider spider concurrently.
The TaskQueue class is used to manage the tasks (in this case, links) that are passed to the spider. The num_workers attribute is set to the number of CPU cores on the system to maximize performance. The executor attribute is a thread pool executor that is used to run the spider concurrently.
The run() method is used to start the concurrent execution of the spider by submitting the tasks to the executor. The stop() method is used to stop the execution of the spider. The generate_spider() method is used to start the spider using the CrawlerProcess class from the scrapy library.
It's failed because it increased the request load on the website. It's currently not a part of the pipeline but I wanted to put it anyway.


### Database Overview
![alt text](https://github.com/Astosi/Thuisbezorgd-Scraper/blob/main/test_imgs/thuiznezongd_db.png?raw=true)

### Netherlands Postcodes Table
![alt text](https://github.com/Astosi/Thuisbezorgd-Scraper/blob/main/test_imgs/netherlands_postcodes.png?raw=true)

### Restaurants Table
![alt text](https://github.com/Astosi/Thuisbezorgd-Scraper/blob/main/test_imgs/restourants.png?raw=true)

### Menus Table
![alt text](https://github.com/Astosi/Thuisbezorgd-Scraper/blob/main/test_imgs/items.png?raw=true)






