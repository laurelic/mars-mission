def scrape:
""" scrapes data and images about Mars from several websites via BeautifulSoup """

    #import dependencies
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import requests
    from splinter import Browser

    #initiate splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #scrape NASA Mars News
    #set the url to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'

    #visit the site via splinter
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'lxml')

    #get the most recent news tile
    nasa_title = nasa_soup.find('div', class_='content_title').text

    #get the teaser associated with that title
    nasa_teaser = nasa_soup.find('div', class_='article_teaser_body').text

    #scrape JPL Mars Space Images for Featured Image
    #set the url to be scaped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #visit the site via splinter
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'lxml')

    #retrieve the featured image
    featured_image = jpl_soup.find('a', class_='button fancybox')
    jpl_pic_page = 'https://www.jpl.nasa.gov' + featured_image['data-link']
    browser.visit(jpl_pic_page)
    jpl_pic_page_html = browser.html
    jpl_pic_soup = bs(jpl_pic_page_html, 'lxml')
    jpl_pic_url = 'https://www.jpl.nasa.gov' + jpl_pic_soup.find('figure', class_='lede').find('a')['href']

    #scrape the Mars Weather Twitter page
    #set the url to be scraped
    weather_url = "https://twitter.com/marswxreport?lang=en"

    #call the page
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, 'lxml')

    #retrieve the first tweet for latest weather update
    mars_weather = weather_soup.find('div', class_='js-tweet-text-container').find('p').text

    #scrape Mars Facts
    #set the url to be scraped
    facts_url = 'http://space-facts.com/mars/'

    #scrape the table from the site
    facts_table = pd.read_html(facts_url)

    #convert the scrape into a DataFrame
    facts_df = facts_table[0]
    facts_df.columns = ['Feature', 'Stat']

    #convert the dataframe to html
    html_facts = facts_df.to_html()
    html_facts = html_facts.replace('\n', '')

    #scrape USGS photos of hemispheres
    #set the url to be scraped
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #create beautiful soup element
    usgs_response = requests.get(usgs_url)
    usgs_soup = bs(usgs_response.text, 'lxml')

    #initiate an empty list to store dictionaries or urls and titles
    hemispheres = []

    #scape all hemispheres and store in dictionaries
    hemisphere_scrape = usgs_soup.find_all('div', class_='item')

    for hemisphere in hemisphere_scrape:
        #find the link to the hemiphere's page
        h_page = hemisphere.find('a', class_='itemLink product-item')['href']
        hemisphere_url = 'https://astrogeology.usgs.gov' + h_page
        
        #create a beautiful soup object of the page
        hemisphere_response = requests.get(hemisphere_url)
        hemisphere_soup = bs(hemisphere_response.text, 'lxml')
        
        #find the image url
        hemisphere_pic_url = hemisphere_soup.find('div', class_='downloads').find('a')['href']
        
        #find the hemisphere name
        hemisphere_name = hemisphere_soup.find('h2').text.replace(' Enhanced', '')
        
        #store the image url and hemisphere name in the hemisphere list
        hemisphere = {'title': hemisphere_name, 'img_url': hemisphere_pic_url}
        hemispheres.append(hemisphere)

    scrape_results = {'nasa_title': nasa_title, 'nasa_teaser': nasa_teaser, 'jpl_pic_url': jpl_pic_url, 'mars_weather': mars_weather, 'html_facts': html_facts, 'hemispheres' = hemispheres}

    return scrape_results

