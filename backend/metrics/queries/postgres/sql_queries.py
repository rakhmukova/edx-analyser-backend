SQL_QUERY_COMPLETED_COURSE_USERS = '''select allUsers.user_id as user_id, allUsers.user_name as user_name from (
            
            select uniqueUserIds.user_id as user_id, userAndIDs.user_name as user_name from (
                select 
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                GROUP BY user_id 
            ) uniqueUserIds
            
            LEFT JOIN (
                select 
                    log_line -> 'username' as user_name,
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                where log_line -> 'username' != 'null' and log_line -> 'username' != '""' and log_line -> 'username' is not null
                GROUP BY user_id, user_name
            ) userAndIDs
            
            ON uniqueUserIds.user_id = userAndIDs.user_id
        ) allUsers
        
        INNER JOIN (
            select 
                log_line #>> '{context, user_id}' as user_id
            from logs where log_line ->> 'name' LIKE 'edx.special_exam%'
            group by user_id
        ) usersWhoStartedAnyExam
        
        ON allUsers.user_id = usersWhoStartedAnyExam.user_id
        group by allUsers.user_id, user_name
        order by user_name desc'''

SQL_QUERY_ENROLLED_USERS_WITHOUT_ACTIVITY = '''select notStartedUsers.enrolled_but_not_started as user_id, userNames.user_name as user_name, notStartedUsers.enrollment_date as enrollment_date from (
            select enrolledUsers.user_id as enrolled_but_not_started, enrolledUsers.enrollment_date as enrollment_date from (
                select   
                    log_line #>> '{event, user_id}' as user_id,
                    TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as enrollment_date
                from logs
                where log_line #>> '{event_type}' = 'edx.course.enrollment.activated'		
            ) enrolledUsers
            LEFT JOIN (
                select total_time_per_day.user_id as user_id, SUM(total_time_per_day.time_at_session_per_day) as duration from (
                        select durationTable.session_user_id as user_id, durationTable.session_date, SUM(durationTable.session_duration) as time_at_session_per_day from (
                                select
                                    log_line #>> '{context, user_id}' as session_user_id,
                                    TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as session_date,
                                    log_line -> 'session' as session_name,
                                    age(MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP), MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP)) as session_duration
                                from logs
                                where log_line ->> 'session' != 'null' and log_line ->> 'session' != ''
                                    group by session_user_id, session_name, session_date
                            ) durationTable
                            group by durationTable.session_user_id, durationTable.session_date
                    ) total_time_per_day
                    group by total_time_per_day.user_id
            ) userTimeOnCourse
            ON userTimeOnCourse.user_id = enrolledUsers.user_id
            where userTimeOnCourse.user_id is null or duration = '00:00:00'
        ) notStartedUsers
        INNER JOIN (
            select uniqueUserIds.user_id as user_id, userAndIDs.user_name as user_name from (
                select 
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                GROUP BY user_id 
            ) uniqueUserIds
            LEFT JOIN (
                select 
                    log_line -> 'username' as user_name,
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                where log_line -> 'username' != 'null' and log_line -> 'username' != '""' and log_line -> 'username' is not null
                GROUP BY user_id, user_name
            ) userAndIDs
            ON uniqueUserIds.user_id = userAndIDs.user_id
        ) userNames
        ON userNames.user_id = notStartedUsers.enrolled_but_not_started
        group by user_name, notStartedUsers.enrolled_but_not_started, enrollment_date       
        order by user_name desc NULLS LAST'''

