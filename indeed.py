from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from fake_useragent import UserAgent

import random
import time
from pandas import DataFrame as df

ua = UserAgent()
user_agent = ua.random
# proxies=[]
# proxy = random.choice(proxies)

opt = Options()
# opt.add_argument("start-maximized")
# opt.add_argument("--incognito")
# opt.add_argument("--headless")
opt.add_argument(f"user-agent={user_agent}")
# opt.add_argument(f"--proxy-server={proxy}")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=opt)

web = "https://in.indeed.com"
keyword = "Python Developer"
location = "Chennai"
job_list = []

driver.get(web)

job_keyword = driver.find_element(By.ID,"text-input-what")
job_location = driver.find_element(By.ID,"text-input-where")

job_keyword.send_keys(keyword)
job_location.send_keys(location)

find_job = driver.find_element(By.CLASS_NAME,"yosegi-InlineWhatWhere-primaryButton").click()

def indeed_jobs():

    containers = driver.find_elements("xpath","//div[@id='mosaic-provider-jobcards']/ul/li")

    for container in containers:

        try:

            job_content = container.find_element("xpath",".//table[contains(@class,'jobCard_mainContent')]/tbody/tr")
            job_title = job_content.find_element("xpath",".//td[contains(@class,'resultContent')]/div/h2/a/span").text

            # company_name = container.find_element(By.XPATH,".//table[contains(@class,'jobCard_mainContent')]/tbody/tr/td/div[2]/span").text
            company_name = container.find_element("xpath",".//span[@class='companyName']").text

            company_loctaion = container.find_element("xpath",".//div[@class='companyLocation']").text

            job_href = job_content.find_element("xpath",".//td[contains(@class,'resultContent')]/div/h2/a")
            job_link = job_href.get_attribute("href")

        except:
            continue

        try:
            job_snippet_list = []
            job_snippets = container.find_elements("xpath",".//div[@class='job-snippet']/ul/li")
            for job_snippet in job_snippets:
                job_snippet_list.append(job_snippet.text)
        except:
            job_snippets = "-"
            job_snippet_list.append(job_snippets)

        try:
            posted_list = []
            posted_date = container.find_element("xpath",".//span[@class='date']").text
            posted_list.append(posted_date)
        except:
            pass


        try:
            salary = container.find_element("xpath",".//div[contains(@class,'salaryOnly')]/div/div").text
        except:
            salary = "Not Issued"
            pass

        job_detail = {
                    "Job_Title":job_title,
                    "Company_Name":company_name,
                    "Company_Location":company_loctaion,
                    "Job_Snippets":job_snippet_list,
                    "Job_Posted_Date":posted_list,
                    "Salary_Details":salary,
                    "Job_Pagelink":job_link,
                    }
        job_list.append(job_detail)

    time.sleep(10)

for i in range(0,3):
    try:
        indeed_jobs()
        next_page = driver.find_elements("xpath",".//div[@class='pagination']/ul/li/a")[-1].click()
        time.sleep(5)
        try:
            # pop_box = driver.find_element("xpath","//div[@id='popover-foreground']/div/button").click()
            pop_box = WebDriverWait(driver,10).until(EC.element_to_be_clickable(("xpath","//div[@id='popover-foreground']/div/button"))).click()
        except Exception as e:
            pass
    except:
        break

driver.quit()

data = df(job_list)
data.to_json("Indeed_jobs.json")
# data.to_csv("Indeedjobs.csv",index=False,encoding="utf-8")




