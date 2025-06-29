# TransferX API calls

USD='USD'

# create a seed if we don't have one already
seed=create_seed()

# or load my seed
seed=get_environment_variable("TRANSFERX_SEED")

# create a new user. Generates a unique GUID entry for "steve" mapping "steve" to the GUID (e.g., 10) and also establishing the first authorized signing key
steve=create_user("steve", seed)

steve.GUID    # returns my GUID

# if user is already created, we can instantiate an object for the user. Seed is optional and allows transactions to be initiated.
steve=get_user("steve", seed) 


steve.set_prop("home.phone", "+16503792008") # set my home phone
steve.get_prop("home") # get whole home address tree


steve.send("yobie", 5, USD, "thanks for the memories.")
steve.request("yobie", 5, USD, "you owe me from last thursday")

txn=steve.get_transaction()      # will block until a new txn is posted that happened after the call. Some will be pull requests. 
# The app can approve pull requests if pre-authorized in the app. 
# Generally, pre-authorized approvals will be stored in the public database, encrypted so only the user can access so if a user changes his provider, there is continuity.

# get list of transactions to show to user.
# transaction type will be auth_request, pull_request, receive_funds, send_funds, etc.
# this allows the mobile app to get a real-time feed of transactions to show to the user.
# also note when funds are sent, there is a real-time notification of that, even it the txn 
# will take seconds to confirm on the blockchain. 
txnlist=steve.get_txn_history(after_this_time)   

'''
stuff in the central database on per user basis

alias, e.g., stk (how people can refer to the user)
GUID, e.g., 10  (this is the recommended way to store someone's identity since aliases can change over time)
property list yaml file, e.g., name, address, phone, email, etc.
transaction history
public key so I can prove my identity
provider name, e.g., server to contact in order to contact that user
asset types and addresses held in the system (addresses stored here are all derived from the seed that is kept in user's app)
reputation
date joined
picture
user's name, e.g., Steve Kirsch
'''