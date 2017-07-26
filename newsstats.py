#!/usr/bin/env python
#
# newsdata.py -- Internal Reporting Tool for Website Log Stats
#
import psycopg2
import sys
import newsdata
from datetime import datetime

filename = 'News-Stats' + str(datetime.now()) +".txt"

f = open(filename,"w+")

## Header
f.write("--- For Internal Purposes Only ---\n\n")
f.write("* Web Traffic Log Analysis *\n\n")

## Questions Section
f.write("1. What are the most popular three articles of all time?\n\n")
ans1 = newsdata.artRank()
f.write("1. {} -- {:,} pageviews\n".format(ans1[0][0],ans1[0][1]))
f.write("2. {} -- {:,} pageviews\n".format(ans1[1][0],ans1[1][1]))
f.write("3. {} -- {:,} pageviews\n".format(ans1[2][0],ans1[2][1]))

f.write("\n\n2. Who are the most popular article authors of all time?\n\n")
ans2 = newsdata.authRank()
f.write("1. {} -- {:,} pageviews\n".format(ans2[0][0],ans2[0][1]))
f.write("2. {} -- {:,} pageviews\n".format(ans2[1][0],ans2[1][1]))
f.write("3. {} -- {:,} pageviews\n".format(ans2[2][0],ans2[2][1]))

f.write("\n\n3. On which days did more than 1%\b of requests lead to errors?\n\n")
ans3 = newsdata.onePercentErrorDay()
f.write("{:%m-%d-%Y} -- {:,.2f} percent error rate\n".format(ans3[0],ans3[1] * 100))
