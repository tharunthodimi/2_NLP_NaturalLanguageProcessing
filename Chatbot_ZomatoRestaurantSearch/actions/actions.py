# This files contains custom actions which can be used to run

# Import Required libraries
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import pandas as pd
import json


# Read the zomato csv file and remove the duplicates
ZomatoData = pd.read_csv('zomato.csv')
ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
# List of places where business is operated
WeOperate = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi', 'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun', 'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore', 'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa', 'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']


# below function looks for valid location where business is operated
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_locationsearch'
    
	def run(self, dispatcher, tracker, domain):
		WeOperate = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi', 'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun', 'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore', 'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa', 'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']
		WeOperate = [i.lower() for i in WeOperate]
		loc = tracker.get_slot('location')
		operated_inlocation = True
		if (loc in WeOperate):
			pass
		else :
			operated_inlocation = False
		return [SlotSet('operated_inlocation',operated_inlocation)]

    
# Below function looks for valid cuisines and slots are set for the same
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_cuisinesearch'
    
	def run(self, dispatcher, tracker, domain):
		Cuisinesavailable = ['Chinese','Mexican','American','Italian','North Indian','South Indian']
		Cuisinesavailable = [i.lower() for i in Cuisinesavailable]
		cuisine = tracker.get_slot('cuisine')
		cuisine = cuisine.lower()
		cuisine_isavailable = True
		if (cuisine in Cuisinesavailable):
			pass
		else :
			cuisine_isavailable = False
		return [SlotSet('cuisine_isavailable',cuisine_isavailable)]
    
# Below method is used to get the restuarants list satisfying the users serach and returns a dataframe
# Method returns 299 if teh payloda contains <300
# Method returns 699 indicating payload value 300-700
# Method return 800 indicating payload value with more than 700
def RestaurantSearch(City,Cuisine,budget):
	TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: Cuisine.lower() in x.lower())) & (ZomatoData['City'].apply(lambda x: City.lower() in x.lower()))]
	TEMP2 = TEMP.copy()
	TEMP2['budget'] = TEMP2['Average Cost for two']
	def price_range(x): 
		if x<300:
			return 299
		elif(x>=300 and x<=700):
			return 699
		else:
			return 800
	TEMP2['budget'] = TEMP2['budget'].apply(price_range)
	TEMP3 = TEMP2[TEMP2['budget']==budget].sort_values(['Aggregate rating','Average Cost for two'],ascending=False)
	return TEMP3[['Restaurant Name','Address','Average Cost for two','Aggregate rating']]


#Below method is used for decrypting the payload taken for budget range
# payload value <30 indicates prices with less than 300, 300-700 means less than 700
# payload value >=700 is considered with some dummy value 800 because any value with >700 is considered as 800 which indicates >700 value this value can be anyting
def BudgetDecryption(x): 
		if (x == '<300'):
			return 299
		elif(x == '300-700'):
			return 699
		else:
			return 800
    

# Following function is used to search for restaurants with the user provided location,budget and cuisine
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'
    
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')  #budget is taken from payload
		budget = BudgetDecryption(budget)   # convert payload of budget to numerical
		results = RestaurantSearch(City=loc,Cuisine=cuisine,budget=budget)
		restaurantslocated = True
		response=""
		if results.shape[0] < 5:
			response= "Couldn't Find any restaurants with your preferred location,cuisne and budget.Try again with some other budget available range."
			restaurantslocated = False
		else:
			for restaurant in RestaurantSearch(loc,cuisine,budget).iloc[:5].iterrows():
				restaurant = restaurant[1]
				response=response + F"{restaurant['Restaurant Name']} in {restaurant['Address']} has been rated {restaurant['Aggregate rating']} \n\n"
		dispatcher.utter_message("-----"+response)
		return [SlotSet('location',loc),SlotSet('restaurantslocated',restaurantslocated)]


# Send email for the list of 10 restaurants when user wish to have the details on mail
class ActionSendEmail(Action):
	def name(self):
		return 'action_send_email'

	def run(self, dispatcher, tracker, domain):
		import smtplib 
		loc = tracker.get_slot('location') 
		cuisine=tracker.get_slot('cuisine') 
		budget=tracker.get_slot('budget')     #budget is takend from payloas
		budget = BudgetDecryption(budget) # budget is decrypted to numerical values

		askmailid=tracker.get_slot('askmailid') 
		results= RestaurantSearch(City=loc, Cuisine=cuisine,budget=budget)
		response="" 
		if results.shape[0] < 5:
			response= "Couldn't Find any restaurants with your preferred location,cuisne and budget.Try again with some other budget available range."
		else:
			for restaurant in RestaurantSearch(loc,cuisine,budget).iloc[:10].iterrows():
				restaurant = restaurant[1]
				response=response + F"{restaurant['Restaurant Name']} is loacted at {restaurant['Address']} and  has been rated {restaurant['Aggregate rating']} with avg cost {restaurant['Average Cost for two']} \n\n"
		s = smtplib.SMTP('smtp.gmail.com', 587)  #port number 587
		s.starttls() 
		s.login("tharuntejreddy112@gmail.com", "password")  #password should be replaced with email password
		message = "Please find the Top 10 Restaurants with your prederred search in Foodie chatbot\n \n"  
		subject="Foodie: Here are the list of Restaurants you might be interested in"
		message = message + response
		message = 'Subject: {} \n\n{}'.format(subject,message)
		try:
			s.sendmail("tharuntejreddy112@gmail.com",askmailid,message)
			dispatcher.utter_message("Email sent")
			s.quit()
		except:
		  dispatcher.utter_message("Couldn't send mail.Try again later")
		  return [AllSlotsReset()]
      
# Following method is used to restart the action
class ActionRestartConversation(Action):
	def name(self):
		return 'action_torestart'

	def run(self, dispatcher, tracker, domain):
		return [Restarted()]		
		