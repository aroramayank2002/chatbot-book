-- working as expected

The project tries to extract ingredients (food, spices, oil) and their quantities from the
huge text.

Steps:
Hardcoded ingredients without quantity, asks for quantity to fill the slots.

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
start
