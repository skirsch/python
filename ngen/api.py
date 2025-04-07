# can type into a python shell
from ngen import *    

credential=gen_secret()  # generate the device keypair used for signing
stk=Account(new=credential)   # create my account (do only once)

stk=link(credential)      # get an object linked to my account
stk.addBiometrics(biotoken)  # add for account recovery and to enable getting an alias (since guarantee uniqueness)
stk.setAlias("steve")  # register my account as "steve"
stk.getAddr(USD)   # get the address of smart contract to send USD into so we can fund it
alan=stk.lookup("alan")
stk.send(alan, 5, USD, "consuting services")    # simple payment

# allow pull payments
stk.allow(alan, 10, USD, 1)  # alan can spend from my account 10 USD/ day at most. I'll get a push notice if he goes over.
stk.allow(alan, 50, USD, 7)  # alan can spend up to $50/week. Whichever limits hits first disables further payments
stk.allow(alan, 100, USD)    # global total spend limit regardless of time
# note all the above limits can be changed at any time

# do a pull payment
stk.pull(alan, 5, USD, "dinner reimbursement")

stk.request_auth(alan, 5, USD)   # request an auth from alan

stk.requet_payment(alan, 10, USD)   # make a simple payment request. Will be pushed to mobile app.

# get recovery file
stk.get_recovery_data()

# initiaate account recovery using recovery data and biometric scan
stk=Account(recovery_data, biometric_token)   # get my account back based on the recovery file and a recent biometric scan

# do an atomic swap
swap_id=stk.swap(alan, 5, USD, 4.5, EUR, 100)   # offer to swap my USD for alan's EUR. Offer good for 100 seconds.
stk.revoke(swap_id)         # revoke my swap offer

# pairing request from new device. Need only do this once per new device
Pair(stk, credential)  # this will authorize our device

# PII management
stk.set_data(dict)   # add dict to store on server. Will be encrypted using the encryption key shared between user devices
stk.get_data("home", "zipcode")  # get element at hierarchy which could be a dict

### to be added
Ngen: we get auth to deduct fees

Revocable and irrevocable authorizations, e.g. hotel check-in, which is irrevocable for a certain number of days

Do an exchange at the market. Eg usd to eur.

Create a callback function for approving a payment Request once the user has created an preauth 

Initiate a cross border payment

