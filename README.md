# Webscraping

A personal side project to deepen understanding in the area of Natural Language Processing.

The first step is to build an evergrowing natural language corpus.
The end goal is to deploy the written code on a device that executes the code once a day and updates the corpus with new articles.
This way, one can have an evergrowing natural language corpus of news.

The project is still in its roots, so no clear structure and methods are figured out yet; it's much experimenting.


### Notes to myself:
- for Tagesschau: able to work with class names as they are consistent throughout the whole archive


### Tagesschau:
- Running this script will give you all articles saved in the Tagesschau archive.
- Depending on the selected timeframe this can take up to 48 hours
- to adapt the timespan modify the following attributes:
  - `url_2 = ?datum=<insert_start_date_here>` with format `year-month-day` e.g. `url_2 = '?datum=2022-01-01'`
  - `start_time_index = datetime.strptime('<insert_date_here>, '%d. %B %Y')` with format `day. month year` e.g. `start_time_index = datetime.strptime('1. Januar 2022', '%d. %B %Y')`
    (format is still only German, will be updated in the future)
  - `end_time_index = datetime.strptime('<insert_date_here>', '%d. %B %Y')` with same format as with `start_time_index`
  


### AP-News:
- class names are not consistent; the numbers change with each article, but use the 'data-key' attribute
- retrieval already working, file management has still bugs

### Die Zeit:
- subscription is needed to get access to premium articles, which would be vital if I want to scrape their archive
- focus more on other news pages before completing this one