

-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 -- check reports from that day from Chamberlin st.
SELECT * FROM interviews WHERE month >= 7 AND transcript LIKE "%courthouse%" -- get the three reports from after the date that mention the courthouse
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit" -- get all possible getaways
SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw" -- all suspected transactions
SELECT * FROM people JOIN (SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as suspected_calls ON suspected_calls.receiver = people.phone_number -- all people who received suspected phone calls
SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1 -- "the earliest flight out of Fiftyville tomorrow"
SELECT * FROM airports WHERE id = 4 -- find airport with ID 4
SELECT * FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id - passengers on suspect's getaway plane

-- people on the getaway plane
SELECT * FROM people JOIN
(SELECT * FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane
ON getaway_plane.passport_number = people.passport_number

-- people who both were on the getaway plane and made a suspicious phone call
SELECT * FROM
(SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as call_suspects
JOIN
(SELECT * FROM people JOIN (SELECT * FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane ON getaway_plane.passport_number = people.passport_number) as plane_suspects
ON
call_suspects.caller = plane_suspects.phone_number


-- people who were on the plane, made the calls and left the courthouse at the same time
SELECT * FROM
(SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit") as suspect_cars
JOIN
(SELECT * FROM
(SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as call_suspects
JOIN
(SELECT * FROM people JOIN (SELECT * FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane ON getaway_plane.passport_number = people.passport_number) as plane_suspects
ON
call_suspects.caller = plane_suspects.phone_number) as suspects
ON
suspects.license_plate = suspect_cars.license_plate

SELECT * FROM
people
JOIN
(SELECT * FROM bank_accounts
JOIN (SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw") as sus_trans
ON bank_accounts.account_number = sus_trans.account_number) as owners
ON owners.person_id = people.id -- people who withdrew money from the suspected ATM


SELECT * FROM
(SELECT * FROM
(SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit") as suspect_cars
JOIN
(SELECT * FROM
(SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as call_suspects
JOIN
(SELECT * FROM people JOIN (SELECT * FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane ON getaway_plane.passport_number = people.passport_number) as plane_suspects
ON
call_suspects.caller = plane_suspects.phone_number) as suspects
ON
suspects.license_plate = suspect_cars.license_plate) as sus4
JOIN
(SELECT * FROM bank_accounts
JOIN (SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw") as sus_trans
ON bank_accounts.account_number = sus_trans.account_number) as owners
ON owners.person_id = sus4.id


-- people who were on the plane, made the calls and left the courthouse at the same time
SELECT * FROM
	(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit") as suspect_cars
JOIN
	(SELECT * FROM
		(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as call_suspects
	JOIN
		(SELECT * FROM people
		JOIN
			(SELECT passport_number FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane
		ON getaway_plane.passport_number = people.passport_number) as plane_suspects
	ON
	call_suspects.caller = plane_suspects.phone_number) as suspects
ON
suspects.license_plate = suspect_cars.license_plate


-- people who were on the plane, made the calls and left the courthouse at the right time and withdrew money from ATM
SELECT * FROM
(SELECT * FROM
	(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit") as suspect_cars
JOIN
	(SELECT * FROM
		(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND year = 2020 AND duration < 60) as call_suspects
	JOIN
		(SELECT * FROM people
		JOIN
			(SELECT passport_number FROM (SELECT * FROM flights WHERE month = 7 AND day = 29 AND year = 2020 ORDER BY hour, minute LIMIT 1) as flight JOIN passengers ON flight.id = passengers.flight_id) as getaway_plane
		ON getaway_plane.passport_number = people.passport_number) as plane_suspects
	ON
	call_suspects.caller = plane_suspects.phone_number) as suspects
ON
suspects.license_plate = suspect_cars.license_plate) as sus4
JOIN
(SELECT * FROM bank_accounts
JOIN (SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND month = 7 AND day = 28 AND year = 2020 AND transaction_type = "withdraw") as sus_trans
ON bank_accounts.account_number = sus_trans.account_number) as owners
ON owners.person_id = sus4.id
