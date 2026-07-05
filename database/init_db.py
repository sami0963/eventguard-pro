# 🟢 بيانات تجريبية

c.execute("INSERT INTO events (title, location, date, type, crowd_level, traffic_needed) VALUES (?,?,?,?,?,?)",
("Amsterdam Marathon", "Amsterdam", "2026-07-10", "sport", 9, 1))

c.execute("INSERT INTO events (title, location, date, type, crowd_level, traffic_needed) VALUES (?,?,?,?,?,?)",
("Summer Festival", "Rotterdam", "2026-07-15", "festival", 8, 1))

c.execute("INSERT INTO jobs (company, description, location, date, workers_needed, source_link) VALUES (?,?,?,?,?,?)",
("City Council", "Traffic control needed", "Amsterdam", "2026-07-10", 12, "https://example.com"))

c.execute("INSERT INTO notifications (type, message) VALUES (?,?)",
("info", "EventGuard system initialized 🚦"))
