#
# Migrate extras (comments, ratings and waiting times) from old (pre-Feb 2015)
# Hitchwiki maps DB:
#
# - hitchwiki_maps.t_comments
# - hitchwiki_maps.t_waitingtimes
# - hitchwiki_maps.t_ratings
#
# to the tables of the new custom MediaWiki extensions:
#
# - HWComments:
#   - hitchwiki_en.hw_comments
#   - hitchwiki_en.hw_comments_count
# - HWRatings:
#   - hitchwiki_en.hw_ratings
#   - hitchwiki_en.hw_ratings_avg
# - HWWaitingTime:
#   - hitchwiki_en.hw_waiting_time
#   - hitchwiki_en.hw_waiting_time_avg
#
# Relies on hitchwiki_maps.point_page_mappings table generated by spotmigrate.py
#

import ConfigParser
import MySQLdb

settings = ConfigParser.ConfigParser()
settings.read('../../configs/settings.ini')
dummy_user_id = 0

db = MySQLdb.connect(
    host=settings.get('db', 'host'),
    user=settings.get('db', 'username'),
    passwd=settings.get('db', 'password'),
    db=settings.get('db', 'database')
)

print 'Truncate comments table...'

comments_del_cur = db.cursor()
comments_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_comments'
)
db.commit()

print 'Import spot comments...'

comments_cur = db.cursor()
comments_cur.execute(
    'INSERT INTO hitchwiki_en.hw_comments' +
        ' (hw_comment_id, hw_user_id, hw_page_id, hw_timestamp, hw_commenttext)' +
    " SELECT c.id, c.fk_user, ppm.page_id, DATE_FORMAT(c.datetime, '%Y%m%d%H%i%S'), c.comment" +
        ' FROM hitchwiki_maps.t_comments AS c' +
        ' LEFT JOIN hitchwiki_maps.point_page_mappings AS ppm' +
            ' ON ppm.point_id = c.fk_place' +
        ' WHERE ppm.page_id IS NOT NULL' # import comments only for imported spots
)
db.commit()

print 'Truncate comment counts table...'

comments_count_del_cur = db.cursor()
comments_count_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_comments_count'
)
db.commit()

print 'Update comment count for each page...'

comment_count_cur = db.cursor()
comment_count_cur.execute(
    'INSERT INTO hitchwiki_en.hw_comments_count' +
        ' (hw_page_id, hw_comments_count)' +
    ' SELECT hw_page_id, COUNT(*)' +
        ' FROM hitchwiki_en.hw_comments' +
        ' GROUP BY hw_page_id'
)
db.commit()

print 'Truncate spot ratings table...'

ratings_del_cur = db.cursor()
ratings_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_ratings'
)
db.commit()

print 'Import spot ratings...'

ratings_cur = db.cursor()
ratings_cur.execute(
    'INSERT INTO hitchwiki_en.hw_ratings' +
        ' (hw_rating_id, hw_user_id, hw_page_id, hw_timestamp, hw_rating)' +
    " SELECT r.id, r.fk_user, ppm.page_id, DATE_FORMAT(r.datetime, '%Y%m%d%H%i%S'), 6 - r.rating" +
        ' FROM hitchwiki_maps.t_ratings AS r' +
        ' LEFT JOIN hitchwiki_maps.point_page_mappings AS ppm' +
            ' ON ppm.point_id = r.fk_point' +
        ' WHERE r.rating <> 0' + # ignore "none" ratings
            ' AND ppm.page_id IS NOT NULL' # import ratings only for imported spots
)
db.commit()

print 'Truncate spot rating aggregates (avg, count) table...'

ratings_avg_del_cur = db.cursor()
ratings_avg_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_ratings_avg'
)
db.commit()

print 'Update average rating and rating count for each page...'

rating_avg_cur = db.cursor()
rating_avg_cur.execute(
    'INSERT INTO hitchwiki_en.hw_ratings_avg' +
        ' (hw_page_id, hw_count_rating, hw_average_rating)' +
    ' SELECT hw_page_id, COUNT(*), AVG(hw_rating)' +
        ' FROM hitchwiki_en.hw_ratings' +
        ' GROUP BY hw_page_id'
)
db.commit()

print 'Truncate waiting times table...'

waiting_times_del_cur = db.cursor()
waiting_times_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_waiting_time'
)
db.commit()

print 'Import spot waiting times...'

waiting_times_cur = db.cursor()
waiting_times_cur.execute(
    'INSERT INTO hitchwiki_en.hw_waiting_time' +
        ' (hw_waiting_time_id, hw_user_id, hw_page_id, hw_timestamp, hw_waiting_time)' +
    " SELECT w.id, w.fk_user, ppm.page_id, DATE_FORMAT(w.datetime, '%Y%m%d%H%i%S'), w.waitingtime" +
        ' FROM hitchwiki_maps.t_waitingtimes AS w' +
        ' LEFT JOIN hitchwiki_maps.point_page_mappings AS ppm' +
            ' ON ppm.point_id = w.fk_point' +
        ' WHERE ppm.page_id IS NOT NULL' # import waiting times only for imported spots
)
db.commit()

print 'Truncate waiting time aggregates (min, max, avg, count) table...'

waiting_times_avg_del_cur = db.cursor()
waiting_times_avg_del_cur.execute(
    'TRUNCATE hitchwiki_en.hw_waiting_time_avg'
)
db.commit()

print 'Update min waiting time, max waiting time and waiting time count for each page...'

waiting_time_count_cur = db.cursor()
waiting_time_count_cur.execute(
    'INSERT INTO hitchwiki_en.hw_waiting_time_avg' +
        ' (hw_page_id, hw_count_waiting_time, hw_min_waiting_time, hw_max_waiting_time)' +
    ' SELECT hw_page_id, COUNT(*), MIN(hw_waiting_time), MAX(hw_waiting_time)' +
        ' FROM hitchwiki_en.hw_waiting_time' +
        ' GROUP BY hw_page_id'
)
db.commit()

print 'Update median waiting times...'

waiting_time_all_cur = db.cursor(MySQLdb.cursors.DictCursor)
waiting_time_all_cur.execute(
    "SELECT hw_page_id, GROUP_CONCAT(hw_waiting_time ORDER BY hw_waiting_time SEPARATOR ';') AS waiting_times" +
        ' FROM hitchwiki_en.hw_waiting_time' +
        ' GROUP BY hw_page_id'
)
for waiting_time_group in waiting_time_all_cur.fetchall():
    waiting_times = waiting_time_group['waiting_times'].split(';')
    count = len(waiting_times)
    if count & 1: # odd number of waiting times; median is the middle number
        median = int(waiting_times[(count - 1) / 2])
    else: # even number of waiting times; median is the mean value of the two middle numbers
        middle1 = float(waiting_times[count / 2 - 1])
        middle2 = float(waiting_times[count / 2])
        median = (middle1 + middle2) / 2

    waiting_time_median_cur = db.cursor()
    waiting_time_median_cur.execute((
        "UPDATE hitchwiki_en.hw_waiting_time_avg" +
            ' SET hw_average_waiting_time = %f ' +
            ' WHERE hw_page_id = %d'
    ) % (median, waiting_time_group['hw_page_id']))
    db.commit()
