import { AtomicTransactionComposer, OnApplicationComplete } from "algosdk";
import { getMethodByName } from "./abi";
import { daemonClient } from "./client";
import { getCurrentAccount } from "./current-account";
import { encodeTxns, signer } from "./utils/atomic-txn-composer";
import { sendTxns, signTxns } from "./utils/send-sign-tx";

export async function claimRewards() {
  const atomicTxnComposer = new AtomicTransactionComposer();
  atomicTxnComposer.addMethodCall({
    appID: parseInt(
      (document.getElementById("app-id") as HTMLInputElement).value
    ),
    method: getMethodByName("withdraw"),
    sender: getCurrentAccount(),
    signer,
    suggestedParams: {
      ...(await daemonClient.getTransactionParams().do()),
      fee: 2000,
    },
    onComplete: OnApplicationComplete.NoOpOC,
    methodArgs: [
      parseInt(
        (document.getElementById("reward-asa-id") as HTMLInputElement).value
      ),
      100,
      getCurrentAccount(),
      0,
    ],
  });
  // dummy txn for costs of process
  // atomicTxnComposer.addMethodCall({
  //   appID: parseInt(
  //     (document.getElementById("app-id") as HTMLInputElement).value
  //   ),
  //   method: getMethodByName("withdraw"),
  //   sender: getCurrentAccount(),
  //   signer,
  //   suggestedParams: {
  //     ...(await daemonClient.getTransactionParams().do()),
  //     fee: 2000,
  //   },
  //   onComplete: OnApplicationComplete.NoOpOC,
  //   methodArgs: [
  //     parseInt(
  //       (document.getElementById("reward-asa-id") as HTMLInputElement).value
  //     ),
  //     100,
  //     getCurrentAccount(),
  //     1,
  //   ],
  // });
  const txnToBeSigned = encodeTxns(atomicTxnComposer.buildGroup());
  const signedTxns = await signTxns(txnToBeSigned);
  await sendTxns(signedTxns);
}
