from gpapi.googleplay import GooglePlayAPI, RequestError
from time import sleep
import json, re, os, pymongo

mail = "item084.dev@gmail.com"
passwd = "devdevdev@GG"

api = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename="hero2lte")
api.login(email=mail, password=passwd)

cat = "MUSIC_AND_AUDIO"
catList = ['apps_topselling_free', 'apps_topgrossing', 'apps_movers_shakers', 'apps_topselling_paid']
#api.list(cat)
# print(catList)
#for c in catList:
#    print(c)

# limit = 100

cats = [
    "Art & Design",
    "Auto & Vehicles",
    "Beauty",
    "Books & Reference",
    "Business",
    "Comics",
    "Communication",
    "Dating",
    "Education",
    "Entertainment",
    "Events",
    "Family",
    "Finance",
    "Food & Drink",
    "Games",
    "Health & Fitness",
    "House & Home",
    "Libraries & Demo",
    "Lifestyle",
    "Maps & Navigation",
    "Medical",
    "Music & Audio",
    "News & Magazines",
    "Parenting",
    "Personalization",
    "Photography",
    "Productivity",
    "Shopping",
    "Social",
    "Sports",
    "Tools",
    "Travel & Local",
    "Video Players & Editors",
    "Wear OS by Google",
    "Weather",
]

def cats():
    # print("\nBrowse play store categories\n")
    d = {}
    browse = api.browse()
    for cat in browse.get("category"):
        catid = cat["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
        catList = api.list(catid)
        # print(c["name"])
        d[catid] = {"name": None, "list": None}
        d[catid]["name"] = cat["name"]
        d[catid]["list"] = catList
    stringfy = json.dumps(d)
    with open('categories.json', 'w+') as f:
        f.write(stringfy+'\n')

def conn():
    """Mongo DB connection."""
    while True:
        try:
            server = "duke.eecs.umich.edu:27017/?ssl=true"
            user = "kelyao" #input("Username: ")
            password = "happy0416!MG" # getpass.getpass()
            url = "mongodb://{}:{}@{}".format(user, password, server)
            client = pymongo.MongoClient(url)
            print(client.list_database_names())
        except pymongo.errors.OperationFailure:
            print("Authentication failed.")
        else:
            print("Connected:", url)
            break
    return url, client


def download():
    _, client = conn()
    db = client.MobiPurposeDB
    names = db.list_collection_names()
    cnt = 0
    with open("all.txt", "w+") as f:
        for name in names:
            print(name)
            for i, doc in enumerate(db[name].find()):
                data = doc.get("id")
                cnt+=1
                if data is None:
                    continue
                f.write(data+'\n')
    print(cnt)

def upload():
    _, client = conn()
    db = client.MobiPurpose
    col = db.GooglePlayApps_3
    col.create_index([('id', pymongo.ASCENDING)], unique=True)
    with open("all.txt", "r") as f:
        for line in f:
            try:
                col.insert({"id": line.rstrip('\n')})
            except:
                pass

def fetch(cat, catlist):
    #cat = "MUSIC_AND_AUDIO"
    #catList = ['apps_topselling_free']#, 'apps_topgrossing', 'apps_movers_shakers', 'apps_topselling_paid']



    #try:
    #    os.mkdir("result/" + cat)
    #except:
    #    pass

    _, client = conn()
    db = client.MobiPurposeDB
    col = db[cat]
    col.create_index([('id', pymongo.ASCENDING)], unique=True)
    d = []
    #d.append({"id": "docid"})
    #exit()
    for sub in catList:
        d = []
        #cnt = 0
        try:
            for app in api.list_all(cat, sub): #, limit, 10000):
                #d.append({"id": app["docid"]})
                try:
                    col.insert({"id": app["docid"]})
                    print(app["docid"])
                except pymongo.errors.DuplicateKeyError:
                    pass
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            pass
        #col.insert_many(d)


if __name__ == "__main__":

    d = {}
    with open('categories.json', 'r') as f:
        d = f.read()
    d = json.loads(d)
    for cat in d:
        print(cat, d[cat]["list"])
        fetch(cat, d[cat]["list"])

    exit()
    upload()
    exit()
    browse = api.browse()
    for c in browse.get("category"):
        print(c["name"])

    sampleCat = browse["category"][0]["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
    browseCat = api.home(cat=sampleCat)
    print(browseCat)

    exit()







"""
    _, client = conn()
    db = client.MobiPurpose
    col = db[cat]
    col.create_index([('id', pymongo.ASCENDING)], unique=True)
    exit()
    d = []
    for sub in catList:
        d = []
        #cnt = 0
        with open('result/{}/{}.txt.temp'.format(cat, sub), 'w+') as f:
            try:
                for app in api.list_iter(cat, catList[0]): #, limit, 10000):
                    app = app["docid"]
                    #print(app)
                    #if app in d:
                    #    cnt += 1
                    #    print(cnt)
                    #    continue
                    #d[app] = None
                    f.write(app+'\n')
            except Exception as e:
                traceback.print_exc(e)
                pass
        col.insert_many(d)
"""



# appList = api.list_iter(cat, catList[0], limit, 12)

exit()

#for app in appList:
#   app = app["docid"]
#    d[app] = None
#    print(app)
#print(len(d))
#"https://android.clients.google.com/fdfe/"
#s = re.search(r"nextPageUrl(.*?)[\r\n]",str(data)).group()
#print(s)#str(data)[s:s+120])
# print(data.payload.listResponse.doc[0].child)#.containerMetadata.nextPageUrl)

limit = 100
d = {}
for i in range(0, 7):
    if i % 10 == 0:
        print(i // 10)
    with open('apps_topselling_free.txt', 'w+') as f:
    #print("\nList only {} apps from subcat {} for {} category\n".format(
    #    limit, catList[0], cat))
        appList = api.list(cat, catList[0], limit, i * (limit))
        for app in appList:
            app = app["docid"]
            #print(app)
            if app in d:
                continue
            d[app] = None
            f.write(app+'\n')
            # print(app["docid"])
    # sleep(0.3)
print(len(d))

exit()


# BROWSE
print("\nBrowse play store categories\n")
browse = api.browse()
for c in browse.get("category"):
    print(c["name"])

sampleCat = browse["category"][0]["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
print("\nBrowsing the {} category\n".format(sampleCat))
browseCat = api.home(cat=sampleCat)

for doc in browseCat:
    if 'docid' in doc:
        print("doc: {}".format(doc["docid"]))
    for child in doc["child"]:
        print("\tsubcat: {}".format(child["docid"]))
        for app in child["child"]:
            print("\t\tapp: {}".format(app["docid"]))

