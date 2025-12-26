queries = {
    # invoice_reports
    'last_glh': '''
    SELECT DISTINCT vehicle_id
    FROM vehicle_last_geometris_location_history 
    WHERE date >= {0}
    ORDER BY vehicle_id ASC;
    ''',
    'companies': '''
    SELECT companyName
    FROM companies 
    WHERE companyName NOT LIKE 'Mobile Test Company'
    ORDER BY companyName ASC;
    ''',
    'glh_static': '''
    SELECT g.eldSerialNum, g.vehicle_id, v.vehicleId as vehicle_name, c.companyName, count(g.id) as counter
    FROM geometris_location_history_static g 
    JOIN vehicles v 
        ON g.vehicle_id = v.id
    JOIN companies c
        ON v.companyId = c.id
    WHERE g.vehicle_id = {0}
    AND g.date BETWEEN {1} AND {2}
    AND g.type LIKE "ON_PERIODIC"
    GROUP BY g.eldSerialNum
    ORDER BY g.date ASC;
    ''',
    'tx_sa_history': '''
    SELECT id
    FROM super_action_history
    WHERE vehicle_id = {0}
    AND dateTime BETWEEN {1} AND {2}
    AND vehicle_id IS NOT NULL
    AND action NOT IN (
        "FILL_IN",
        "CERTIFY",
        "REQUESTED_DRIVER_PHONE_NUM",
        "FORCE_LOGOUT",
        "CANCEL_LOG_EDIT"
        )
    LIMIT 1; 
    ''',
    'enterprise_sa_history': '''
    SELECT id
    FROM super_action_history
    WHERE vehicle_id = {0}
    AND dateTime BETWEEN {1} AND {2}
    AND vehicle_id IS NOT NULL
    AND action NOT IN (
        "FILL_IN",
        "CERTIFY",
        "REQUESTED_DRIVER_PHONE_NUM",
        "FORCE_LOGOUT",
        "CANCEL_LOG_EDIT",
        "DELETE_OF_UD",
        "SUPER_UD_ASSIGN",
        "ANNOTATE_UD",
        "CONVERT_ANNOTATED_UD_TO_ACTIVE",
        "CREATE_UD_FROM_LH",
        "EDIT_UD"
        )
    LIMIT 1;
    ''',
    'active_gps': '''
    SELECT COUNT(id) 
    FROM gps 
    WHERE status LIKE 'ACTIVE';
    ''',

    # vehicle_last_glh
    'daily_vehicle_last_glh': '''
    SELECT g.*, v.vehicleId
    FROM vehicle_last_geometris_location_history g
    JOIN vehicles v 
	    ON g.vehicle_id = v.id
    WHERE date >= {0}
    ORDER BY id ASC;
    ''',
    'daily_sa_history': '''
    SELECT * 
    FROM super_action_history
    WHERE dateTime >= {0}
    ORDER BY id ASC;
    ''',
    'fake_lh_data_insert': '''
    INSERT INTO vehicle_last_geometris_location_history
    (bearing, timeZoneOffset, date, eldSerialNum, engineHours, fuel, geoCodedLocation, latitude, longitude, distance,
     odometer, rpm, speed, state, totalFuelUsed, type, uniqueId, vin, vinRaw, vehicle_id)
    VALUES (%(bearing)s, %(timeZoneOffset)s, %(date)s, %(eldSerialNum)s, %(engineHours)s, %(fuel)s,
     %(geoCodedLocation)s, %(latitude)s, %(longitude)s, %(distance)s, %(odometer)s, %(rpm)s, %(speed)s, %(state)s,
      %(totalFuelUsed)s, %(type)s, %(uniqueId)s, %(vin)s, %(vinRaw)s, %(vehicle_id)s)
     ''',
    'fake_sa_history_insert': '''
    INSERT INTO super_action_history
    (action, dateTime, eventDate, toolsUser, driver_id, superUser_id, vehicle_id)
    VALUES (%(action)s, %(dateTime)s, %(eventDate)s, %(toolsUser)s, %(driver_id)s, %(superUser_id)s, %(vehicle_id)s)
    ''',

    # billing_check
    'drivers': '''
    SELECT d.id, CONCAT(d.firstName, " ", d.lastName) AS name, c.companyName
    FROM drivers d
    JOIN companies c 
        ON d.companyId = c.id
    WHERE CONCAT(d.firstName, " ", d.lastName) IN ({0})
    AND d.createdOn BETWEEN 1759381200000 AND 1761973200000
    ORDER BY c.companyName, name ASC
    ''',
    'driver_events': '''
    SELECT driver_id, vehicle_id
    FROM driver_events 
    WHERE driver_id = {0}
    AND start BETWEEN 1759381200000 AND 1761973200000
    GROUP BY vehicle_id
    ORDER BY driver_id;
    ''',
    'glh_billing': '''
    SELECT g.eldSerialNum, g.vehicle_id, v.vehicleId as vehicle_name, e.originationDate
    FROM geometris_location_history_static g 
    JOIN vehicles v 
        ON g.vehicle_id = v.id
    JOIN elds e 
        ON g.eldSerialNum = e.serialNum
    WHERE g.vehicle_id = {0}
    AND g.date BETWEEN 1759381200000 AND 1761973200000
    AND g.type LIKE "ON_PERIODIC"
    GROUP BY g.eldSerialNum
    ORDER BY g.date ASC;
    ''',
    'activity_history': '''
    SELECT *
    FROM super_admin_activities
    WHERE attributeType LIKE 'ELD_COMPANY'
    AND date BETWEEN 1759381200000 AND 1761973200000
    AND asset like '{0}'
    AND updatedValue LIKE '{1}';
    ''',
    'sa_billing': '''
    (SELECT driver_id, vehicle_id, dateTime 
    FROM super_action_history
    WHERE driver_id = {0}
    AND vehicle_id = {1}
    AND dateTime BETWEEN 1759381200000 AND 1761973200000
    AND action NOT IN (
    "FILL_IN",
    "CERTIFY",
    "REQUESTED_DRIVER_PHONE_NUM",
    "FORCE_LOGOUT",
    "CANCEL_LOG_EDIT",
    "DELETE_OF_UD",
    "SUPER_UD_ASSIGN",
    "ANNOTATE_UD",
    "CONVERT_ANNOTATED_UD_TO_ACTIVE",
    "CREATE_UD_FROM_LH",
    "EDIT_UD"
    )
    AND vehicle_id IS NOT NULL
    ORDER BY dateTime ASC
    LIMIT 1)
    
    UNION ALL
    
    (SELECT driver_id, vehicle_id, dateTime 
    FROM super_action_history
    WHERE driver_id = {0}
    AND vehicle_id = {1}
    AND dateTime BETWEEN 1759381200000 AND 1761973200000
    AND action NOT IN (
    "FILL_IN",
    "CERTIFY",
    "REQUESTED_DRIVER_PHONE_NUM",
    "FORCE_LOGOUT",
    "CANCEL_LOG_EDIT",
    "DELETE_OF_UD",
    "SUPER_UD_ASSIGN",
    "ANNOTATE_UD",
    "CONVERT_ANNOTATED_UD_TO_ACTIVE",
    "CREATE_UD_FROM_LH",
    "EDIT_UD"
    )
    AND vehicle_id IS NOT NULL
    ORDER BY dateTime DESC
    LIMIT 1);
    ''',
}
