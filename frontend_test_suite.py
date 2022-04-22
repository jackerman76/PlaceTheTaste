import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestDefaultSuite():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()

    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_bACKTOMAP(self):
    # Test name: BACK-TO-MAP
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://742c-71-116-60-111.ngrok.io/")
    # 2 | setWindowSize | 948x600 | 
    self.driver.set_window_size(948, 600)
    # 3 | click | css=#gmimap11 > area | 
    self.driver.find_element(By.CSS_SELECTOR, "#gmimap11 > area").click()
    # 4 | click | css=.py-5 | 
    self.driver.find_element(By.CSS_SELECTOR, ".py-5").click()
    # 5 | click | id=map_rate_this_recipe | 
    self.driver.find_element(By.ID, "map_rate_this_recipe").click()
    # 6 | click | id=view_recipe_back_to_map | 
    self.driver.find_element(By.ID, "view_recipe_back_to_map").click()
    # 7 | assertElementPresent | id=filter-recipe-text | Filter Recipes
    elements = self.driver.find_elements(By.ID, "filter-recipe-text")
    assert len(elements) > 0
  
  def test_cLICKMARKER(self):
    # Test name: CLICK-MARKER
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://742c-71-116-60-111.ngrok.io/")
    # 2 | setWindowSize | 951x604 | 
    self.driver.set_window_size(951, 604)
    # 3 | click | css=#gmimap14 > area | 
    self.driver.find_element(By.CSS_SELECTOR, "#gmimap14 > area").click()
    # 4 | click | id=leave-a-comment | 
    self.driver.find_element(By.ID, "leave-a-comment").click()
    # 5 | assertElementPresent | name=submit_comment | 
    elements = self.driver.find_elements(By.NAME, "submit_comment")
    assert len(elements) > 0
  
  def test_fILTERSELECTION(self):
    # Test name: FILTER-SELECTION
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://742c-71-116-60-111.ngrok.io/")
    # 2 | setWindowSize | 948x601 | 
    self.driver.set_window_size(948, 601)
    # 3 | click | css=.ks-cboxtags > li:nth-child(1) > label | 
    self.driver.find_element(By.CSS_SELECTOR, ".ks-cboxtags > li:nth-child(1) > label").click()
    # 4 | assertChecked | id=checkbox1 | 
    assert self.driver.find_element(By.ID, "checkbox1").is_selected() is True
    # 5 | click | css=.ks-cboxtags > li:nth-child(5) > label | 
    self.driver.find_element(By.CSS_SELECTOR, ".ks-cboxtags > li:nth-child(5) > label").click()
    # 6 | assertChecked | id=checkbox5 | 
    assert self.driver.find_element(By.ID, "checkbox5").is_selected() is True
    # 7 | click | name=filter_recipe | 
    self.driver.find_element(By.NAME, "filter_recipe").click()
  
  def test_fILTERTONEW(self):
    # Test name: FILTER-TO-NEW
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://742c-71-116-60-111.ngrok.io/")
    # 2 | setWindowSize | 1552x840 | 
    self.driver.set_window_size(1552, 840)
    # 3 | click | css=.ks-cboxtags > li:nth-child(1) > label | 
    self.driver.find_element(By.CSS_SELECTOR, ".ks-cboxtags > li:nth-child(1) > label").click()
    # 4 | click | css=li:nth-child(7) > label | 
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(7) > label").click()
    # 5 | click | name=filter_recipe | 
    self.driver.find_element(By.NAME, "filter_recipe").click()
    # 6 | click | css=#gmimap2 > area | 
    self.driver.find_element(By.CSS_SELECTOR, "#gmimap2 > area").click()
    # 7 | assertText | id=recipe_name | Greek Einkorn (Wheat Berry) Salad
    assert self.driver.find_element(By.ID, "recipe_name").text == "Greek Einkorn (Wheat Berry) Salad"
  
  def test_rATERECIPELOGIN(self):
    # Test name: RATE-RECIPE-LOGIN
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("https://742c-71-116-60-111.ngrok.io/")
    # 2 | setWindowSize | 946x601 | 
    self.driver.set_window_size(946, 601)
    # 3 | click | css=#gmimap14 > area | 
    self.driver.find_element(By.CSS_SELECTOR, "#gmimap14 > area").click()
    # 4 | click | id=leave-a-comment | 
    self.driver.find_element(By.ID, "leave-a-comment").click()
    # 5 | click | id=label_rating3 | 
    self.driver.find_element(By.ID, "label_rating3").click()
    # 6 | click | id=submit_recipe_rating | 
    self.driver.find_element(By.ID, "submit_recipe_rating").click()
    # 7 | assertText | css=h1 | Login
    assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Login"
  
