import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL της RemoteOK
URL = "https://remoteok.com/"

# Αποστολή HTTP request
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)

# Έλεγχος αν η σελίδα απάντησε σωστά
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Βρίσκουμε τα job postings
    job_listings = soup.find_all("tr", class_="job")

    jobs = []

    for job in job_listings:
        title = job.find("h2", class_="preventLink").text.strip() if job.find("h2", class_="preventLink") else "N/A"
        company = job.find("h3", class_="companyLink").text.strip() if job.find("h3", class_="companyLink") else "N/A"
        location = job.find("div", class_="location").text.strip() if job.find("div", class_="location") else "Remote"
        link = "https://remoteok.com" + job.find("a", class_="preventLink")["href"] if job.find("a",
                                                                                                class_="preventLink") else "N/A"

        jobs.append({"Title": title, "Company": company, "Location": location, "Link": link})

    # Αποθήκευση σε CSV
    df = pd.DataFrame(jobs)
    df.to_csv("remote_jobs.csv", index=False)

    print("✅ Scraping completed! Data saved to remote_jobs.csv")
else:
    print("❌ Failed to retrieve data from RemoteOK")
