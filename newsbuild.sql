-- View definitions for the log analsis project.
--

CREATE VIEW uri_log AS
-- create view of article log only
   SELECT path, count(id) as visits
   FROM log
   GROUP BY path
   ORDER BY visits desc;

CREATE VIEW art_rank AS
-- create view of article rank by site visits
   SELECT articles.title, uri_log.visits as visits, articles.author as author_id
   FROM uri_log JOIN articles
   ON '/article/' || articles.slug = uri_log.path
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
   ORDER BY (count(status) FILTER (WHERE status = '404 NOT FOUND') * 1.000) / (count(status) * 1.000) desc;
