import argparse
import collections
import logging
import requests

Auth = collections.namedtuple('Auth', 'uid sid')

def authenticate( login, password ):
    auth = { "username": login, "password": password }
    resp = requests.post( "https://dirty.ru/api/auth/login/", auth )

    body = resp.json()

    #if body[ 'status' ] == 'error':
    #    raise Exception( body['errors'][0]['description'] )

    return Auth( uid = body[ 'uid' ], sid = body[ 'sid' ] )

def bans( target ):
    resp = requests.get( "https://d3.ru/api/users/" + target + "/bans/" )
    body = resp.json()

    for ban in body['bans']:
        print( "Banned at {:10} by {:16} for '{}'".format( ban['domain']['prefix'], ban['moderator']['login'], ban['reason'] ) )

def domains( target ):
    resp = requests.get( "https://d3.ru/api/users/" + target + "/domains/" )
    body = resp.json()
    
    for domain in body['domains']:
        print( "Created {:10} subdomain".format( domain['title'] ) )

if __name__ == "__main__":
    logger = logging.getLogger('DirtyShield')
    logger.setLevel( logging.INFO )

    parser = argparse.ArgumentParser( description='PyScript I will tell you who is your friend' )


    # auth info
    parser.add_argument( 'login', help = 'your username' )
    parser.add_argument( 'password', help = 'your password' )

    # target
    parser.add_argument( 'target', help = 'login you are interested in' )

    args = parser.parse_args()

    logger.info( 'Gathering info' )
    auth = authenticate( args.login, args.password )
    #logger.info( "uid %s", auth.uid )
    #logger.info( "uid %s", auth.sid )

    bans( args.target )
    domains( args.target )

    logger.info( 'Done' )