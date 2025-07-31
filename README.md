<!-- markdownlint-disable MD007 -->
# Microbloging Site

- Front end of HTML & W3.CSS, back end of Python, Flask and MongoDB
- Maximum of 140 characters per post
- Textarea content added to MongoDB upon submit button click
    - Delete a previous post from the list upon "x" button click
- MongoDB implemented on Cloud Atlas
- Timezone set to UTC + 1 hour
- Hitting browser refresh may resend post data, this is normal browser behaviour
    - clicking the URL+enter will prevent this possible behaviour.
- The flask app renders a new page every time there is a submitted or deleted post
    - going back and forward in the browser will show these different pages (normal browser behaviour)

## MongoDB Cloud Atlas

Remember to add your computer's IP to the allowable IPlist if you have network restriction security setup on your **Cloud Atlas MongoDB** account. If using a **VPN**, be aware of this.

## Setup

- `pyenv exec python -m venv .venv`
- `source ./.venv/bin/activate`
- `pip install -r requirements.txt`
- `python -m flask run`