SQL_QUERY_STARTED_BUT_NOT_COMPLETED_USERS = '''
        select allUsers.user_id as user_id, allUsers.user_name as user_name from (
            select uniqueUserIds.user_id as user_id, userAndIDs.user_name as user_name from (
                select 
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                GROUP BY user_id 
            ) uniqueUserIds
            LEFT JOIN (
                select 
                    log_line -> 'username' as user_name,
                    log_line #>> '{context, user_id}' AS user_id 
                from logs 
                where log_line -> 'username' != 'null' and log_line -> 'username' != '""' and log_line -> 'username' is not null
                GROUP BY user_id, user_name
            ) userAndIDs
            ON uniqueUserIds.user_id = userAndIDs.user_id
        ) allUsers
        INNER JOIN (		
			select userTimeOnCourse.user_id as user_id from (
				select total_time_per_day.user_id as user_id, SUM(total_time_per_day.time_at_session_per_day) as duration from (
					select durationTable.session_user_id as user_id, durationTable.session_date, SUM(durationTable.session_duration) as time_at_session_per_day from (
							select
								log_line #>> '{context, user_id}' as session_user_id,
								TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as session_date,
				    			log_line -> 'session' as session_name,
								age(MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP), MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP)) as session_duration
							from logs
							where log_line ->> 'session' != 'null' and log_line ->> 'session' != ''
								group by session_user_id, session_name, session_date
						) durationTable
						group by durationTable.session_user_id, durationTable.session_date
				) total_time_per_day
				group by total_time_per_day.user_id
			) userTimeOnCourse
			LEFT JOIN (
				select 
					log_line #>> '{context, user_id}' as user_id
				from logs where log_line ->> 'name' LIKE 'edx.special_exam%'
				group by user_id
			) usersWhoStartedAnyExam
			ON userTimeOnCourse.user_id = usersWhoStartedAnyExam.user_id
			where usersWhoStartedAnyExam.user_id is null and userTimeOnCourse.duration > '00:00:00'
         ) usersWhoStartedCourseAndDidntTryAnyExam
        ON allUsers.user_id = usersWhoStartedCourseAndDidntTryAnyExam.user_id
        group by allUsers.user_id, user_name
        order by user_name desc NULLS last'''

SQL_QUERY_DISTINCT_SCROLLING = """
        SELECT url_decode(split_part((log_line ->> 'event')::json ->> 'chapter','/', 7)) AS tutorial_book, 
        COUNT(url_decode(split_part((log_line ->> 'event')::json ->> 'chapter','/', 7)))
        FROM logs 
        WHERE log_line ->> 'event_type'
        LIKE  '%pdf%'
        GROUP BY tutorial_book;
    """

