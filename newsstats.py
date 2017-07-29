#!/usr/bin/env python
#
# newsdata.py -- Internal Reporting Tool for Website Log Stats
#
import psycopg2
import sys
import newsdata
from datetime import datetime

filename = 'News-Stats' + str(datetime.now()) + ".txt"

f = open(filename, "w+")

# Header
f.write("--- For Internal Purposes Only ---\n\n")
f.write("* Web Traffic Log Analysis *\n\n")
# Questions Section

# Question 1
f.write("1. What are the most popular three articles of all time?\n\n")
ans1 = newsdata.artRank()
for counter, ans in enumerate(ans1):
    f.write("{}. {} -- {:,} pageviews\n"
            .format(counter + 1, ans1[counter][0], ans1[counter][1]))

# Question 2
f.write("\n\n2. Who are the most popular article authors of all time?\n\n")
ans2 = newsdata.authRank()
for counter, ans in enumerate(ans2):
    f.write("{}. {} -- {:,} pageviews\n"
            .format(counter + 1, ans2[counter][0], ans2[counter][1]))

# Question 3
f.write("\n\n")
f.write("3. On which days did more than 1%\b of requests lead to errors?\n\n")
ans3 = newsdata.onePercentErrorDay()
for counter, ans in enumerate(ans3):
    if ans3[counter][1] < 0.02:
        break
    f.write("{}. {:%B %d, %Y} -- {:,.2f} percent error rate\n"
            .format(counter + 1, ans3[counter][0], ans3[counter][1] * 100))
