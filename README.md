# **Log Analysis Reporting Tool**
This reporting tool gives the user the ability to a webserver log analysis on various website traffic metrics. The program is implemented in python using a back-end PostgreSQL database.

## **Getting Started**
### Prior to installation
Prior to loading the library, you should have:
- Installed [Vagrant](http://vagrantup.com/), [VirtualBox](https://www.virtualbox.org/).

### Installation
1. Clone/copy this repo
2. Launch the Vagrant VM (after navigating to the directory in which you saved this repo):
```
$ vagrant up
$ vagrant ssh
```
3. Programs using this library should be saved in the same directory as the cloned repo

### Database Setup
1. Load Data into 'news' database
From the appropriate filepath with newsdata.sql in that path, type the following:
```
$ psql -d news -f newsdata.sql
```
Please try [this link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) if you do not have access to the newsdata.sql file.
2. Import newsbuild.sql into 'news' database
Commands can be imported in or be copy-pasted in after logging into 'news' database from the CL.
```
$ psql news
>>>
CREATE VIEW uri_log AS
-- create view of article log only
   SELECT split_part(path, '/article/', 2) as article_short, count(id) as visits
   FROM log
   WHERE path like '/article/%'
   GROUP BY article_short
   ORDER BY visits desc;

CREATE VIEW art_rank AS
-- create view of article rank by site visits
   SELECT articles.title, uri_log.visits as visits, articles.author as author_id
   FROM uri_log JOIN articles
   ON articles.slug = uri_log.article_short
   ORDER BY uri_log.visits desc;

CREATE VIEW auth_rank AS
-- create view of author rank by site visits to their articles
   SELECT authors.name, sum(art_rank.visits)
   FROM authors left JOIN art_rank
   ON authors.id = art_rank.author_id
   Group BY authors.name
   ORDER BY sum(art_rank.visits) desc;

CREATE VIEW log_status_rank AS
-- create view of day ranking by % of http request resulting in error status codes
   SELECT date(time) as day, count(status) as total, count(status) FILTER (WHERE status = '200 OK') as success, count(status) FILTER (WHERE status = '404 NOT FOUND') as err_code, (count(status) FILTER (WHERE status = '404 NOT FOUND') * 1.000) / (count(status) * 1.000) as percent_errors
   FROM log
   Group BY date(time)
   ORDER BY (count(status) FILTER (WHERE status = '404 NOT FOUND') * 1.000) / (count(status) * 1.000) desc
   LIMIT 10;
```
3. Programs using this library should be saved in the same directory as the cloned repo

## **Running Log Analysis**
From the directory in which the files are saved type:
```
$ python3 ./newsstats.py
```
This program will create a .txt file in that same directory that is timestamped. If you want to re-run the program, a new file will be created--the old document won't be changed.

## **Common Usage**
Programs that use this library are most often run from the command line but can be run with modifications from other GUIs

## **Known Issues**
The code has the following known issues:
1. The only error code that is caught by the log right now is a '404 - NOT FOUND' code.
    - If the site were to experience additional errors (it had not when this code was released), the error rate for certain days would be under estimated.
2. Some of the code in `newsbuild.sql` is, admittedly, not as efficient as it could be
    - Later iterations of this code or pull requests could improve the efficiency of various views

## **License**
This code is covered under an [MIT License](./LICENSE)
