import azure.mgmt.resourcegraph as arg
import json
import math
from pandas import json_normalize
from tqdm import tqdm
from azure.mgmt.resource import SubscriptionClient
from azure.identity import AzureCliCredential
from colorama import init, Fore, Back, Style
import pyfiglet
from argparse import ArgumentParser
from prettytable import PrettyTable


init(autoreset=True)
outputfilename="sokqlovia_output.csv"


def getresources( strQuery ):
    # Get your credentials from Azure CLI (development only!) and get your subscription list
    print("\nLaunching Query")
    credential = AzureCliCredential()
    subsClient = SubscriptionClient(credential)
    subsRaw = []
    for sub in subsClient.subscriptions.list():
        subsRaw.append(sub.as_dict())
    subsList = []
    for sub in subsRaw:
        subsList.append(sub.get('subscription_id'))

    # Create Azure Resource Graph client and set options
    argClient = arg.ResourceGraphClient(credential)
    argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray")

    # Create query
    argQuery = arg.models.QueryRequest(subscriptions=subsList, query=strQuery, options=argQueryOptions)

    # Run query
    argResults = argClient.resources(argQuery)

    print("Results Found: " + str(argResults.total_records))
    print("Return Count: " + str(argResults.count))
    print("Results Trucated:" + str(argResults.result_truncated))
    print("Skip Token: " + str(argResults.skip_token))
    query_num = (math.ceil(argResults.total_records/argResults.count))
    print("Queries Needed: " + str(query_num))
    orderstring = "order by"
    if orderstring in strQuery or query_num==1:
        sf = 1
    else:
        if input((Style.BRIGHT + Back.YELLOW + Fore.RED + "[WARNING] Query will be executed in multiple parts. 'order by' operator not found in query. Recommend terminating script (Y/N)")) == "y":
            exit()

    print("###################################\n")
    # pandas test

    json_a = json.dumps(argResults.data)
    json_b = json.loads(json_a)
    df_full = json_normalize(json_b)
    d = 1
    #print(d)
    newval=1000
    while argResults.skip_token:
        for d in tqdm(range(query_num)):
            argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray", skip_token=argResults.skip_token, skip=newval)
            argQuery = arg.models.QueryRequest(subscriptions=subsList, query=strQuery, options=argQueryOptions)
            argResults = argClient.resources(argQuery)
            json_a = json.dumps(argResults.data)
            json_b = json.loads(json_a)
            df = json_normalize(json_b)
            df_full = df_full.append(df)
            d += 1
            newval+= 1000
            #print(d)
    print("Data Preview")
    print(df_full)
    df_full.to_csv(outputfilename, index=False)


def compulsary_ascii():
    ascii_banner = pyfiglet.figlet_format("Sokqlovia")
    print(ascii_banner)


def testquery():
    getresources(
        "Resources | where type =~ 'Microsoft.Compute/virtualMachines' | project id, name, location, resourceGroup, properties.storageProfile.osDisk.osType | order by id asc")

def display_stored():
    x = PrettyTable()
    x.field_names = ["QueryID","QueryName","ShortDescription","PositionalArg","KQL"]
    f = open("stored_queries.json")
    data = json.load(f)
    for i in data['queries']:
        x.add_row([i['QueryID'], i['QueryName'], i['ShortDescription'],i['PositionalArg'], i['KQL']])
    #     #print(i)
    f.close()
    print(x)

def savedqueryexec(id,param):
    f = open("stored_queries.json")
    data = json.load(f)
    curr = 0
    for i in data['queries']:
        if i['QueryID'] == id:
            #i['QueryID'], i['QueryName'], i['ShortDescription'],i['PositionalArg'], i['KQL']
            # if it has a positional argument - need to check if one was provided
            if i['PositionalArg'] == "Y":
                if param == "zttz":
                    print(Style.BRIGHT + Back.YELLOW + Fore.RED + "[Error] Positional Argument Expected with -p")
                    exit()
                else:
                    #replace holder with arg <sokqlovia>
                    query = i['KQL']
                    print(query)
                    query = query.replace("<sokqlovia>",param)
                    print(query)
                    getresources(query)
            # since no positional arg needed - kick of normal query
            else:
                getresources(i['KQL'])

        else:
            if (curr+1) == len(i):
                print(Style.BRIGHT + Back.YELLOW + Fore.RED + "[Error] Unable to find matching template (run -d)")
            curr += 1

def argparsing():
    compulsary_ascii()
    parser = ArgumentParser()
    parser.add_argument("-x", help="Demo Query. i.e. outputs results of query saved in testquery()",
                        action="store_true",required=False)
    parser.add_argument("-o", dest="outfile", help="Override default output file/path. Default is sokqlovia_output.csv in cwd",
                        required=False)
    parser.add_argument("-c", dest="custom_query", help="Quote encapsulated KQL query to be executed", required=False)
    parser.add_argument("-d", help="Displays List of Pre-define templates for use with -t flag",
                        action="store_true", required=False)
    parser.add_argument("-s", dest="saved_query", help="Select Saved Query by ID, provide param -p for positional argument", required=False)
    parser.add_argument("-p", help="Parameter needed. Used in conjuction with -S", required=False)

    args = parser.parse_args()
    if args.outfile:
        outputfilename = args.outputdir

    if args.x:
        testquery()

    if args.custom_query:
        getresources(args.custom_query)

    if args.saved_query:
        if args.p:
            tmp = (args.p)
        else:
            tmp = "zttz"
        savedqueryexec(args.saved_query,tmp)

    if args.d:
        print("\n Typical Usage: soklovia.py -s <QueryID> -p <positional_arg>\n")
        display_stored()


if __name__ == '__main__':
    argparsing()


