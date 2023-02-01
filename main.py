from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from fake_useragent import UserAgent

import pandas as pd

from time import sleep
import random
from sys import exit

useragent = UserAgent()


options = Options()
# options.set_preference("general.useragent.override", useragent.random)

driver = webdriver.Firefox(options=options)

def try_find_addr(query):
  driver.get("https://google.com")
  sleep(random.uniform(1.000012,5.0023))

  try:
    box = driver.find_element(By.XPATH, '/html/body/center/form/table/tbody/tr/td[2]/input[3]')
  except:
    box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

  box.send_keys(query)
  
  go = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]')
  go.click()

  try:
    addr = driver.find_element(By.CLASS_NAME, 'LrzXr')
    return str(addr.text)
  except:
    return "FAIL"


df = pd.read_csv("data.csv")

enmpty = df[ (df['Address'].isnull()) ].index

changed = 0
failed = 0

for index in enmpty:
  print(f"Found empty: {str(df.loc[index, 'School:'])} at index {str(index)}")
  school = str(df.loc[index, 'School:'])
  state = str(df.loc[index, 'State:'])
  addr = try_find_addr(f"{school} {state}")
  if addr != "FAIL":
    df.loc[index, 'Address'] = addr
    print(f"Updated address for {school} in {state} to: '{addr}'")
    df.to_csv("data.csv", index=False)
    changed += 1
  else:
    print(f"Couldn't get an address for {school} in {state}")
    failed += 1
  print(f"Status: Updated: {str(changed)}, Failed: {str(failed)}")

  if failed > 11:
    print("Lots of fails. Bot detection got us. Exiting.")
    exit(0)



df.to_csv("data.csv", index=False)

print("Done.")