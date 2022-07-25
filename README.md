# API-Quizbowl-Program
Working with an API we used get, post, put, delete to manipulate and retrieve data in the api

## User
When you login as a regular user you are prompted to take a quiz   
Once you press enter the user will begin a 10 question quiz.   
After the quiz is over you will be shown your score, and if you missed any questions   
It will show you the question number, the question, your answer, and the right answer for each question missed.

Behind the scenes to create the quiz first an api get function is call to store all questions created in a variable.   
Then 10 random questions are selected with the contingency that they are not already in the quiz.

I also created an answer evaluator that interprates all fuzzy answers and will mark you as correct if you were on the right page.  
for instance if you answered dallas, cowboys, or the cowboys instead of The Dallas Cowboys as being a very sad team you'd be correct.

## Admin
When registering with my personal email, my program recognizes me as an admin and in my user data admin is set to true.   
As an admin I get a different prompt than a regular user.   
I can create questions using an api post function, edit questions using an api put function, delete questions using an api delete function, and can retrieve all   
of my questions using an api get function.

All of these functions require my token to modify and get my questions.

Also, all modification; additions, edits, deletions update the UI in real time

Because the Admin class inherits from the User class I can also choose to take a quiz see my score and all that jazz.

my admin email: dylankatina@gmail.com
my password: 123


