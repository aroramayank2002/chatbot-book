-- not working as expected

The project tries to extract ingredients (food, spices, oil) and their quantities from the
huge text.

Steps:
1. Extract all ingredients
2. Slot filling or form filling, ask for their quantities and fill form.



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
I'm making a soup with carrots, celery, and onions.
