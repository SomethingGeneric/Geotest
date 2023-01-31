from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

def try_find_addr(query):
  driver.get("https://google.com")

  box = driver.find_element(By.CLASS_NAME, 'gLFyf')
  box.send_keys(query + "\n")

  try:
    addr = driver.find_element(By.CLASS_NAME, 'LrzXr')
    return str(addr.text)
  except:
    return "FAIL"


df = pd.read_csv("data.csv")

enmpty = df[ (df['Address'].isnull()) ].index

c = 0

for index in enmpty:
  if c == 3:
    break
  print(f"Found empty: {str(df.loc[index, 'School:'])} at index {str(index)}")
  school = str(df.loc[index, 'School:'])
  state = str(df.loc[index, 'State:'])
  addr = try_find_addr(f"{school} {state}")
  if addr != "FAIL":
    df.loc[index, 'Address'] = addr
    print(f"Updated address for {school} in {state} to: '{addr}'")
  else:
    print(f"Couldn't get an address for {school} in {state}")
  c += 1

df.to_csv("data_save.csv", index=False)

print("Done.")