SQL_QUERY_DISTINCT_VIEWS_OF_AVAILABLE_PDF = """
        SELECT url_decode(split_part((log_line ->> 'event')::json ->> 'chapter','/', 7)) AS tutorial_book,
         COUNT(url_decode(split_part((log_line ->> 'event')::json ->> 'chapter','/', 7)))
        FROM logs WHERE log_line ->> 'event_type' = 'textbook.pdf.page.scrolled' 
        GROUP BY tutorial_book
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

SQL_QUERY_PLAY_PAUSE_EVENTS = ''' SELECT log_line ->> 'event_type' as event_t, 
	                                         log_line -> 'username' as username,
											 log_line -> 'time' as time 
	    							  FROM logs 
									  WHERE log_line ->> 'event_type' = 'pause_video' OR 
		    						        log_line ->> 'event_type' = 'play_video' '''

SQL_QUERY_PLAY_VIDEO_TIMES = '''select 
            TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS') as time_run, 
            count (*) as count_of_start
        from logs
        where log_line ->> 'event_type' = 'play_video'
        group by time_run
        order by time_run'''

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

SQL_QUERY_USER_ROUTE = '''select uniqueUrls.target_url as target_url, urlsAndIDs.target_name as target_name from (
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

SQL_QUERY_DISTINCT_EVENT_TYPES = '''select DISTINCT log_line -> 'name' AS edx_event from logs order by edx_event'''

SQL_QUERY_DISTINCT_USER_NAMES_IDS_EVENTS = '''select tbl.usr, tbl.evt, url_map.target_name, tbl.cnt from (
    with events (name) as (values ('play_video'), ('pause_video'), ('load_video'), ('edx.special_exam.proctored.attempt.started'), ('edx.ui.lms.outline.selected')),
    modules (url) as (	
	with pages (page) as (select distinct (log_line ->> 'page') from logs)
	select distinct
		case
    		when POSITION('?' in page) > 0 THEN SUBSTRING(page, 0, POSITION('?' in page))
    		when POSITION('#' in page) > 0 THEN SUBSTRING(page, 0, POSITION('#' in page))
    		else page
  		end as url
		from pages
		where page is not null
    ),
    mod_event (usr, mdl, evt) as (
	select
		coalesce (l.log_line ->> 'username', '<<' || (l.log_line #>> '{context, user_id}') || '>>'),
		case
    		when POSITION('?' in l.log_line ->> 'page') > 0 THEN SUBSTRING(l.log_line ->> 'page', 0, POSITION('?' in l.log_line ->> 'page'))
    		when POSITION('#' in l.log_line ->> 'page') > 0 THEN SUBSTRING(l.log_line ->> 'page', 0, POSITION('#' in l.log_line ->> 'page'))
    		else l.log_line ->> 'page'
  		end as url,
		l.log_line ->> 'event_type'
	from logs as l
    )
    select usr, mdl, evt, count(*) as cnt from mod_event
    where mdl in (select url from modules)
    	and evt in (select name from events)
    group by usr, mdl, evt
	) tbl	
	join (
		select 
				url_decode((log_line ->> 'event')::json ->> 'target_url') as target_url,
				(log_line ->> 'event')::json ->> 'target_name' as target_name
            from logs 
            where 
				(log_line ->> 'event_type' LIKE '%link_clicked' or 
				log_line ->> 'event_type' LIKE '%selected')
				and (log_line ->> 'event')::json ->> 'target_name' is not null
				and (log_line ->> 'event')::json ->> 'target_name' not LIKE '%текущий раздел%'
            GROUP BY target_name, target_url	
	) url_map
	on tbl.mdl = url_map.target_url	
    order by usr'''

SQL_QUERY_EVENTS_DISTRIBUTION = '''select 
            log_line ->> 'name' as event_name,
            TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS') as time_run,
            count (*) as count_of_start
        from logs
        where log_line ->> 'name' != \'\''''

SQL_QUERY_TOTAL_USER_TIME_ON_COURSE = '''select total_time_per_day.user_id, SUM(total_time_per_day.time_at_session_per_day) as duration from (
            select durationTable.session_user_id as user_id, durationTable.session_date, SUM(durationTable.session_duration) as time_at_session_per_day from (
                    select
                        log_line #>> '{context, user_id}' as session_user_id,
                        TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as session_date,
                        log_line -> 'session' as session_name,
                        age(MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP), MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP)) as session_duration
                    from logs
                    where log_line ->> 'session' != 'null' and log_line ->> 'session' != ''
                        group by session_user_id, session_name, session_date
                ) durationTable
                group by durationTable.session_user_id, durationTable.session_date
                order by durationTable.session_date desc
        ) total_time_per_day
        group by total_time_per_day.user_id
        order by duration desc'''

SQL_QUERY_USER_TIME_ON_COURSE_PER_DAY = '''select durationTable.session_user_id, durationTable.session_date, SUM(durationTable.session_duration) as time_at_session_per_day from (
            select
                log_line #>> '{context, user_id}' as session_user_id,
                TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::DATE as session_date,
                log_line -> 'session' as session_name,
                age(MAX(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP), MIN(TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP)) as session_duration
            from logs
            where log_line ->> 'session' != 'null' and log_line ->> 'session' != ''
                and log_line #>> '{context, user_id}' = %s
                group by session_user_id, session_name, session_date
        ) durationTable
        group by durationTable.session_user_id, durationTable.session_date
        order by durationTable.session_date desc'''

SQL_QUERY_PAGE_ACTIVITY_PER_DAY = '''select   
            log_line -> 'page' as section_name, 
            TO_DATE(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS') as time_run,
            count(*) as interaction_count
        from logs
        where log_line ->> 'page' != 'null'
        group by section_name, time_run
        order by interaction_count desc'''

GET_UNIQUE_PAGES_URLS = '''select  
            log_line -> 'page' as section_name, 
            count(*) as interaction_count
        from logs
        where log_line ->> 'page' != 'null'
        group by section_name
        order by interaction_count desc'''

USER_PAGES_VISITED_AT_TIMEDATE = '''select 
            TO_TIMESTAMP(log_line ->> 'time', 'YYYY-MM-DD"T"HH24:MI:SS')::TIMESTAMP as time_access,
            log_line ->>'page' as page_visited
        from logs
        where 
        log_line #>> '{context, user_id}' = %s
        and log_line ->>'page' is not null 
            and log_line ->>'page' != 'x_module'
            order by time_access'''
