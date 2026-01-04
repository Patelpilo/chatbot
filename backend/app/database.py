from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:i wan to27017"

def _make_mock_collection():
    class MockCollection:
        def __init__(self):
            self._docs = {}
            self._id = 1
            self.name = "mock_collection"
            class _DB:
                def __init__(self, name):
                    self.name = name
            self.database = _DB("mockdb")

        def insert_one(self, doc):
            doc_id = self._id
            self._id += 1
            doc_copy = dict(doc)
            doc_copy["_id"] = doc_id
            self._docs[doc_id] = doc_copy
            class _Res:
                pass
            r = _Res()
            r.inserted_id = doc_id
            return r

        def find_one(self, query):
            for d in self._docs.values():
                match = True
                for k, v in query.items():
                    if d.get(k) != v:
                        match = False
                        break
                if match:
                    return d
            return None

        def insert_many(self, docs):
            ids = []
            for doc in docs:
                ids.append(self.insert_one(doc).inserted_id)
            class _R:
                pass
            r = _R()
            r.inserted_ids = ids
            return r

        def find(self, query):
            results = []
            for d in self._docs.values():
                match = False
                if "$or" in query:
                    for cond in query["$or"]:
                        submatch = True
                        for k, v in cond.items():
                            if d.get(k) != v:
                                submatch = False
                                break
                        if submatch:
                            match = True
                            break
                else:
                    match = True
                    for k, v in query.items():
                        if d.get(k) != v:
                            match = False
                            break
                if match:
                    results.append(d)

            class _Cursor(list):
                def sort(self, field, direction):
                    reverse = direction == -1
                    return sorted(self, key=lambda x: x.get(field), reverse=reverse)

            return _Cursor(results)

    return MockCollection()

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.admin.command("ping")
    print("CONNECTED DATABASES:", client.list_database_names())

    db = client["whatsease"]
    users_collection = db["users"]
    messages_collection = db["messages"]
except Exception as e:
    print("WARNING: Could not connect to MongoDB at", MONGO_URI, "— falling back to in-memory mock DB. Error:", e)
    users_collection = _make_mock_collection()
    messages_collection = _make_mock_collection()
