# creation credentials
DEPLOYER=PJCLRFRILMQO6XDZVEDB7WYGGKOV7NBURQ3BNS477DEOA5S2OQWJCAC2LU
REWARDS_CREATOR=PJCLRFRILMQO6XDZVEDB7WYGGKOV7NBURQ3BNS477DEOA5S2OQWJCAC2LU
COLLECTION_CREATOR=ZPWXNFCQBT4ZDVEN5OJDTTGJIKQHT4JOEYTDHNQ2JGELNYOAIWVVE4JJBA
CLIENT=CKG27NSKL2TBOD7XTTO5NALZGH2YDD2YJMFY7LFTJFHOJPCHMYSMMPTDSM

# pool living time
BEGIN_TIMESTAMP=$(date --date="2 minutes" +"%s")
END_TIMESTAMP=$(date --date="1 hour" +"%s")

# pool fixed rate
FIXED_RATE=100

# total rewards created
REWARD_TOTAL=100
DECIMALS=0 # must be equal to the log in base 10 of the reward_total