import os
import openai
import panel as pn  # GUI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to assist people on a college website name="shri ramdeobaba college of engineering and management" \
You first greet the customer, then ask them what help they need, \
You wait to collect the details, then summarize it and check for a final \
time if the person wants to know anything more. \
You respond in a short, very conversational friendly style. \
You have Answer questions on the basis of given information only \
otherwise applogies and ask to check on website or contact the office \
The college details includes \
General Information:
College name=shri ramdeobaba college of engineering and management and location=Nagpur.
Contact information phone=(91)-(712)-2580011 email=rcoem@rknec.edu
Operating hours and availability 9AM to 9PM.

Admissions Information:
Application deadlines=check that on menu/admissions
Application process and steps.
Information on different programs and majors.
Tuition and fees.
Scholarships and financial aid availability : YES , we have TFWS for top rankers in which tution fees for that student in canclled
Admission office contact phone=(91)-(712)-2580011 email=rcoem@rknec.edu
for any question that cant be answered regarding admission = visit admissions in menu

Academic Information:
Course catalog : we provide all btech,and mba courses and mtech , phd courses also
Academic calendar : menu/academics/academics calendar
Faculty and staff directory : menu/faculty
Information on academic departments and programs : menu/academics
Library resources and hours.

Campus Facilities and Services:
Campus map and directions = "https://www.google.com/maps/place/Shri+Ramdeobaba+College+of+Engineering+and+Management/@21.1766264,79.0590474,17z/data=!3m1!4b1!4m6!3m5!1s0x3bd4c1a8970c08e9:0xfe4a9c97e7e671cb!8m2!3d21.1766214!4d79.0616223!16s%2Fm%2F05szf_z?entry=ttu"
Housing options and application procedures = facility of seperate boys and girls hostel , hostel mess and gym 
Student support services = personal counselling is provided
Campus events and activities = Pratishruti , Prerna , Manzer , and many more

Student Life:
Extracurricular activities and clubs = Technical club, SRC , NSS , GDSC , GFG , etc
Sports = football, cricket , vollyball , chess , basketball
Health and wellness resources.
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard