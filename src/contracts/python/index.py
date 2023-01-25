#!/usr/bin/env python3

# participants always will stake NFTs (pure) so amount is always 1
# max amount of nfts to stake is 9
# nfts_list max lenght is 126 bytes
# 14 bytes for each nft

import json
from pytealutils.strings.string import atoi, itoa
from pyteal import (Btoi, pragma, Seq, Subroutine, TealType, Expr, abi, Router, BareCallActions, OnCompleteAction, Approve, CallConfig, Assert, TxnType, Txn, Global,
                    App, Bytes, Not, If, Return, ScratchVar, Int, OnComplete, Reject, InnerTxnBuilder, TxnField, Gt, Ge, Balance, For, Concat, AssetParam, Len, Mod, Extract)

pragma(compiler_version="^0.18.1")

# Constants
CONTRACT_VERSION = 6
BYTES_PER_NFT = Int(14)
MAX_LIST_BYTES = Int(126)
ADMIN_ADDRESS = Bytes("A")  # global byteslice
STAKE_COLLECTION_CREATOR = Bytes("SCC")  # global byteslice

PAUSED_FLAG = Bytes("P")  # global byteslice or global int?

REWARD_ASSET = Bytes("RA")  # global int
FIXED_RATE = Bytes("FR")  # global int
BEGIN_TIMESTAMP = Bytes("BT")  # global int
END_TIMESTAMP = Bytes("ET")  # global int
TOTAL_REWARDS = Bytes("TR")  # global int
TOTAL_STAKED = Bytes("TS")  # global int

LAST_UPDATED = Bytes("LU")  # local int
AMOUNT_REWARDED = Bytes("AR")  # local int
AMOUNT_STAKED = Bytes("AS")  # local int

# each asset has 16 bytes available
# 0-15 first element
# 16-32 second element
# etc ...
STAKED_LIST = Bytes("SL")  # local byteslice


@Subroutine(TealType.none)
def add_to_stake_list(asset_id: Expr) -> Expr:
    user_staked_list = App.localGetEx(
        Txn.sender(), Global.current_application_id(), STAKED_LIST)
    return Seq(
        user_staked_list,
        (zeros_to_add := ScratchVar()).store(Bytes("")),
        (full_byte_asset := ScratchVar()).store(Bytes("")),
        (tmp_list := ScratchVar()).store(Bytes("")),
        If(user_staked_list.hasValue())
        .Then(Seq(
            tmp_list.store(
                App.localGet(Txn.sender(), STAKED_LIST)
            )
        )),
        Assert(
            Len(tmp_list.load()) <= (MAX_LIST_BYTES - BYTES_PER_NFT),
            Len(asset_id) <= BYTES_PER_NFT
        ),
        If(Len(asset_id) < BYTES_PER_NFT)
        .Then(Seq(
            For((i := ScratchVar()).store(Int(0)), i.load() < (
                BYTES_PER_NFT - Len(asset_id)), i.store(i.load() + Int(1)))
            .Do(
                zeros_to_add.store(
                    Concat(zeros_to_add.load(), Bytes("0")))
            ),
            full_byte_asset.store(
                Concat(zeros_to_add.load(), asset_id))
        ))
        .ElseIf(Len(asset_id) == BYTES_PER_NFT)
        .Then(Seq(
            full_byte_asset.store(asset_id)
        )),
        App.localPut(
            Txn.sender(),
            STAKED_LIST,
            Concat(
                tmp_list.load(),
                full_byte_asset.load()
            )
        ),
    )


@Subroutine(TealType.none)
def remove_from_list(start: Expr) -> Expr:
    return Seq(
        (new_list := ScratchVar()).store(Bytes("")),
        If(start == Int(0))
        .Then(Seq(
            new_list.store(
                Extract(App.localGet(Txn.sender(), STAKED_LIST), BYTES_PER_NFT, Len(
                    App.localGet(Txn.sender(), STAKED_LIST)) - BYTES_PER_NFT)
            )
        ))
        .Else(Seq(
            new_list.store(
                Concat(
                    Extract(App.localGet(Txn.sender(), STAKED_LIST),
                            start - BYTES_PER_NFT, BYTES_PER_NFT),
                    Extract(App.localGet(Txn.sender(), STAKED_LIST), start + BYTES_PER_NFT,
                            Len(App.localGet(Txn.sender(), STAKED_LIST)) - BYTES_PER_NFT)
                ),
            )
        )),
        App.localPut(Txn.sender(), STAKED_LIST, new_list.load())
    )


@ Subroutine(TealType.uint64)
def get_asset_idx_from_list(asset_id: Expr) -> Expr:
    return Seq(
        For((i := ScratchVar()).store(Int(1)), i.load() <= MAX_LIST_BYTES, i.store(i.load() + Int(1))).Do(
            If(Mod(i.load(), BYTES_PER_NFT) == Int(0))
            .Then(Seq(
                (asset_id_from_list := ScratchVar()).store(atoi(
                    Extract(App.localGet(Txn.sender(), STAKED_LIST),
                            i.load() - BYTES_PER_NFT, BYTES_PER_NFT)
                )),
                If(asset_id_from_list.load() == asset_id)
                .Then(Return(i.load() - BYTES_PER_NFT))
            ))
        ),
        Reject(),
    )


@ Subroutine(TealType.uint64)
def is_creator() -> Expr:
    return Txn.sender() == Global.creator_address()


@ Subroutine(TealType.none)
def is_admin() -> Expr:
    return Assert(Txn.sender() == App.globalGet(ADMIN_ADDRESS))


@ Subroutine(TealType.none)
def set_admin(addr: Expr) -> Expr:
    return Seq(
        App.globalPut(ADMIN_ADDRESS, addr),
    )


@ Subroutine(TealType.none)
def check_if_official_asa(asset_id: Expr) -> Expr:
    creator = AssetParam.creator(asset_id)
    return Seq(
        creator,
        Assert(
            creator.value() == App.globalGet(
                STAKE_COLLECTION_CREATOR)
        ),
    )


@ Subroutine(TealType.none)
def optin_asset(asset: Expr) -> Expr:
    return Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: asset,
            TxnField.asset_receiver: Global.current_application_address(),
        }),
        InnerTxnBuilder.Submit(),
    )


@ Subroutine(TealType.none)
def send_asset(
    asset: abi.Asset,
    amount: abi.Uint64,
    recipient: abi.Account


) -> Expr:
    return Seq(

        # Store amount we actually need to dispense.
        (dispensed_amount := ScratchVar()).store(amount.get()),

        # Check if we're sending the staking asset or the reward asset
        # If we're trying to send more than the account has, use the maximum
        # available value the account has.
        # Deduct the amount from the local state.
        If(asset.asset_id() == App.globalGet(REWARD_ASSET))
        .Then(
            (amount_rewarded := ScratchVar()).store(
                App.localGet(recipient.address(), AMOUNT_REWARDED)),
            If(dispensed_amount.load() > amount_rewarded.load())
            .Then(dispensed_amount.store(amount_rewarded.load())),
            App.localPut(
                recipient.address(),
                AMOUNT_REWARDED,
                App.localGet(recipient.address(), AMOUNT_REWARDED) -
                dispensed_amount.load()
            ),
        ),

        # Send the amount requested or maximum amount available to the recipient.
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_amount: dispensed_amount.load(),
                TxnField.asset_receiver: recipient.address(),
                TxnField.fee: Int(0),
            }
        ),
        InnerTxnBuilder.Submit(),
    )


@Subroutine(TealType.none)
def is_not_paused() -> Expr:
    return Seq(
        Assert(Not(App.globalGet(PAUSED_FLAG))),
    )


@Subroutine(TealType.none)
def calculate_rewards(addr: Expr) -> Expr:
    return Seq(
        # Skip if not begun
        If(Global.latest_timestamp() < App.globalGet(BEGIN_TIMESTAMP), Return()),

        # Skip if updated since ET
        If(App.localGet(addr, LAST_UPDATED) >
           App.globalGet(END_TIMESTAMP), Return()),

        # Calculate time since last update
        # End
        (end := ScratchVar()).store(
            If(Global.latest_timestamp() > App.globalGet(END_TIMESTAMP))
            .Then(App.globalGet(END_TIMESTAMP))
            .Else(Global.latest_timestamp())
        ),
        # Start
        (start := ScratchVar()).store(
            If(App.localGet(addr, LAST_UPDATED) < App.globalGet(BEGIN_TIMESTAMP))
            .Then(App.globalGet(BEGIN_TIMESTAMP))
            .Else(App.localGet(addr, LAST_UPDATED))
        ),

        # Duration
        (pool_total_duration := ScratchVar()).store(
            App.globalGet(END_TIMESTAMP) - App.globalGet(BEGIN_TIMESTAMP)),
        (time_in_seconds := ScratchVar()).store(end.load() - start.load()),

        # utils vars
        (corresponding_units := ScratchVar()).store(
            time_in_seconds.load() / (pool_total_duration.load() / App.globalGet(TOTAL_REWARDS))
        ),
        (stake_percent := ScratchVar()).store(
            App.localGet(Txn.sender(), AMOUNT_STAKED) * \
            Int(100) / App.globalGet(TOTAL_STAKED)
        ),

        # Calculate rewards
        (rewards := ScratchVar()).store(
            stake_percent.load() * corresponding_units.load() / App.globalGet(FIXED_RATE)
        ),

        # If there are more total rewards than have been rewarded we can
        # issue them, otherwise we can only reward what's available.
        If(App.globalGet(TOTAL_REWARDS) >= rewards.load())
        .Then(Seq(
            # Remove rewards from global
            App.globalPut(TOTAL_REWARDS, App.globalGet(
                TOTAL_REWARDS) - rewards.load()),

            # Add rewards to local
            App.localPut(addr, AMOUNT_REWARDED, App.localGet(
                addr, AMOUNT_REWARDED) + rewards.load()),
        ))
        .Else(Seq(
            # Add any remaining rewards to local
            App.localPut(addr, AMOUNT_REWARDED, App.localGet(
                addr, AMOUNT_REWARDED) + App.globalGet(TOTAL_REWARDS)),

            # Global rewards are now empty.
            App.globalPut(TOTAL_REWARDS, Int(0)),
        )),

        # Should we update "LU" here? It seems to be updated in the TEAL code
        App.localPut(addr, LAST_UPDATED, Global.latest_timestamp()),
    )


router = Router(
    # Name of the contract
    "staking",
    # What to do for each on-complete type when no arguments are passed (bare call)
    BareCallActions(
        # On create only, just approve
        no_op=OnCompleteAction.never(),
        # Just be nice, we _must_ provide _something_ for clear state because it is its own
        # program and the router needs _something_ to build
        clear_state=OnCompleteAction.call_only(Approve()),
    ),
)


@router.method(no_op=CallConfig.CALL, opt_in=CallConfig.CALL)
def deposit(
    axfer: abi.AssetTransferTransaction,
    asset: abi.Asset
) -> Expr:
    """Deposit adds an amount of staked assets to the pool, increasing the
    senders share of the rewards."""
    return Seq(
        # Check the contract isn't paused
        is_not_paused(),

        # Check previous transaction is of type axfer
        Assert(axfer.get().type_enum() == TxnType.AssetTransfer),

        # Confirm sender for this appl and the axfer are the same
        # Note: Do we need to care if it came from the same address?
        Assert(axfer.get().sender() == Txn.sender()),

        # Check the staking asset is being received by the smart contract
        Assert(axfer.get().asset_receiver() ==
               Global.current_application_address()),

        # Check if asset was created from collection addr
        check_if_official_asa(asset.asset_id()),

        # save asset id into staked list
        add_to_stake_list(itoa(asset.asset_id())),

        # update local staked amount
        App.localPut(
            Txn.sender(),
            AMOUNT_STAKED,
            App.localGet(Txn.sender(), AMOUNT_STAKED) + \
            axfer.get().asset_amount()
        ),

        # Add deposit to global
        App.globalPut(
            TOTAL_STAKED,
            App.globalGet(TOTAL_STAKED) + axfer.get().asset_amount()
        ),

        # Calculate rewards
        calculate_rewards(Txn.sender()),

        # Success
        Approve()
    )


@router.method(no_op=CallConfig.ALL, close_out=CallConfig.ALL)
def withdraw(
    asset: abi.Asset,
    amount: abi.Uint64,
    recipient: abi.Account,
    dummy: abi.Uint64
) -> Expr:
    """Remove an amount of staked assets or reward assets from the pool."""
    return Seq(
        If(dummy.get() == Int(0)).Then(Seq(
            # Check the contract isn't paused
            is_not_paused(),

            # Calculate rewards
            calculate_rewards(Txn.sender()),

            # if withdrawing staked asset, then update staked asset local state
            If(Not(App.globalGet(REWARD_ASSET) == asset.asset_id()))
            .Then(Seq(
                App.localPut(
                    Txn.sender(),
                    AMOUNT_STAKED,
                    App.localGet(
                        Txn.sender(),
                        AMOUNT_STAKED
                    ) - Int(1)
                ),
                remove_from_list(get_asset_idx_from_list(asset.asset_id())),
            )),

            # Send asset to recipient
            send_asset(asset, amount, recipient),

            # If it's a NoOp we can skip the closeout check
            If(Txn.on_completion() == OnComplete.CloseOut, Seq(
                Assert(Not(App.localGet(recipient.address(), AMOUNT_REWARDED))),
            )),

        )),

        # Success
        Approve(),
    )


@router.method(no_op=CallConfig.CREATE)
def deploy(
    collection_creator: abi.Account,
    reward: abi.Asset,
    begin: abi.Uint64,
    end: abi.Uint64,
) -> Expr:
    """Used to deploy the contract, defining assets and times."""
    return Seq(
        # Can only deploy as a new smart contract.
        Assert(Not(Txn.application_id())),

        # User sender as admin.
        set_admin(Txn.sender()),

        # Set reward asset
        App.globalPut(REWARD_ASSET, reward.asset_id()),

        # Set begin timestamp
        # Must be after LatestTimestamp
        Assert(Gt(begin.get(), Global.latest_timestamp())),
        App.globalPut(BEGIN_TIMESTAMP, begin.get()),

        # Set end timestamp
        # Must be after begin timestamp
        Assert(Gt(end.get(), begin.get())),
        App.globalPut(END_TIMESTAMP, end.get()),

        # Set collection creator addr
        App.globalPut(STAKE_COLLECTION_CREATOR, collection_creator.address()),

        # Success
        Approve(),
    )


@router.method(no_op=CallConfig.CALL)
def init(
    pay: abi.PaymentTransaction,
    asset: abi.Asset
) -> Expr:
    """Initialise the newly deployed contract, funding it with a minimum
    balance and allowing it to opt in to the request assets (can be any assets)."""
    return Seq(
        # Check if admin is initializing the contract
        is_admin(),

        # Check previous transaction is a payment transaction
        Assert(pay.get().type_enum() == TxnType.Payment),

        # Check receiver of payment is this smart contract
        Assert(pay.get().receiver() == Global.current_application_address()),

        # Check amount is greater than minimum balance requirement
        Assert(
            Ge(
                Balance(Global.current_application_address()) + \
                pay.get().amount(),
                (Global.min_balance() * (Txn.assets.length() + Int(1))) + \
                (Global.min_txn_fee() * Txn.assets.length())
            )
        ),

        optin_asset(asset.asset_id()),

        # Success
        Approve(),
    )


@router.method(no_op=CallConfig.CALL, close_out=CallConfig.CALL)
def reward(
    rewards: abi.AssetTransferTransaction,
    fixed_rate: abi.Uint64,
    reward: abi.Asset
) -> Expr:
    """Primarily used to supply the initial rewards for the staking contract,
    but can also be used to add additional rewards before the contract ends."""
    return Seq(
        # Check if admin is supplying the rewards
        is_admin(),

        # Check previous transaction is of type axfer
        Assert(rewards.get().type_enum() == TxnType.AssetTransfer),

        # Check receiver of asset transfer is this smart contract
        Assert(rewards.get().asset_receiver() ==
               Global.current_application_address()),

        # Check received asset is reward
        Assert(rewards.get().xfer_asset() == App.globalGet(REWARD_ASSET)),

        # Increase Total Rewards available
        App.globalPut(TOTAL_REWARDS, App.globalGet(
            TOTAL_REWARDS) + rewards.get().asset_amount()),

        # Set fixed rate
        App.globalPut(FIXED_RATE, fixed_rate.get()),

        # Success
        Approve(),
    )


@router.method(no_op=CallConfig.CALL)
def config(
    paused: abi.Bool,
    admin: abi.Account,
) -> Expr:
    return Seq(
        is_admin(),
        App.globalPut(PAUSED_FLAG, paused.get()),
        set_admin(admin.address()),
    )


if __name__ == '__main__':
    approval, clearstate, contract = router.compile_program(
        version=CONTRACT_VERSION)

    with open("pyteal_staking.teal", "w") as f:
        f.write(approval)

    with open("pyteal_clear.teal", "w") as f:
        f.write(clearstate)

    with open("pyteal_abi.json", "w") as f:
        f.write(json.dumps(contract.dictify(), indent=4))
