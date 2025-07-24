Chatbot from code in "BUILDING CHATBOTS" book.

To create a jupyter notebook -> new jupyter notebook.

To run the snippet
    ctrl + enter

stop words: high frequency words e.g. a,an,the.

---- rasa --------
npm install -g rasa-nlu-trainer
rasa-nlu-trainer
    automatically picked up file horoscope_bot/data/data.json

--- convert data.json to nlu.yml ----
rasa data convert nlu --data data/data.json --out data/nlu-data.yml --format yaml



pip install rasa --upgrade

 -- common commands --
 rasa init
 rasa train
 rasa shell
 rasa -h
 --debug
 rasa run actions (run in separate window)
/stop
rasa interactive 
rasa validate 
rasa data convert nlu --data data.json --out new_nlu.yml


rasa run --enable-api
    http://localhost:5005/version
        {
        "version": "3.6.21",
        "minimum_compatible_version": "3.6.21"
        }

# Using third party front end
rasa run --enable-api --cors="*"

There is a  react component for rasa chat.

-------- rasa x ----------
Steps:
    1. Create data sets, intents examples ( nlu.yml )
        Best way is to get responses from end users.
            Steps:
                Share your assistant with your users.
                Review conversations with regular basis.
                Annotate messages and use them as NLU training data.
                Test that assistant behaves normally.
                Track when your assistant fails and measaure its performance.
                Fix unsuccessful conversations and verify.
    2. Rasa X helps in all of above.
        pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
        pip install rasa-x -i https://pypi.rasa.com/simple
        > rasa x




