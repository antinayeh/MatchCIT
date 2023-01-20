# Match CIT: 
A web app that helps MCIT students find true love.
## Collaboraters: 
* [Peici Qiu](https://github.com/peiciqiu) 
* [Antina Yeh](https://github.com/antinayeh)
* Norris Chen
## Description: 
Finding love can be hard for anyone, but it is especially hard when you are a graduate student studying Computer Science who is too busy to go on 10 failed dates before finding your true love. That is why we created Match CIT: a dating web app for the MCIT community at the University of Pennsylvania. 

Through Match CIT, students can fill out a curated survey asking them about their personality, interests, values and much more. This data will then be sent to our database, where our own matching algorithm will run on the data and generate a list of top 3 most compatible matches out of all the Match CIT users for each student. Students will then recieve an email showing their top matches, including a compatability score for each match. Our algorithm uses machine learning algorithms such as k means clustering to help generate the results. Now when students go on dates with their matches, they can be sure that they are at least MatchCIT-verified compatible, increasing their chance of finding true love by just a bit more! 

## Design Flow:
* User fills out the survey
* Frontend sends survey responses in HTML Form data by HTTP POST request to backend api /api/signup
* Backend receives the data and stores in user table of a local SQLite database instance
* Admin triggers matching process by sending GET request to backend api /api/match
* Backend loads survey data from database, generates matches and stores the match results in a csv file
* Admin triggers notification process by sending GET request to backend api /api/notify
* Backend loads match results from the csv file and sends out emails
## Algorithm: 

There are plenty of algorithms being used in the current dating market. For example, Tinder uses an Elo system (similar to the chess system) where the more people swipe right on your profile, the more Elo you have. People with similar Elo will see each other more on their app, which makes the app kind of a popularity contest. On the other side of the spectrum, Hinge uses the Gale Shapley Algorithm which is a stable marriage problem that tries to match everyone so everyone reaches a happy medium. We wanted to do something innovative from all the dating apps on the market while still preserving two core values we think dating should be based on:

1) People should have an opportunity to reach out to the people we think they are the MOST compatible with
2) People should be matched on both their similarities AND their differences
### Similarity Matching:
We similarly paired people on their hobbies and their values. Values included their religion and their love languages while hobbies include sports, indoor activities, and social events. We pair people using an unsupervised machine learning algorithm of k-means clustering. K-means clustering groups data points based on certain similarities. Most of the time, the grouping is done based on a distance equation and the number of clusters is done based on an optimal k number search algorithm called the elbow method which graphs the number of k(clusters) with the sum of squared error within clusters. 

Before all of the algorithms, we must make sure the data can be run through k means. This means running One Hot Encoding algorithms for the data fields that return some strings. For example both religion and the aesthetics data fields needed to be one hot encoded. After all that, we need to standard scale all the data so they all weighed the same when using k-means. This ensures the same weights are applied evenly to all fields.

### Difference Matching
We differently paired people based on their physical appearance and personality. For data fields like height, weight, and age, we believe people can have preferences that are not similar to their own physical traits. This means we needed to create a compatibility score to enumerate the compatibility between two people based on their own physical traits and their preferred traits. We do this by first finding the difference between people’s preferred trait and other people’s original trait. The smaller the number, the closer they are compatible to each other. Since we wanted the larger number to be more compatible, we inverted the number and unit scaled it to be between 0 and 1. Then, finding the compatibility score for each of the physical traits(age, height, race) and personality, we plug it into our final equation giving each of the traits a specific weight based on research and experience. Then we chose the top three compatible person for each person and send the emails! Please look at MatchMakingAlgorithm.ipynb for the code!

## Up Next:
For the purposes of MCIT dating, our program is sufficient enough to meet the needs of the students in the program. However, as we think about scaling we have three ideas that would help in making the whole idea more robust:
1) Making accounts for the users to put in their information so the results can be sent to their accounts instead of emails. Their accounts can now contain more information about the user, not just what is in the survey and people can browse each other accounts and add more links or pictures to their own accounts to personalize their accounts even more
2) Making the whole system more dynamic. Instead of running the algorithm once, we can make it so everytime a new user is added to the database, we can run the program again so people can always get new matches on their accounts.
3) We can try to find datasets online that have people who kept dating after 3 months of matching. With these datasets, we can run their features in a forward feeding neural network to find the model to predict matches for people that would last at least 3 months.


## Tech Stack:
* Frontend: HTML, CSS, Javascript 
* Backend: Python Flask, Postman API 
* Database: SQLite


## Demo: 
* Watch our demo video [here](https://www.youtube.com/watch?v=RrXoyc01ezg)! <br />
