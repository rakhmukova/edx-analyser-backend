# COMMON : SECTION BEGINS

SQL_QUERY_STUDENTS_COUNT = '''
        SELECT COUNT(DISTINCT log_line ->> 'username')
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'username' != 'null' AND log_line ->> 'username' IS NOT NULL AND log_line ->> 'username' != ''
'''

SQL_QUERY_ACTIVE_STUDENTS_COUNT = '''
    SELECT 
        COUNT(DISTINCT(log_line ->> 'username')) AS username
    FROM logs
    WHERE   
        log_line #>> '{context, course_id}' = %s AND
        (log_line ->> 'event_type' LIKE 'textbook.pdf%%' OR
        (log_line ->> 'event_type' LIKE 'edx.forum%%') OR
        (log_line ->> 'event_type' LIKE '%%video%%' AND
        log_line ->> 'event_type' NOT LIKE 'edx.video.bumper.dismissed') OR
        (log_line ->> 'event_type' LIKE 'problem_check') AND
        log_line ->> 'event_type' NOT LIKE '%%/%%' AND
        log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != '')
'''

SQL_QUERY_WEEKLY_ACTIVE_USERS = """
    SELECT
        DATE_TRUNC('week', TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS'))::DATE,
        COUNT(DISTINCT log_line ->> 'username')
    FROM logs
    WHERE log_line #>> '{context, course_id}' = %s
    GROUP BY DATE_TRUNC('week', TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS'))    
    ORDER BY DATE_TRUNC('week', TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS'))::DATE
"""


SQL_QUERY_ACTIVITY_IN_SECTIONS = '''
    SELECT  
        CASE 
            WHEN log_line ->> 'event_type' LIKE 'textbook.pdf%%' THEN 'textbook'
            WHEN log_line ->> 'event_type' LIKE 'edx.forum%%' THEN 'forum'
            WHEN log_line ->> 'event_type' LIKE '%%problem%%' THEN 'problem'
            WHEN log_line ->> 'event_type' LIKE '%%video%%' THEN 'video'
            ELSE log_line ->> 'event_type' 
        END as event_type,
        COUNT(DISTINCT(log_line ->> 'username')) AS username
    FROM logs
    WHERE   
        log_line #>> '{context, course_id}' = %s AND
        (log_line ->> 'event_type' LIKE 'textbook.pdf%%' OR
        (log_line ->> 'event_type' LIKE 'edx.forum%%') OR
        (log_line ->> 'event_type' LIKE '%%video%%' AND
        log_line ->> 'event_type' NOT LIKE 'edx.video.bumper.dismissed') OR
        (log_line ->> 'event_type' LIKE 'problem_check') AND
        (log_line ->> 'event_type' NOT LIKE '%%/%%'))
    GROUP BY 
        CASE 
            WHEN log_line ->> 'event_type' LIKE 'textbook.pdf%%' THEN 'textbook'
            WHEN log_line ->> 'event_type' LIKE 'edx.forum%%' THEN 'forum'
            WHEN log_line ->> 'event_type' LIKE '%%problem%%' THEN 'problem'
            WHEN log_line ->> 'event_type' LIKE '%%video%%' THEN 'video'
            ELSE log_line ->> 'event_type' 
        END;
'''

# COMMON : SECTION ENDS



# PAGES: SECTION BEGINS

SQL_QUERY_COURSE_PAGES_POPULARITY = '''
        SELECT  
            log_line -> 'page' AS section_name, 
            COUNT(*) AS interaction_count
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'page' != 'null'
        GROUP BY section_name
        ORDER BY interaction_count DESC'''

#PAGES: SECTION ENDS



# TEXTBOOK: SECTION BEGINS

SQL_QUERY_SCROLLING_TIME = '''
    SELECT 
        url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)) AS textbook, 
        log_line ->> 'username' AS username,
        (TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP) AS current_time
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        (log_line ->> 'event_type' = 'textbook.pdf.page.scrolled' OR 
        log_line ->> 'event_type' = 'textbook.pdf.page.navigated' OR
        log_line ->> 'event_type' = 'textbook.pdf.thumbnails.toggled' OR
        log_line ->> 'event_type' = 'textbook.pdf.thumbnail.navigated') AND 
        log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != ''
    ORDER BY username, current_time
'''


