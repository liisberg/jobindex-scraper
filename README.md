# jobindex-scraper
Change URL according to category you wish to scrape.

# requirements
`pip3 install -r requirements.txt`

# scrape
`python3 scrape.py`

All results will be stored in sqlite3:
`sqlite3 jobs.db`

```
sqlite> select company_name, count(*) from jobs group by company_name order by count(*) desc limit 10;
Grundfos A/S|12
Vestas Wind Systems A/S|7
Arla Foods|6
Kamstrup A/S|5
```
