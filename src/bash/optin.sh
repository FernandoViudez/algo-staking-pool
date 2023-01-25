source "$(dirname ${BASH_SOURCE[0]})/config.sh"


goal asset optin -a $CLIENT \
    --assetid $STAKING_ASA_ID_0
goal asset optin -a $CLIENT \
    --assetid $STAKING_ASA_ID_1
goal asset optin -a $CLIENT \
    --assetid $STAKING_ASA_ID_2

goal asset optin -a $CLIENT \
    --assetid $REWARD_ASA_ID