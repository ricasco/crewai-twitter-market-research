#!/usr/bin/env python
from twitter.crew import TwitterCrew
import datetime

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        'twitter_description': input('Enter the Twitter page description here: '),
        'topic_of_the_week': input('Enter the topic of the week here: '),
    }
    TwitterCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()