from selenium import webdriver
import time
import random
import array
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def log(data):
  file = open("log.txt", "a")  # append mode
  file.write(data+"\n")
  file.close()

def random_line(fname):
  lines = open(fname).read().splitlines()
  return random.choice(lines)

log("Initiating..")

Driver = webdriver.Chrome(executable_path=r"F:\software\chromedriver_win32\chromedriver.exe")  

def checkElementbyName(name):
  try:
    Driver.find_element_by_name(name)
  except NoSuchElementException:
    return False
  return True

def checkElementbyClassName(name):
  try:
    Driver.find_element_by_class_name(name)
  except NoSuchElementException:
    return False
  return True

def checkElementbyXpath(path):
  try:
    Driver.find_element_by_xpath(path)
  except NoSuchElementException:
    return False
  return True

def generatePassword():
  MAX_LEN = 12
  DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
  LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                      'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                      'z']
    
  UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                      'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                      'Z']
    
  SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
            '*', '(', ')', '<']
  COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
  rand_digit = random.choice(DIGITS)
  rand_upper = random.choice(UPCASE_CHARACTERS)
  rand_lower = random.choice(LOCASE_CHARACTERS)
  rand_symbol = random.choice(SYMBOLS)
  
  temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

  for x in range(MAX_LEN - 4):
    temp_pass = temp_pass + random.choice(COMBINED_LIST)
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)
    
  password = ""
  for x in temp_pass_list:
    password = password + x
  
  return password
          


tempMail = "https://temp-mail.org/"
twitterSignUp = "https://twitter.com/i/flow/signup"

log("Getting tempMail")
Driver.get(tempMail)

DeleteBtn = Driver.find_element_by_id("click-to-delete")

def getActiveEmail():
  return Driver.execute_script('''
  return document.getElementsByClassName('emailbox-input opentip')[0].value
  ''')

previousEmail = getActiveEmail()
log("previous email : "+previousEmail)
log("clicking delete button")
DeleteBtn.click()
DeleteBtn.click()
log("Delete button clicked")

log("launching loop")
while (getActiveEmail() == "Loading" or getActiveEmail() == "Loading." or getActiveEmail() == "Loading.." or getActiveEmail() == "Loading..." or getActiveEmail() == previousEmail or getActiveEmail() == "" or getActiveEmail() == "Loading"):
  log("in while loop: "+ getActiveEmail())
  time.sleep(0.5)

getActiveEmail()

newEmail = getActiveEmail()
log("new email id detected : "+newEmail)

log("executing script to open new tab")
Driver.execute_script("window.open('about:blank','secondtab');")
Driver.switch_to.window("secondtab")
Driver.get(twitterSignUp) 

generatedName = random_line("firstNames.txt")+" "+random_line("lastNames.txt")
log(generatedName+" has been generated")

while(checkElementbyName('name') == False):
  time.sleep(0.5)

log("twitter sign up loaded")

nameTxtbx = Driver.find_element_by_name("name")
useEmailBtn = Driver.find_element_by_xpath("//div[@role='button']")
monthSelect = Select(Driver.find_element_by_id('SELECTOR_1'))
dateSelect = Select(Driver.find_element_by_id('SELECTOR_2'))
yearSelect = Select(Driver.find_element_by_id('SELECTOR_3'))
nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")


log("trying to type in credentials")
nameTxtbx.send_keys(generatedName)
useEmailBtn.click()
emailTxtbx = Driver.find_element_by_name("email")
emailTxtbx.send_keys(newEmail)

monthSelect.select_by_index(random.randint(1,11))
dateSelect.select_by_index(random.randint(1,27))
yearSelect.select_by_index(random.randint(20,50))

log("credentials typed")
log("clicking the next button ")
nextBtn.click()

while(checkElementbyName('name') == True):
  time.sleep(0.2)
  nextBtn.click()

nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
nextBtn.click()
signUpBtn = Driver.find_element_by_xpath("//span[contains(text(),'Sign up')]")
signUpBtn.click()

log("switching tabs")
Driver.switch_to.window(Driver.window_handles[0])
log("tabs switched")

RefreshBtn = Driver.find_element_by_id("click-to-refresh")
RefreshBtn.click()
xpathOTP = "html/body/main/div/div/div[2]/div[2]/div/div/div/div[4]/ul/li[2]/div/a/span[4]"
while(checkElementbyXpath(xpathOTP) == False):
  time.sleep(0.5)
OTP = Driver.execute_script('''
let otp = document.getElementsByClassName('inboxSubject small subject-title d-none visable-xs-sm')[1].textContent;
return otp[0]+otp[1]+otp[2]+otp[3]+otp[4]+otp[5];
''')

log(OTP)

log("switching tabs")
Driver.switch_to.window(Driver.window_handles[1])
log("tabs switched")

log("enterig otp")
otpTxtbx = Driver.find_element_by_name('verfication_code')
otpTxtbx.send_keys(OTP)

nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
nextBtn.click()

while(checkElementbyName('password') == False):
  time.sleep(0.2)

log("entering password")
Driver.execute_script('''
document.getElementsByName('password')[0].setAttribute('type','text')
''')
passTxtbx = Driver.find_element_by_name('password')
generatedPassword = generatePassword()
log("generated password is : "+generatedPassword)
passTxtbx.send_keys(generatedPassword)

nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
while(checkElementbyName('password') == True):
  time.sleep(0.2)
  nextBtn.click()

time.sleep(5)
log('skipping profile photo updation')

Driver.execute_script('''
    document.getElementsByClassName('css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')[5].click();
  ''')

log('skipping bio updation')
while(checkElementbyXpath("//textarea[@name='text']") == False):
  time.sleep(0.2)
Driver.find_element_by_xpath("//textarea[@name='text']").send_keys("You know who I am.")

nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
nextBtn.click()

log("selecting language")
while(checkElementbyXpath("//input[@type='checkbox']") == False):
  time.sleep(0.2)

Driver.find_element_by_xpath("//span[contains(text(),'English')]").click()
nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
nextBtn.click()
while(checkElementbyXpath("//span[contains(text(),'English')") == True):
  time.sleep(0.2)
  nextBtn.click()

log("skipping interests")
while(checkElementbyXpath("//span[contains(text(),'What are you interested in?')]") == False):
  time.sleep(0.2)
nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
nextBtn.click()
while(checkElementbyXpath("//span[contains(text(),'What are you interested in?')") == True):
  time.sleep(0.2)
  nextBtn.click()

log("clicking next..")
nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
while(checkElementbyXpath("//span[contains(text(),'Next')]") == False):
  time.sleep(0.2)
nextBtn.click()

log("clicking next..")
nextBtn = Driver.find_element_by_xpath("//span[contains(text(),'Next')]")
while(checkElementbyXpath("//span[contains(text(),'Next')]") == False):
  time.sleep(0.2)
nextBtn.click()

log("skkipping following..")
time.sleep(3)
Driver.execute_script('''
    document.getElementsByClassName('css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')[5].click();
  ''')

profile = "https://twitter.com/_pratikpakhale"
Driver.get(profile)

followBtn = Driver.find_element_by_xpath("//span[contains(text(),'Follow')]")
followBtn.click()
