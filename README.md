# Flipkart_Scrapper

App link: https://flipkart-comment-scrapper.herokuapp.com/

- App retrieves comments on various models of phones from Flipkart website. 
- App  be used through app interface(untill Nov-28th: heroku free tier) or an api.
- Only subset of data is displayed due to the server limits, the limitations can be removed from scraper file if needed and total data can be displayed.
- The application uses flask for api purpose and retrieves data from flipkart using requests library, the data is then formatted using bs4 library.

Project structure: </br>
.github/workflows/deployement.yaml - For deploying through github actions </br>
webapp/templates - Html pages  </br>
webapp/css/main.css - css design  </br>
Procfile - Needed for deployment to heroku  </br>
app.py - Application for handling api/form requests  </br>
fkart_scraper.py - Application for scrapping data from the flipkart website  </br>
requirements.txt - All the required libraries.
