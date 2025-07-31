-- working

The project tries to extract food from huge test based on catelog.

Steps:
1. Extract foods using catelog




-------- tech -----------
cd /Users/mayankarora/dib/poc/chatbot-book/food_bot_ingredients
rasa --help
rasa init
rasa interactive
rasa run actions
rasa train
rasa shell (always train before)
/stop
rasa run --endpoints endpoints.yml --debug
rasa shell --debug


-------- test ------------
1 cup White Peas,1 onion finely chopped,1 tomato finely chopped,1 tsp Ginger Garlic Paste,1 tsp Jeera Powder,1 tsp Dhania Powder,1/2 tsp Haldi Powder,Salt to taste,1 tsp Cumin Seeds,Oil for cooking and frying,2 boiled potatoes,3 – 4 chopped Green Chillies,1 tsp Roasted Jeera Powder,1/2 Red Chilly Powder,1 tsp Amchoor Powder,1 tsp Cornflour, , , , , , , , , , ","Soak white peas in water for about six hours .,Boil with haldi till done. Add salt, mash a little.,Take oil and add jeera. When it begins to sputter add the onion and ginger garlic paste and saute it for 2 minutes. Then add the tomato and continue to saute them for another 1 minute or so.,Add all the masalas and saute it for one more minute and then add the boiled peas into it. Cover and cook for some time till the peas have absorbed the flavours .,Boil potatoes, peel & mash them, add all the ingredients listed under the pattice ingredients.,To make the pattice, make small balls of the potato mix and then apply slight pressure to flatten it evenly.,Heat the Tava, put a little oil on it & fry pattice gently on both sides. Fry on medium heat. Keep aside.
