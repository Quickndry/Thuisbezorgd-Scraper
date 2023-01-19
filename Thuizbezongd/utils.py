import sqlite3


def get_links(province_name):
    import os.path

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "thuisbezongd.db")

    with sqlite3.connect(db_path) as db:
        curr = db.cursor()
        curr.execute("""SELECT PC_4 FROM netherlands_pc4 WHERE Provincie_name = ? COLLATE NOCASE""", (province_name,))
        api_links = []
        post_codes = [i[0] for i in curr.fetchall()]
        post_codes = post_codes
        [api_links.append(f"https://cw-api.takeaway.com/api/v33/restaurants?postalCode={code}&limit=0&isAccurate=true")
             for code in post_codes]
        return api_links

