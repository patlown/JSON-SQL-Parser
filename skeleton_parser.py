
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""
import os
import sys
from json import loads
from re import sub


columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
This function parses files for the Bid relation of the db

"""
def bidParser(item,bidList):
    bid = item['Bids']
    for bid in item['Bids']:
        parsedBid = ""
        parsedBid += transformDttm(bid['Bid']['Time']) + columnSeparator
        parsedBid += transformDollar(bid['Bid']['Amount']) + columnSeparator
        parsedBid += bid['Bid']['Bidder']['UserID'] + columnSeparator
        parsedBid += item['ItemID'] + "\n"
        bidList.append(parsedBid)


def AuctionParser(item,auctionList):

    parsedAuction = item["ItemID"] + columnSeparator
    parsedAuction += item["Seller"]["UserID"] + columnSeparator
    if item.get("Description") is None:
        parsedAuction += "nullvalue" + columnSeparator
    else:
        parsedAuction += item["Description"] + columnSeparator
    parsedAuction += item["Currently"] + columnSeparator
    if item.get("Buy_Price") is None:
        parsedAuction += "nullvalue" + columnSeparator
    else:
        parsedAuction += item["Buy_Price"] + columnSeparator
    parsedAuction += item["First_Bid"] + columnSeparator
    parsedAuction += item["Number_of_Bids"] + columnSeparator
    parsedAuction += item["Started"] + columnSeparator
    parsedAuction += item["Ends"]  + "\n"

    auctionList.append(parsedAuction)

def writeFile(parsedString,filename):
    f = open(filename, "a+")
    f.write(parsedString)
    f.close()


def UserParser(item,userIDs,userList):
    # First check if the item has bids, if so, check the bidders and add users
    # we have not seen before
    if item.get("Bids") is not None:
        for bid in item['Bids']:
            parsedUser = ""
            if bid['Bid']['Bidder']['UserID'] not in userIDs:
                
                userIDs[bid.get("UserID")] = bid.get("UserID")
                
                parsedUser += bid['Bid']['Bidder']['UserID'] + columnSeparator
                parsedUser += bid['Bid']['Bidder']['Rating'] + columnSeparator
                if bid['Bid']['Bidder'].get('Location') is None:
                    parsedUser += "nullvalue" + columnSeparator
                else:
                    parsedUser += bid['Bid']['Bidder']['Location'] + columnSeparator
                if bid['Bid']['Bidder'].get('Country') is None:
                    parsedUser += "nullvalue" + "\n"
                else:
                    parsedUser += bid['Bid']['Bidder']['Country'] + "\n"
            userList.append(parsedUser)
    
    # now add seller of item to the string
    if item['Seller']['UserID'] not in userIDs:
        parsedUser = ""
        parsedUser += item['Seller']['UserID'] + columnSeparator
        parsedUser += item['Seller']['Rating'] + columnSeparator
        parsedUser += item['Location'] + columnSeparator
        parsedUser += item['Country'] + "\n"
        userList.append(parsedUser)


    return parsedUser

def itemIsParser(item,itemIsList):
    

    for category in item.get('Category'):
        parsedItemIs = ""

        parsedItemIs += item['ItemID'] + columnSeparator
        parsedItemIs += category + "\n"

        itemIsList.append(parsedItemIs)
    
def itemParser(item,itemList):
    parsedItem = ""
    parsedItem += item.get('ItemID') + columnSeparator
    parsedItem += item.get('Name') + "\n"

    itemList.append(parsedItem)

def categoryParser(item, categories, categoryList ):
    
    for category in item.get("Category"):
        parsedCategory = ""

        if category not in categories:
            categories[category] = category
            parsedCategory += category + "\n"
            categoryList.append(parsedCategory)




"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        parsedUsers = ""
        auctionList = list()
        itemIsList = list()
        userList = list()
        itemList = list()
        categoryList = list()
        bidList = list()
        categories = {}
        userIDs = {}
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            #pass each item to the bid parser if it has a bid
            #bid parser does file creation in its method
            if item['Bids'] is not None:
                bidParser(item,bidList)
            writeFile("".join(bidList),"Bid.dat")
                
            #create parsed auction string and write to file
            AuctionParser(item,auctionList)
            writeFile("".join(auctionList),"Auctions.dat")
            #create parsed users string and write to file
            parsedUsers += UserParser(item,userIDs,userList)
            writeFile("".join(userList),"Users.dat")
            # create itemIs data and pass to file
            itemIsParser(item,itemIsList)
            writeFile("".join(itemIsList), "ItemIs.dat")

            # create item data and write to file
            itemParser(item,itemList)
            writeFile("".join(itemList),"Item.dat")

            # create category data and write to file
            categoryParser(item,categories,categoryList)
            writeFile("".join(categoryList),"Category.dat")






            pass

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
