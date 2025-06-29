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

# allow pull payments with unique IDs. When doing a pull, you specify the pre-auth ID. 

pull_id1=stk.allow(alan, 10, USD, per_day=1)  # alan can spend from my account 10 USD/ day at most. I'll get a push notice if he goes over.
stk.allow(alan, 50, USD, per_day=7)  # alan can spend up to $50/week. This replaces 
stk.allow(alan, 100, USD, use_count=10)    # allow limit of 10 pulls, up to $100 total.
stk.allow(alan, 100, USD)                   # simplest; just authorize $100 USD
stk.revoke(id1)    # revoke the grant
# note all allows are independent and can be remvoked at any time

stk.allow(hotel_california, 300, USD, guarantee_time=3)  # hotel can pull up to $300 over the next 3 days and I can't cancel

# do a pull payment
stk.pull(pull_id4, 5, USD, "dinner reimbursement")  # pull preauthorized fudns

stk.request_auth(alan, 5, USD)   # request an authID from alan so can pull 5 USD

stk.requet_payment(alan, 10, USD)   # make a simple payment request. Will be pushed to mobile app.

# get recovery file
stk.get_recovery_data()

# initiaate account recovery using recovery data and biometric scan
stk=Account(recovery_data, biometric_token)   # get my account back based on the recovery file and a recent biometric scan

# do an atomic swap
swap_id=stk.swap(alan, 5, USD, 4.5, EUR, 100)   # offer to swap my USD for alan's EUR. Offer good for 100 seconds.
stk.revoke(swap_id)         # revoke my swap offer

# pairing request from new device. Need only do this once per new device
pair(stk, credential)  # this will authorize our device's credential
stk.request_auth

# PII management
stk.set_data(dict)   # add dict to store on server. Will be encrypted using the encryption key shared between user devices
stk.get_data("home", "zipcode")  # get element at hierarchy which could be a dict

### to be added

## Note: we get a signed auth to deduct fees from the account 

stk.swap(5, USD, receive=EUR)   # turn 5 USD to EUR at the market price

stk.send(alan, 5, EUR)          # if have EUR, send them. Otherwise, convert from default currency to EUR and send

stk.notify(pull_id)         # if someone attempts a pull, notify my mobile device so I can manually approve it.

stk.create_escrow("vax_bet", sides=("yes", "no", "maybe"))  # create a betting pool
alan.send_escrow(5, USD)    # place bet
stk.settle_escrow("vax bet", (("yes", .3), ("no", .2), ()"maybe", .5))  # settle the bet
