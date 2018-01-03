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
            subdomain = post['domain']['prefix']
            if subdomain not in summary:                
                summary[subdomain] = { "upvote":0, "downvote": 0 }
            
            rating = int(post['rating'])
            if rating >= 0 :
                summary[subdomain]['upvote'] += rating
            else:
                summary[subdomain]['downvote'] += rating

        page += 1
    
    for key, value in summary.items():
        print("|{:20}| total {:>5d}| upvotes {:>5d}| downvotes {:>5d}|".format(key, value['upvote'] + value['downvote'], value['upvote'], value['downvote']))

def comments(target):
    summary = {}

    page = 1
    while True:
        resp = requests.get("https://d3.ru/api/users/{}/comments/?page={};per_page=42".format(target, page))
        body = resp.json()

        if not body['comments']:
            break

        for comment in body['comments']:
            subdomain = comment['domain']['prefix']
            if subdomain not in summary:                
                summary[subdomain] = { "upvote":0, "downvote": 0 }
            
            rating = int(comment['rating'])
            if rating >= 0 :
                summary[subdomain]['upvote'] += rating
            else:
                summary[subdomain]['downvote'] += rating

        page += 1

    for key, value in summary.items():
        print("|{:20}| total {:>5d}| upvotes {:>5d}| downvotes {:>5d}|".format(key, value['upvote'] + value['downvote'], value['upvote'], value['downvote']))

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='PyScript I will tell you who is your friend')
    parser.add_argument('target', help = 'login you are interested in')

    ARGS = parser.parse_args()

    print("{:_^67}".format("Banned at subdomains"))
    bans(ARGS.target)

    print("{:_^67}".format("Owned subdomains"))
    domains(ARGS.target)

    print("{:_^67}".format("Rating by posts"))
    posts(ARGS.target)

    print("\n{:_^67}".format("Rating by comments"))
    comments(ARGS.target)
    print("{:_<67}\n".format(""))
