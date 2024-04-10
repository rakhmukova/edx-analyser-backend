# COMMON : SECTION BEGINS

SQL_QUERY_ALL_USERS_COUNT = '''
        SELECT COUNT(DISTINCT log_line ->> 'username')
        FROM logs
        WHERE log_line ->> 'username' != 'null' AND log_line ->> 'username' IS NOT NULL AND log_line ->> 'username' != ''
'''

SQL_QUERY_DAILY_ACTIVE_USERS = """
        SELECT
            TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS'),
            COUNT(DISTINCT log_line ->> 'username')
        FROM logs
        GROUP BY TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')    
        ORDER BY TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')
"""
# COMMON : SECTION ENDS



# PAGES: SECTION BEGINS

SQL_QUERY_COURSE_PAGES_POPULARITY = '''select  
            log_line -> 'page' as section_name, 
            count(*) as interaction_count
        from logs
        where log_line ->> 'page' != 'null'
        group by section_name
        order by interaction_count desc'''

#PAGES: SECTION ENDS



# TEXTBOOK: SECTION BEGINS

SQL_QUERY_DISTINCT_SCROLLING = """
        SELECT url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)) AS tutorial_book,
        COUNT(url_decode(split_part(reverse(split_part(reverse((log_line ->> 'event')::json ->> 'chapter'), '/', 1)), '/', 1)))
        FROM logs
        WHERE log_line ->> 'event_type'
        LIKE  '%textbook%'
        GROUP BY tutorial_book;
    """


SQL_QUERY_SEARCHED_PDF_TERMS = """
        SELECT 
           trim((log_line ->> 'event')::json ->> 'query') as search_word,
           count(*) AS count_number
        FROM logs
        WHERE log_line ->> 'event_type' = 'textbook.pdf.search.executed'
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
        where log_line ->> 'event_type' = 'play_video'
        group by time_run
        order by time_run'''

# VIDEOS: SECTION ENDS


# PROBLEMS: SECTION BEGINS

SQL_QUERY_PROBLEMS_SUMMARY = '''
    SELECT 
        log_line #>> '{event, problem_id}' AS problem_id,
        MIN(log_line #>> '{event, attempts}') AS min_correct_attempt
    FROM logs
    WHERE log_line ->> 'event_type' = 'problem_check' AND log_line #>> '{event, success}' = 'correct'
    group by problem_id, log_line ->> 'username'
'''

SQL_QUERY_CORRECTLY_SOLVED_PROBLEMS = '''
        SELECT  
                problemsTable.problem_id AS problem_id,
                problemsTable.attempts AS all_attempts,
                correctlySolvedProblems.correct_attempts AS correct_attempts 
        FROM (
            SELECT 
                log_line #>> '{event, problem_id}' AS problem_id,
                COUNT(log_line ->> 'event') AS attempts
            FROM 
                logs
            WHERE 
                log_line ->> 'event_type' = 'problem_check' AND log_line #>> '{event, problem_id}' != ''
            GROUP BY problem_id    
        ) problemsTable
        LEFT JOIN 
        (
            SELECT 
                    log_line #>> '{event, problem_id}' AS problem_id,
                    COUNT(log_line ->> 'event') AS correct_attempts
            FROM logs
            WHERE log_line ->> 'event_type' = 'problem_check' and log_line #>> '{event, success}' = 'correct'
            GROUP BY problem_id  
        ) AS correctlySolvedProblems
        ON correctlySolvedProblems.problem_id = problemsTable.problem_id;
'''

# PROBLEMS: SECTION ENDS


# FORUM: SECTION BEGINS

SQL_QUERY_TOP_THREADS = '''
        SELECT
            threads.author AS author,
            threads.title AS title,
            threads.body AS body,
            COALESCE(all_comments.total_comments, 0) AS total_comments,
            COALESCE(all_votes.total_votes, 0) AS total_votes
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
                    log_line ->> 'event_type' = 'edx.forum.thread.voted'
                GROUP BY
                    thread_id
            ) AS all_votes ON threads.thread_id = all_votes.thread_id
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
            log_line ->> 'event_type' LIKE  '%textbook%' and
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
            log_line ->> 'event_type' = 'edx.forum.comment.created' or
            log_line ->> 'event_type' = 'edx.forum.response.created' or
            log_line ->> 'event_type' = 'edx.forum.thread.created' and
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
            log_line ->> 'event_type' = 'problem_check' AND 
            log_line #>> '{event, success}' = 'correct' AND 
            log_line ->> 'username' != 'null' AND 
            log_line ->> 'username' IS NOT NULL AND 
            log_line ->> 'username' != ''
        group by username
'''

SQL_QUERY_TOTAL_USER_TIME_ON_COURSE = '''select total_time_per_day.username, SUM(total_time_per_day.time_at_session_per_day) as duration from (
            select durationTable.session_username as username, SUM(durationTable.session_duration) as time_at_session_per_day from (
                    select
                        log_line ->> 'username' as session_username,
                        age(MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP), MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP)) as session_duration
                    from logs
                    where 
                        log_line ->> 'session' != 'null' and 
                        log_line ->> 'session' != '' and 
                        log_line ->> 'username' != 'null' AND 
                        log_line ->> 'username' IS NOT NULL AND 
                        log_line ->> 'username' != ''
                        group by session_username, log_line ->> 'session'
                ) durationTable
                group by durationTable.session_username
        ) total_time_per_day
        group by total_time_per_day.username
        order by duration desc'''


SQL_QUERY_TOTAL_DAYS_ON_COURSE = '''
            select
                log_line ->> 'username' as username,
                COUNT(DISTINCT (TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE)) as count_of_days
            from logs
            where 
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
        WHERE log_line ->> 'username' != 'null' AND log_line ->> 'username' != '' AND log_line ->> 'username' IS NOT NULL
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