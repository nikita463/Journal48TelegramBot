from api.typings import File

jsFile = {
    "filename": "name",
    "link": "link"
}

file = File(**jsFile)

print(file)
