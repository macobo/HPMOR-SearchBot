import re

def find_matches_naive(chapter, section):
    pattern = "\\b{}\\b".format(section)
    matches = lambda x: re.findall(pattern, x, flags=re.IGNORECASE)
    count = 0
    paragraphs = []
    for paragraph in chapter["contents"]:
        result = matches(paragraph)
        if result:
            count += len(result)
            paragraphs.append(paragraph)
    return paragraphs, count


def find_sections_naive(collection, section):
    result = {
        "total_count": 0,
        "chapters": []
    }
    for chapter in list(collection):
        matches, count = find_matches_naive(chapter, section)
        if count == 0: continue
        result["total_count"] += count
        result["chapters"].append({
            "chapter_no": chapter["chapter_no"],
            "title": chapter["title"],
            "matches": matches,
            "count": count
        })
    return result

def find_naive(section):
    from pymongo import MongoClient
    client = MongoClient()
    db = client.hpmor_database
    collection = list(db.chapters.find({}))
    #print(collection)
    return find_sections_naive(collection, section)

if __name__ == "__main__":
    from sys import argv
    from pprint import pprint
    results = find_naive(argv[1])
    #pprint(results)
    print(results["total_count"])