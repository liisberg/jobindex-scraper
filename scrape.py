import requests
from bs4 import BeautifulSoup
import sqlite3

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Accept-Encoding": "utf-8",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
}


def create_table(conn):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS jobs")
    c.execute("CREATE TABLE jobs (title text NOT NULL, link text NOT NULL, company_id int NOT NULL, company_name text NOT NULL, published date NOT NULL, source text NOT NULL)")
    conn.commit()


def jobs(conn, url):
    print("Scraping {}".format(url))
    c = conn.cursor()
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find_all("div", class_="PaidJob")
    for res in results:
        links = res.find_all("a")
        title = links[1].getText()
        link = links[1].get("href")
        company_id = res.find("li", class_="toolbar-companyprofile")
        if company_id:
            company_id = company_id.find("a").get("href").split("/")[2]
        company_name = links[2].getText()
        published = res.find("time").get("datetime")

        c.execute("INSERT INTO jobs (title, link, company_id, company_name, published, source) VALUES (?, ?, ?, ?, ?, ?)", (title, link, company_id or 0, company_name, published, url))

    next_url = soup.find("li", class_="page-item page-item-next")
    if next_url:
        next_url = next_url.find("a").get("href")
        jobs(conn, next_url)

    conn.commit()

if __name__ == "__main__":
    URL = "https://www.jobindex.dk/jobsoegning/it/systemudvikling/danmark"
    try:
        conn = sqlite3.connect("jobs.db")
        create_table(conn)
        jobs(conn, URL)
        print("Done scraping jobs!")
    except Exception as err:
        print("Error storing jobs.")
    finally:
        conn.close()



