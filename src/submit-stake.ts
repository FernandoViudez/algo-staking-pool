import {
  AtomicTransactionComposer,
  makeAssetTransferTxnWithSuggestedParamsFromObject,
  makeBasicAccountTransactionSigner,
  OnApplicationComplete,
} from "algosdk";
import { daemonClient } from "./client";
import { getCurrentAccount } from "./current-account";
import { getSelectedOpts } from "./select-nfts";
import { getMethodByName } from "./abi";
import { encodeTxns, signer } from "./utils/atomic-txn-composer";
import { sendTxns, signTxns } from "./utils/send-sign-tx";

export async function submitStake() {
  const atc = await buildATC(getSelectedOpts().pop());
  const txnToBeSigned = encodeTxns(atc.buildGroup());
  const signedTxns = await signTxns(txnToBeSigned);
  await sendTxns(signedTxns);
}

async function buildATC(assetId: number) {
  const atomicTxnComposer = new AtomicTransactionComposer();
  const commonParams = {
    appID: parseInt(
      (document.getElementById("app-id") as HTMLInputElement).value
    ),
    sender: getCurrentAccount(),
    suggestedParams: await daemonClient.getTransactionParams().do(),
    signer,
  };
  atomicTxnComposer.addMethodCall({
    method: getMethodByName("deposit"),
    onComplete: (document.getElementById("first-time") as HTMLInputElement)
      .checked
      ? OnApplicationComplete.OptInOC
      : OnApplicationComplete.NoOpOC,
    methodArgs: [await buildAssetSendTxn(assetId), assetId],
    ...commonParams,
  });
  return atomicTxnComposer;
}

async function buildAssetSendTxn(asaId: number) {
  const signer = makeBasicAccountTransactionSigner({
    addr: "",
    sk: new Uint8Array(),
  });

  const axfer_txn = makeAssetTransferTxnWithSuggestedParamsFromObject({
    amount:
      parseInt(
        (document.getElementById("amount-to-stake") as HTMLInputElement).value
      ) || 1,
    assetIndex: asaId,
    from: getCurrentAccount(),
    suggestedParams: await daemonClient.getTransactionParams().do(),
    to: (document.getElementById("app-addr") as HTMLInputElement).value,
  });

  return {
    txn: axfer_txn,
    signer,
  };
}