SQL_QUERY_TEXTBOOK_POPULARITY = """
        SELECT 
            url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)) AS tutorial_book,
            COUNT(url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1))) AS interaction_count,
            COUNT(DISTINCT (log_line ->> 'username')) AS unique_users_count
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND log_line ->> 'event_type' LIKE '%%textbook%%'
        GROUP BY tutorial_book
        ORDER BY tutorial_book;
    """


SQL_QUERY_SEARCHED_PDF_TERMS = """
        SELECT 
           LEFT(TRIM((log_line ->> 'event')::json ->> 'query'), 100) as search_word,
           COUNT(*) AS count_number
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND 
              log_line ->> 'event_type' = 'textbook.pdf.search.executed' AND
              TRIM((log_line ->> 'event')::json ->> 'query') != '' AND
              LENGTH(TRIM((log_line ->> 'event')::json ->> 'query')) > 2  
        GROUP BY search_word
        ORDER BY count_number desc;
    """

# TEXTBOOK: SECTION ENDS



# VIDEOS: SECTION BEGINS

SQL_QUERY_PLAY_VIDEO_COUNT_DAILY = '''
        select 
            TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS') as time_run, 
            count (*) as count_of_start
        from logs
        where log_line #>> '{context, course_id}' = %s AND log_line ->> 'event_type' = 'play_video'
        group by time_run
        order by time_run'''

SQL_QUERY_VIDEO_INTERACTION = '''
    WITH interactions AS (
        SELECT
            ((log_line ->> 'event')::json ->> 'id') AS video_id,
            log_line ->> 'page' AS video_link, 
            COUNT(log_line ->> 'page') AS interaction_count
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            log_line ->> 'event_type' LIKE '%%video%%' AND 
            (log_line ->> 'page' LIKE '%%/%%' OR log_line ->> 'page' LIKE '%%xblock%%')
        GROUP BY video_id, video_link
    ),
    unique_views AS (
        SELECT
            ((log_line ->> 'event')::json ->> 'id') AS video_id,
            COUNT(DISTINCT(log_line ->> 'username')) AS unique_views
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            log_line ->> 'event_type' LIKE '%%video%%' AND 
            (log_line ->> 'page' LIKE '%%/%%' OR log_line ->> 'page' LIKE '%%xblock%%')
        GROUP BY video_id
    )
    SELECT
        i.video_id,
        i.video_link,
        i.interaction_count,
        COALESCE(u.unique_views, 0) AS unique_views
    FROM
        interactions i
    LEFT JOIN
        unique_views u
    ON
        i.video_id = u.video_id
    ORDER BY
        i.interaction_count DESC;
'''

SQL_QUERY_POPULAR_VIDEO_FRAGMENTS = """
SELECT 
    video_id,
    event_type,
    event_time
FROM (
    SELECT 
        ((log_line ->> 'event')::json ->> 'id') AS video_id,
        log_line ->> 'event_type' as event_type,
        ROUND(
    GREATEST(
        LEAST(
            ((log_line ->> 'event')::json ->> 'duration')::numeric, 
            ((log_line ->> 'event')::json ->> 'currentTime')::numeric
        ), 
        0
    )
) as event_time
    FROM logs
    WHERE   log_line #>> '{context, course_id}' = %s AND 
            (log_line ->> 'event_type' = 'play_video' OR
             log_line ->> 'event_type' = 'pause_video')
    
    UNION ALL
    
    SELECT 
        ((log_line ->> 'event')::json ->> 'id') AS video_id,
        'play_video' AS event_type,
        ROUND(
        GREATEST(
            LEAST(
                ((log_line ->> 'event')::json ->> 'duration')::numeric, 
                ((log_line ->> 'event')::json ->> 'new_time')::numeric
            ), 
            0
        )
    ) as event_time
    FROM logs
    WHERE log_line #>> '{context, course_id}' = %s 
        AND log_line ->> 'event_type' = 'seek_video'
    
    UNION ALL
    
    SELECT 
        ((log_line ->> 'event')::json ->> 'id') AS video_id,
        'pause_video' AS event_type,
        ROUND(
    GREATEST(
        LEAST(
            ((log_line ->> 'event')::json ->> 'duration')::numeric, 
            ((log_line ->> 'event')::json ->> 'old_time')::numeric
        ), 
        0
    )
) as event_time
    FROM logs
    WHERE log_line #>> '{context, course_id}' = %s 
        AND log_line ->> 'event_type' = 'seek_video'
) AS combined_events
ORDER BY video_id, event_time;

"""

