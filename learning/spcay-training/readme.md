visually creating training data to extract food from text.
https://www.teaforturmeric.com/matar-paneer/

----------- label studio -----------

pip install label-studio

label-studio --port 4012
aroramayank2002@gmail.com/asdqwe123!Q

https://www.youtube.com/watch?v=e1yJZUp0590&ab_channel=KarndeepSingh

Issue with labelling, trying out prodigy.

------------ prodigy -------------------

pip install prodigy-1.16.0-py3-none-any.whl
installation issues trying spacy

------------ streamlit ----------------

pip install spacy-streamlit
streamlit run TextAnalysisApp.py

Issue:
    pip uninstall streamlit
    pip install streamlit==1.36.0
    worked

it doesn't not allow adding custom entities without modifying the model

--------- doccano ----------------

pip install doccano
doccano init
    Error
        pip show marshmallow
        was > than 3.13
        pip uninstall marshmallow
        pip install marshmallow==3.13.0

    Role created successfully "project_admin"
    Role created successfully "annotator"
    Role created successfully "annotation_approver"

doccano createuser --username admin --password adminpassword --email admin@example.com
cd /Users/mayankarora/dib/poc/chatbot-book/learning/spcay-training
doccano webserver --port 4013
http://localhost:4013
doccano task

    error: AttributeError: type object 'CustomRESTRequestModel' has no attribute 'model_json_schema'
    fix:  pip install doccano --upgrade


