source "$(dirname ${BASH_SOURCE[0]})/config.sh"

goal asset send -f $COLLECTION_CREATOR \
    -t $CLIENT \
    --assetid $STAKING_ASA_ID_0 \
    --amount 1

goal asset send -f $COLLECTION_CREATOR \
    -t $CLIENT \
    --assetid $STAKING_ASA_ID_1 \
    --amount 1

goal asset send -f $COLLECTION_CREATOR \
    -t $CLIENT \
    --assetid $STAKING_ASA_ID_2 \
    --amount 1