# VIDEOS: SECTION ENDS


# PROBLEMS: SECTION BEGINS

SQL_QUERY_TASKS_SUMMARY = '''
SELECT 
    tasks_summary.task_id AS task_id,
    tasks_summary.min_correct_attempt AS attempt
    FROM (
        SELECT 
            log_line #>> '{event, problem_id}' AS task_id,
            log_line ->> 'username' AS username,
            MIN(log_line #>> '{event, attempts}') AS min_correct_attempt
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'event_type' = 'problem_check' AND log_line #>> '{event, success}' = 'correct'
        group by task_id, username
    ) tasks_summary
'''

SQL_QUERY_CORRECTLY_SOLVED_PROBLEMS = '''
    SELECT  
        problemsTable.problem_id AS problem_id,
        COALESCE(pages.problem_link, '') AS page_link,
        problemsTable.attempts AS all_attempts,
        correctlySolvedProblems.correct_attempts AS correct_attempts
    FROM (
        SELECT 
            log_line #>> '{event, problem_id}' AS problem_id,
            COUNT(log_line ->> 'event') AS attempts
        FROM 
            logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            log_line ->> 'event_type' = 'problem_check' AND log_line #>> '{event, problem_id}' != ''
        GROUP BY problem_id    
    ) problemsTable
    LEFT JOIN 
    (
        SELECT 
            log_line #>> '{event, problem_id}' AS problem_id,
            COUNT(log_line ->> 'event') AS correct_attempts
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'event_type' = 'problem_check' and log_line #>> '{event, success}' = 'correct'
        GROUP BY problem_id  
    ) AS correctlySolvedProblems
    ON correctlySolvedProblems.problem_id = problemsTable.problem_id
    LEFT JOIN
    (
        SELECT
            log_line #>> '{event, problem_id}' AS problem_id,
            log_line ->> 'referer' AS problem_link
        FROM logs
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'event_type' = 'problem_check' AND log_line ->> 'page' != ''
        GROUP BY problem_id, problem_link
    ) AS pages
    ON pages.problem_id = problemsTable.problem_id;
'''

# PROBLEMS: SECTION ENDS


# FORUM: SECTION BEGINS

SQL_QUERY_TOP_THREADS = '''
        SELECT
            threads.author AS author,
            threads.title AS title,
            threads.body AS body,
            COALESCE(all_comments.total_comments, 0) AS total_comments,
            COALESCE(all_votes.total_votes, 0) AS total_votes,
            'thread' AS question_type
        FROM
            (
                SELECT
                    log_line ->> 'username' AS author,
                    log_line #>> '{event, title}' AS title,
                    log_line #>> '{event, body}' AS body,
                    log_line #>> '{event, id}' AS thread_id
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' = 'edx.forum.thread.created'
            ) threads
        LEFT JOIN
            (
                SELECT
                    log_line #>> '{event, discussion, id}' AS thread_id,
                    COUNT(*) AS total_comments
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' IN ('edx.forum.comment.created', 'edx.forum.response.created')
                GROUP BY
                    thread_id
            ) AS all_comments ON threads.thread_id = all_comments.thread_id
        LEFT JOIN
            (
                SELECT
                    log_line #>> '{event, id}' AS thread_id,
                    COUNT(*) AS total_votes
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' = 'edx.forum.thread.voted'
                GROUP BY
                    thread_id
            ) AS all_votes ON threads.thread_id = all_votes.thread_id
        ORDER BY
            (COALESCE(all_comments.total_comments, 0) + COALESCE(all_votes.total_votes, 0)) DESC
        LIMIT 3;
'''

