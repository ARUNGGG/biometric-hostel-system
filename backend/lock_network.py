import sqlite3
conn = sqlite3.connect('hostel_biometric.db')
conn.execute('DELETE FROM allowed_networks')
conn.execute('INSERT INTO allowed_networks (subnet, description) VALUES (\'192.168.250.0/24\', \'Fake Home\')')
conn.commit()
conn.close()
print('Successfully locked out localhost!')
