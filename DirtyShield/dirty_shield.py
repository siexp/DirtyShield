#!/usr/bin/env python

"""
PyScript that gather information about given user
"""
import argparse
import requests

def bans(target):
    resp = requests.get("https://d3.ru/api/users/{}/bans/".format(target))
    body = resp.json()

    for ban in body['bans']:
        subdomain = ban['domain']['prefix'].encode('utf-8').strip()
        moderator = ban['moderator']['login'].encode('utf-8').strip()
        reason = ban['reason'].encode('utf-8').strip()
        print("{:20} by {:16} for '{}'".format(subdomain.decode('utf-8'), moderator.decode('utf-8'), reason.decode('utf-8')))

    print("{:=<52}".format(""))

def domains(target):
    resp = requests.get("https://d3.ru/api/users/{}/domains/".format(target))
    body = resp.json()
    
    for domain in body['domains']:
        title = domain['title'].encode('utf-8').strip()
        print("{:20}".format(title.decode('utf-8')))
    
    print("{:=<52}".format(""))

"""
Goes throughout target's posts or comments and collects information about upvotes and downvotes 
"""
def traverse(target,trace):
    summary = {}

    page = 1
    while True:
        resp = requests.get("https://d3.ru/api/users/{}/{}/?page={};per_page=42".format(target, trace, page))
        body = resp.json()

        if not body[trace]:
            break

        for post in body[trace]:
            if 'is_hidden' in post:
                continue

            subdomain = post['domain']['prefix'].encode('utf-8').strip()
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


def printHeader(title):
    print("{:_^52}".format(title))
    print("|{:^20}|{:^9}|{:^9}|{:^9}|".format("SUBDOMAIN","TOTAL", "UPVOTE", "DOWNVOTE"))

def printData(summary):
    for key, value in summary:
        if value['upvote'] != 0 or value['downvote'] != 0:
            print("|{:20}| {:>8d}| {:>8d}| {:>8d}|".format(key.decode('utf-8'), value['upvote'] + value['downvote'], value['upvote'], value['downvote']))

def printSummary(summary, title):
    if len(summary) == 0:
        return

    printHeader(title)
    
    orderedByTotal = sorted( summary.items(), key = lambda item: item[1]['upvote'] + item[1]['downvote'], reverse=True)
    printData(orderedByTotal)
    
    print("{:=<52}\n".format(""))

def printTop5(summary, title):
    if len(summary) == 0:
        return

    printHeader(title + ": best")
    best = sorted( summary.items(), key=lambda item: item[1]['upvote'], reverse=True )[:5]
    printData(best)

    printHeader(title + ": worst")
    worst = sorted( summary.items(), key=lambda item: item[1]['downvote'] )[:5]
    printData(worst)
    
    print("{:=<52}".format(""))

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='PyScript I will tell you who is your friend')
    PARSER.add_argument('target', help = 'login you are interested in')
    PARSER.add_argument('--full', help = 'Print full statistics', action = "store_true")

    ARGS = PARSER.parse_args()

    if ARGS.full:
        print("{:_^52}".format("Owned subdomains"))
        domains(ARGS.target)

    print("{:_^52}".format("Banned at subdomains"))
    bans(ARGS.target)
    
    printFlavor = printTop5
    if ARGS.full:
        printFlavor = printSummary
        
    summary = traverse(ARGS.target, "posts")
    printFlavor(summary, "Rating by Posts")

    summary = traverse(ARGS.target, "comments")
    printFlavor(summary, "Rating by comments")