SQL_QUERY_TOP_RESPONSES = '''
        SELECT
            responses.author AS author,
            responses.title AS title,
            responses.body AS body,
            COALESCE(all_comments.total_comments, 0) AS total_comments,
            COALESCE(all_votes.total_votes, 0) AS total_votes,
            'response' AS question_type
        FROM
            (
                SELECT
                    log_line ->> 'username' AS author,
                    log_line #>> '{event, title}' AS title,
                    log_line #>> '{event, body}' AS body,
                    log_line #>> '{event, id}' AS response_id
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' = 'edx.forum.response.created'
            ) responses
        LEFT JOIN
            (
                SELECT
                    log_line #>> '{event, discussion, id}' AS response_id,
                    COUNT(*) AS total_comments
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' IN ('edx.forum.comment.created', 'edx.forum.response.created')
                GROUP BY
                    response_id
            ) AS all_comments ON responses.response_id = all_comments.response_id
        LEFT JOIN
            (
                SELECT
                    log_line #>> '{event, id}' AS response_id,
                    COUNT(*) AS total_votes
                FROM
                    logs
                WHERE
                    log_line #>> '{context, course_id}' = %s AND
                    log_line ->> 'event_type' = 'edx.forum.response.voted'
                GROUP BY
                    response_id
            ) AS all_votes ON responses.response_id = all_votes.response_id
        ORDER BY
            (COALESCE(all_comments.total_comments, 0) + COALESCE(all_votes.total_votes, 0)) DESC
        LIMIT 3;
'''

# FORUM: SECTION ENDS



# STUDENTS: SECTION BEGINS

SQL_QUERY_VIDEO_VIEWS = '''
    SELECT 
        log_line ->> 'username' AS username,
        count(distinct ((log_line ->> 'event')::json ->> 'id')) AS event_id
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'event_type' = 'play_video' AND 
        log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != ''
    GROUP BY username
'''

SQL_QUERY_TEXTBOOK_VIEWS = """
        SELECT 
            log_line ->> 'username' AS username,
            COUNT(distinct (url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)))) as tutorial_book
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            log_line ->> 'event_type' LIKE  '%%textbook%%' AND
            (log_line ->> 'username' != 'null' AND 
            log_line ->> 'username' IS NOT NULL AND 
            log_line ->> 'username' != '')
        GROUP BY username;
    """

SQL_QUERY_ACTIVITY_ON_FORUM = '''
        SELECT 
            log_line ->> 'username' AS username,
            count(distinct (log_line #>> '{event, id}')) as event_id
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            (log_line ->> 'event_type' = 'edx.forum.comment.created' or
            log_line ->> 'event_type' = 'edx.forum.response.created' or
            log_line ->> 'event_type' = 'edx.forum.thread.created') and
            (log_line ->> 'username' != 'null' AND 
            log_line ->> 'username' IS NOT NULL AND 
            log_line ->> 'username' != '')
        GROUP BY username;
'''

SQL_QUERY_SOLVED_TASKS = '''
        SELECT 
            log_line ->> 'username' AS username,
            COUNT(DISTINCT (log_line #>> '{event, problem_id}')) AS problem_id
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' = %s AND
            log_line ->> 'event_type' = 'problem_check' AND 
            log_line #>> '{event, success}' = 'correct' AND 
            log_line ->> 'username' != 'null' AND 
            log_line ->> 'username' IS NOT NULL AND 
            log_line ->> 'username' != ''
        group by username
'''

SQL_QUERY_TOTAL_USER_TIME_ON_COURSE = '''
            select
                log_line ->> 'username' as session_username,
                TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as session_date,
                log_line -> 'session' as session_name,
                MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP) as min_session_time,
                MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP) as max_session_time
            from logs
            where 
                log_line #>> '{context, course_id}' = %s AND
                log_line ->> 'session' != 'null' and 
                log_line ->> 'session' != '' and 
                log_line ->> 'username' != 'null' AND 
                log_line ->> 'username' IS NOT NULL AND 
                log_line ->> 'username' != ''
                group by session_username, session_name, session_date
'''


SQL_QUERY_TOTAL_DAYS_ON_COURSE = '''
            select
                log_line ->> 'username' as username,
                COUNT(DISTINCT (TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE)) as count_of_days
            from logs
            where 
                log_line #>> '{context, course_id}' = %s AND
                log_line ->> 'username' != 'null' AND 
                log_line ->> 'username' IS NOT NULL AND 
                log_line ->> 'username' != ''
            group by username
            order by count_of_days DESC
        '''


# STUDENTS: SEСTION ENDS



# UTILS: SECTION BEGINS

