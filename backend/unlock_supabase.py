import psycopg2
url = "postgresql://postgres.vsvcypedaemkwcbfswvl:Arun%402007%2312@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres?sslmode=require"
try:
    conn = psycopg2.connect(url)
    c = conn.cursor()
    c.execute("INSERT INTO allowed_networks (subnet, description) VALUES ('0.0.0.0/0', 'Global Unlock');")
    conn.commit()
    conn.close()
    print("Unlocked successfully")
except Exception as e:
    print("Error:", e)
