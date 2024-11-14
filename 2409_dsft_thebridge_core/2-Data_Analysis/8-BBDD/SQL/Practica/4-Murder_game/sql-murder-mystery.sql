SELECT
*
FROM crime_scene_report 
WHERE date = 20180115 AND type = "murder" and city = "SQL City";

-- Security footage shows that there were 2 witnesses. The first witness lives at the last house on "Northwestern Dr". The second witness, named Annabel, lives somewhere on "Franklin Ave".

SELECT
*
FROM person
INNER JOIN interview ON person.id = interview.person_id
WHERE name like "%Annabel%" AND address_street_name LIKE "%Franklin Ave%";
--id 16371
--I saw the murder happen, and I recognized the killer from my gym when I was working out last week on January the 9th.

SELECT
*
FROM person
INNER JOIN interview ON person.id = interview.person_id
WHERE person.address_number = 
(
SELECT
MAX(address_number)
FROM person
WHERE address_street_name LIKE "%Northwestern Dr%")
--ORDER BY address_number DESC;
-- I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag. The membership number on the bag started with "48Z". Only gold members have those bags. The man got into a car with a plate that included "H42W".

SELECT 
p.name,
i.*
FROM get_fit_now_check_in gc
INNER JOIN get_fit_now_member gm ON gc.membership_id = gm.id
INNER JOIN person p ON gm.person_id = p.id
INNER JOIN drivers_license dl ON p.license_id = dl.id
INNER JOIN interview i ON p.id = i.person_id
WHERE gc.check_in_date = 20180109 AND gc.membership_id LIKE "48Z%" AND membership_status = "gold" AND plate_number LIKE "%H42W%"
;
--Jeremy Bowers
--I was hired by a woman with a lot of money. I don't know her name but I know she's around 5'5" (65") or 5'7" (67"). She has red hair and she drives a Tesla Model S. I know that she attended the SQL Symphony Concert 3 times in December 2017.

SELECT
	f.person_id,
	COUNT(f.event_id),
    p.name,
    dl.*
FROM 
	facebook_event_checkin f
INNER JOIN 
	person p ON p.id = f.person_id
INNER JOIN 
	drivers_license dl ON p.license_id = dl.id
WHERE 
	f.date BETWEEN 20171201 AND 20171231
	AND f.event_name LIKE "%SQL Symphony Concert%"
    AND dl.car_make LIKE "%Tesla%"
    AND dl.hair_color = "red"
GROUP BY 
	1
HAVING 
	COUNT(f.event_id) >= 3;
-- Miranda Priestly



