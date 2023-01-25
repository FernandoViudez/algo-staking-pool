source "$(dirname ${BASH_SOURCE[0]})/config.sh"

# asets involved
STAKING_ASA_ID_0=$(source "$(dirname ${BASH_SOURCE[0]})/create-collection.sh" | grep 'asset index' | awk -F ' ' '{print $6}')
STAKING_ASA_ID_1=$(source "$(dirname ${BASH_SOURCE[0]})/create-collection.sh" | grep 'asset index' | awk -F ' ' '{print $6}')
STAKING_ASA_ID_2=$(source "$(dirname ${BASH_SOURCE[0]})/create-collection.sh" | grep 'asset index' | awk -F ' ' '{print $6}')
REWARD_ASA_ID=$(source "$(dirname ${BASH_SOURCE[0]})/create-rewards.sh" | grep 'asset index' | awk -F ' ' '{print $6}')

# fund client account
source "$(dirname ${BASH_SOURCE[0]})/optin.sh" | grep ''
source "$(dirname ${BASH_SOURCE[0]})/fund-account.sh" | grep ''
echo "Client account successfully funded"

# pool address
APP_ID=$(source "$(dirname ${BASH_SOURCE[0]})/deploy.sh" | grep 'app index' | awk -F ' ' '{print $6}')
APP_ADDR=$(goal app info --app-id $APP_ID | grep "Application account" | awk -F ":" '{print $2}' | xargs)

# initialize app
source "$(dirname ${BASH_SOURCE[0]})/init.sh" | grep 'succeeded'

echo "REWARD ASA ID ~> " $REWARD_ASA_ID
echo "APP ID ~> " $APP_ID
echo "APP ADDR ~> " $APP_ADDR