SQL_QUERY_UNIQUE_USERNAMES = """
        SELECT
            DISTINCT log_line ->> 'username' AS username 
        FROM logs 
        WHERE log_line #>> '{context, course_id}' = %s AND log_line ->> 'username' != 'null' AND log_line ->> 'username' != '' AND log_line ->> 'username' IS NOT NULL
        GROUP BY username 
"""


SQL_QUERY_UNIQUE_COURSES = """
        SELECT 
            DISTINCT log_line #>> '{context, course_id}',
            COUNT(*) 
        FROM logs
        WHERE 
            log_line #>> '{context, course_id}' != 'null' AND 
            log_line #>> '{context, course_id}' != '' AND
            log_line #>> '{context, course_id}' NOT LIKE '%/%'
        GROUP BY 
            log_line #>> '{context, course_id}'
"""

SQL_QUERY_URLS_AND_NAMES_MAPPING = '''select urlsAndIDs.target_name as target_name, uniqueUrls.target_url as target_url from (
            select 
                url_decode((log_line ->> 'event')::json ->> 'target_url') as target_url
            from logs
			where 
				log_line ->> 'event_type' LIKE '%link_clicked' or 
				log_line ->> 'event_type' LIKE '%selected'
            GROUP BY target_url 
        ) uniqueUrls
        LEFT JOIN (
            select 
				url_decode((log_line ->> 'event')::json ->> 'target_url') as target_url,
				(log_line ->> 'event')::json ->> 'target_name' as target_name
            from logs 
            where 
				(log_line ->> 'event_type' LIKE '%link_clicked' or 
				log_line ->> 'event_type' LIKE '%selected')
				and (log_line ->> 'event')::json ->> 'target_name' is not null
            GROUP BY target_name, target_url
        ) urlsAndIDs
        ON uniqueUrls.target_url = urlsAndIDs.target_url
		where uniqueUrls.target_url is not null
        order by target_name'''

# UTILS: SECTION ENDS

SQL_QUERY_STUDENTS_INFO = '''
SELECT
    COALESCE(td.username, vv.username, tv.username, af.username, st.username) AS username,
    COALESCE(td.total_days_on_course, 0) AS total_days_on_course,
    COALESCE(vv.event_id, 0) AS video_views,
    COALESCE(tv.tutorial_book, 0) AS textbook_views,
    COALESCE(st.solved_tasks, 0) AS solved_tasks,
    COALESCE(af.forum_activity, 0) AS forum_activity
FROM
    (SELECT
        log_line ->> 'username' AS username,
        COUNT(DISTINCT (TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE)) as total_days_on_course
    FROM logs
    WHERE
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'username' != 'null' AND
        log_line ->> 'username' IS NOT NULL AND
        log_line ->> 'username' != ''
    GROUP BY username) AS td
LEFT JOIN
    (SELECT 
        log_line ->> 'username' AS username,
        COUNT(distinct ((log_line ->> 'event')::json ->> 'id')) AS event_id
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'event_type' = 'play_video' AND 
        log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != ''
    GROUP BY username) AS vv ON td.username = vv.username
LEFT JOIN
    (SELECT 
        log_line ->> 'username' AS username,
        COUNT(distinct (url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)))) as tutorial_book
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'event_type' LIKE  '%%textbook%%' and
        (log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != '')
    GROUP BY username) AS tv ON td.username = tv.username
LEFT JOIN
    (SELECT 
        log_line ->> 'username' AS username,
        COUNT(DISTINCT (log_line #>> '{event, problem_id}')) AS solved_tasks
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'event_type' = 'problem_check' AND 
        log_line #>> '{event, success}' = 'correct' AND 
        log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != ''
    group by username) AS st ON td.username = st.username
LEFT JOIN
    (SELECT 
        log_line ->> 'username' AS username,
        count(distinct (log_line #>> '{event, id}')) as forum_activity
    FROM logs
    WHERE 
        log_line #>> '{context, course_id}' = %s AND
        log_line ->> 'event_type' IN ('edx.forum.comment.created', 'edx.forum.response.created', 'edx.forum.thread.created') and
        (log_line ->> 'username' != 'null' AND 
        log_line ->> 'username' IS NOT NULL AND 
        log_line ->> 'username' != '')
    GROUP BY username) AS af ON td.username = af.username
ORDER BY td.username;
'''