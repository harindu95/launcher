history= None
def get_history():
    global history
    import sqlite3
    conn = sqlite3.connect('/home/harindu/.mozilla/firefox/rq8cz875.default/places.sqlite')
    cursor = conn.cursor()
    query = 'select p.url,p.title from moz_historyvisits as h, moz_places as p where p.id == h.place_id order by h.visit_date desc;'
    query2 = 'select p.title from moz_historyvisits as h, moz_places as p where p.id == h.place_id order by h.visit_date desc;'
    history = list(cursor.execute(query))[:400]

    conn.close()
    
def checkTerms(terms,txt):
    for term in terms:
        if not term in txt:
            return False
    return True

def query(w,txt):
    txt = txt.lower()
    terms = txt.split(' ')
    results = []
    if history  == None:
        get_history()
    for line in history:
        try:
            if w.wk1.terminate:
                break
        except AttributeError:
            pass
        info = (line[1] or '' )+ (line[0] or '')
        if checkTerms(terms,info.lower()) :
            results.append({'Name':line[1] or '' ,'Comment':line[0] or '' ,'Icon':'firefox','Type':'firefox'})

    return results

def execute(url):
    import os
    cmd = 'nohup firefox --new-tab ' + url['Comment'] + ' &'
    os.system(cmd)

# get_history()
# print history
