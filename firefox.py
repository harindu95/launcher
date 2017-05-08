import applications
history= None
def get_history():
    global history
    import sqlite3
    conn = sqlite3.connect('/home/harindu/.mozilla/firefox/rq8cz875.default/places.sqlite')
    cursor = conn.cursor()
    query = 'select p.url from moz_historyvisits as h, moz_places as p where p.id == h.place_id order by h.visit_date desc;'
    history = list(cursor.execute(query))[:200]

    conn.close()
    
def checkTerms(terms,txt):
    for term in terms:
        if not term in txt:
            return False
    return True

def query(txt):
    txt = txt.lower()
    terms = txt.split(' ')
    results = []
    if history  == None:
        get_history()
    for line in history:
        if checkTerms(terms,str(line[0]).lower()) :
            results.append({'Name':line[0],'Comment':'','Icon':applications.icon_fullpath('firefox'),'Type':'firefox'})

    return results

def execute(url):
    import os
    cmd = 'nohup firefox --new-tab ' + url['Name'] + ' &'
    os.system(cmd)
