goal clerk send -f $DEPLOYER \
    -t $APP_ADDR \
    -a 301000 \
    -o minbal.txn

# here goes all ASAs that can be staked (and the Reward asa too)
goal app method --app-id $APP_ID \
    -f $DEPLOYER \
    --on-completion "NoOp" \
    --method "init(pay,asset)void" \
    --arg minbal.txn \
    --arg $REWARD_ASA_ID

goal app method --app-id $APP_ID \
    -f $DEPLOYER \
    --on-completion "NoOp" \
    --method "init(pay,asset)void" \
    --arg minbal.txn \
    --arg $STAKING_ASA_ID_0

goal app method --app-id $APP_ID \
    -f $DEPLOYER \
    --on-completion "NoOp" \
    --method "init(pay,asset)void" \
    --arg minbal.txn \
    --arg $STAKING_ASA_ID_1

goal app method --app-id $APP_ID \
    -f $DEPLOYER \
    --on-completion "NoOp" \
    --method "init(pay,asset)void" \
    --arg minbal.txn \
    --arg $STAKING_ASA_ID_2

goal asset send --assetid $REWARD_ASA_ID \
    -f $REWARDS_CREATOR \
    -t $APP_ADDR \
    -a $REWARD_TOTAL \
    -o rewards.txn

goal app method --app-id $APP_ID \
    -f $DEPLOYER \
    --on-completion "NoOp" \
    --method "reward(axfer,uint64,asset)void" \
    --arg rewards.txn \
    --arg $FIXED_RATE \
    --arg $REWARD_ASA_ID

