# TypeSmith

A typing test app built for the Bath Hack 2025 hosted by Bath Computer Science Society.

## Inspiration

Typing tests generally lack realistic punctuation, semantic meaning, and relevance to the user.
In addition, we believe that writing notes on an area of study helps improve recall, more so than taking a passive revision method such as simply reading over notes.
TypeSmith aims to improve the typing test experience, while promoting active study.

## What it does
**<u>Typing Test Relevant To You</u>** <br>
TypeSmith has three modes: theme, coding, and notes. 
<ul>
<li>Theme mode - Choose a theme for your passage to type.</li>
<li>Coding mode - Choose a coding language to type, great for practising syntax and special characters!</li>
<li>Notes mode - Upload your notes and type a summary. Improves active recall! </li>
</ul>

**<u>Practice Tricky Words</u>** <br>
As you type, TypeSmith keeps track of words you struggle to type. These words will show up in later typing tests so you can practice and improve!

## How we built it
We used PySide 6 to build the graphical interface while communicating with the OpenAI API to get the text that users need to type. We also used GitHub for version control.
We took an object-oriented approach in our code to assist in having multiple programmers working on a small project.

## Challenges we ran into
Keeping well documented code and good version control practices while operating over a small number of files was a priority, but conflicts still arise. When this happened it was very important that we had clear communication as a team to figure out what needed to stay or go

## Accomplishments that we're proud of
We managed to achieve most of our initial goals for this project as well as more ideas that appeared during development, while still having a concept which has great potential for further improvements and features.
We are also proud of our teamwork and communication; everyone stayed up to date with a good understanding of the inner workings of each part of the project, despite the fast pace of development.

## What we learned
Communication with the OpenAI API is very simple, and token cost is surprisingly low.
We have also learned that developing as part of a team allows for much faster development and a great environment for ideation and implementation.

## What's next for TypeSmith
<ul>
<li>Accessibility futures such as a colour blind mode</li>
<li>Uploading notes files to be summarised, rather than pasting in text</li>
<li>Reviewing previous results and tricky words, so users can track their progress</li>
</ul>

## Launching the program
```console
npm init
python app.py
```
