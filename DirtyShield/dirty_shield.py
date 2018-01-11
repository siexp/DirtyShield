"""
PyScript that gather information about given user
"""
import argparse
import requests

def bans(target):
    resp = requests.get("https://d3.ru/api/users/{}/bans/".format(target))
    body = resp.json()

    for ban in body['bans']:
        subdomain = ban['domain']['prefix']
        moderator = ban['moderator']['login']
        reason = ban['reason']
        print("{:20} by {:16} for '{}'".format(subdomain, moderator, reason))

def domains(target):
    resp = requests.get("https://d3.ru/api/users/{}/domains/".format(target))
    body = resp.json()
    
    for domain in body['domains']:
        print("{:20}".format(domain['title']))

def posts(target):
    summary = {}

    page = 1
    while True:
        resp = requests.get("https://d3.ru/api/users/{}/posts/?page={};per_page=42".format(target, page))
        body = resp.json()

        if not body['posts']:
            break

        for post in body['posts']:
            if 'is_hidden' in post:
                continue

            subdomain = post['domain']['prefix']
            if not subdomain:
                continue

            if subdomain not in summary:
                summary[subdomain] = { "upvote":0, "downvote": 0 }

            if post['rating'] != None:
                rating = int(post['rating'])
                if rating >= 0:
                    summary[subdomain]['upvote'] += rating
                else:
                    summary[subdomain]['downvote'] += rating

        page += 1
    return summary


def comments(target):
    summary = {}

    page = 1
    while True:
        resp = requests.get("https://d3.ru/api/users/{}/comments/?page={};per_page=42".format(target, page))
        body = resp.json()

        if not body['comments']:
            break

        for comment in body['comments']:
            if 'is_hidden' in comment:
                continue

            subdomain = comment['domain']['prefix']
            if not subdomain:
                continue

            if subdomain not in summary:
                summary[subdomain] = { "upvote":0, "downvote": 0 }

            if comment['rating'] != None:
                rating = int(comment['rating'])
                if rating >= 0:
                    summary[subdomain]['upvote'] += rating
                else:
                    summary[subdomain]['downvote'] += rating

        page += 1

    return summary

def printSummary(summary, title):
    print("{:_^52}".format(title))
    print("|{:20}{:10}{:10}{:10}|".format("SUBDOMAIN","TOTAL", "UPVOTE", "DOWNVOTE"))    
    print("{:=<52}".format(""))
    
    for key, value in summary.items():
        if value['upvote'] != 0 or value['downvote'] != 0:
            print("|{:20}| {:>8d}| {:>8d}| {:>8d}|".format(key, value['upvote'] + value['downvote'], value['upvote'], value['downvote']))
    
    print("{:=<52}\n".format(""))


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='PyScript I will tell you who is your friend')
    PARSER.add_argument('target', help = 'login you are interested in')

    ARGS = PARSER.parse_args()

    print("{:_^52}".format("Banned at subdomains"))
    bans(ARGS.target)

    print("{:_^52}".format("Owned subdomains"))
    domains(ARGS.target)
    
    summary = posts(ARGS.target)
    printSummary(summary, "Rating by Posts")

    summary = comments(ARGS.target)
    printSummary(summary, "Rating by comments")
