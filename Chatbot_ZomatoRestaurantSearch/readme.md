
<img src="Chatbot.png" width="500"/>
**Problem Statement**
 - An Indian startup named 'Foodie' wants to build a conversational bot (chatbot) which can help users discover restaurants across several Indian cities. You have been hired as the lead data scientist for creating this product.
 - The main purpose of the bot is to help users discover restaurants quickly and efficiently and to provide a good restaurant discovery experience. The project brief provided to you is as follows.
 - The bot takes the following inputs from the user:<br>
   > 1.City: Take the input from the customer as a text field. <br><br>
   > 2.Cuisine Preference: Take the cuisine preference from the customer. The bot should list out the following six cuisine categories (Chinese, Mexican, Italian, American, South Indian & North Indian) and the customer can select any one out of that.<br><br>
   > 3.Average budget for two people: Segment the price range (average budget for two people) into three price categories: lesser than 300, 300 to 700 and more than 700. The bot should ask the user to select one of the three price categories.<br><br>

**Staregy**
- A sufficient number of relevant, varied training examples are created for intent and entity recognition and the model is able to generalise well on unseen (test) data.
- The NLU layer is able to correctly recognise common intents and entities (locations, cuisines, budget range and emails), including common synonyms of relevant cities, sufficiently varied ways of providing budget ranges, email addresses .

**Trigger Emails**
- An email is sent to the correct address with the results of the top-10 restaurants in decreasing order of average user ratings, only if the user asks to do so.
- Email is sent only based on users intention.

**Files Uploaded**
- `domain.yml` : Contains Training data for chatbot
- `action.txt` : Contains code required to connect with Zomato.csv file and filter the data based on the user selected options such as city,Cuisine and budget.
- `data`: Contains files like `Stories.yml` and `rules.yml`
