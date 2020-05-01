<h1 align="center"><a href="http://HackFactory.tech">View the Live App</a></h1>


# Inspiration

As avid hackathon attendees, we've noticed that there's always a lot of pressure to come up with clever ideas with the potential to win.

# What it does

Hackhacks generates winning hackathon ideas which are sure to win you prizes at your next hackathon. We also allow users to vote on the best ideas to crowdsource projects.

# How I built it

We web-scraped winning hackathon taglines and titles from DevPost using Uipath.

We finetuned a GPT2 model so that we could generate realistic descriptions of hackathons from the output of the model.

We used an online api to convert our taglines to unique titles and matching images/logos, falling back to google image search in case no title or image could be found.

We built a web backend using Flask, WebSockets, and MongoDB Atlas that stores our winning hackathon ideas as well as user feedback.

Our web application is built in bootstrap and vanilla JS.

# Challenges I ran into
One interesting result of training the GPT-2 system on our scraped dataset was that some of the generated results were exact copies of taglines from the training set.
We're still trying to figure out how to prevent this kind of overtraining from occuring while maintaining high quality hackathon predictions.

On the web development side of things, we found it difficult to balance getting functional code out quickly with delivering high quality code. Obviously it would be ideal
for our code to be beautiful, but we chose to code quickly instead as ugly functional code is better than useless beautiful code. This was largely due to the fact that web
development requires a lot of boilerplate code which is both time consuming and difficult to debug.

Finally, in the process of generating logos and project names, the unofficial API we were hitting had inconsistent functionality, and many queries would cause errors
(somehow within 200 OK responses instead of a 4XX response). 

# Accomplishments that I'm proud of 

We're proud of the fact that we completed a full stack effort which allows users to both get exposure to high quality hackathon ideas generated in our backend while interacting with
these same proposals (in the form of "liking" the content) in the frontend. Additionally, the chance to use production-ready software such as MongoDB Atlas was extremely fulfilling.

# What I learned

This was our first time using Uipath for webscraping, and we found it to be an essential and natural part of our workflow in order to retrieve winning hackathon ideas from Devpost.
We used this data to train a machine learning model for idea generation. We've never done text generation using machine learning before, and discovered a program that allows us to 
train OpenAI's GPT-2 model on our own dataset in a process called "fine-tuning", which takes the original GPT-2 model and alters its weights to optimize for our given input data. This forces
the output to be in a similar format to our training data, while maintaining all of the NLP features of the original GPT-2 model.

Additionally, to get banner images for our generated ideas, we used the Google images API, which allows us to programmatically search through google images and find relevent content based off
of keywords in our idea descriptions.

A few of us also didn't have a lot of web development experience, and found this project to be a tremendous learning experience for building full stack web applications.

# What's next for hackhacks

Build a hackathon project idea generated using our algorithm. We've noticed many incredible ideas come out of the algorithm such as:

1. We use geospatial data turbocharged with machine learning to detect multiple hazards such as flooding and parking spaces.
2. Use your natural vision to create VR realistic environments!
3. A website that allows students to learn about biodiversity in a virtual environment.
4. A program that uses computer vision to map out the locations of missing persons.
5. An app that allows geologists to rate the quality of their equipment against a scale ranging from 0 to 100.
6. A way to verify integrity of loan documents on the Ethereum blockchain


# Built with

Mongodb Atlas, python, flask, bootstrap, javascript

# Try it out



