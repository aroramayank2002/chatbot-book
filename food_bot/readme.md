Agent reading the recipe and executing it.

-------- business ---------------

1. Identify Ingredients.
2. Identify quantity.
2. Group them into max 4 sets.
3. Separate the ones going to food boxes and other going to spice boxes.
4. Define the order.


-------- tech -----------
rasa --help
rasa init
rasa interactive 
rasa run actions
rasa train
rasa shell (always train before)
/stop

rasa data convert nlu --data data.json --out nlu.yml

------- messages -----------
Tell me how to make aalu gobi
I used 2 potatoes, 1 teaspoon of cumin, and 1/2 tsp of turmeric.
1 inch piece of ginger
I want to make 2 cups matar paneer
I want to make paneer bhurji
5 garlic cloves, finely chopped or crushed
1-inch or 1 tbsp ginger, finely chopped or crushed

Error:
        from packaging.version import LegacyVersion
        ImportError: cannot import name 'LegacyVersion' from 'packaging.version' (/Users/mayankarora/dib/poc/chatbot-book/.venv/lib/python3.9/site-packages/packaging/version.py)
    pip install --upgrade rasa


Though intents for training are put into nlu.yml. We can create a folder e.g. intents inside 
data folder and have multiple yml files for training. 

Note: Avoid () within [] in training data (nlu.yml) e.g. [ghee or butter (salted/unsalted both fine)](medium)