
myquery = { "address": "Park Lane 38" }

# Execute the query
docs = collection.find(myquery)

# Iterate over results
for x in docs:
    print(x)
