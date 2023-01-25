import { waitForConfirmation } from "algosdk";
import { daemonClient } from "../client";
import { myAlgoConnect } from "../connect-wallet";

export async function signTxns(txnToBeSigned: { txn: string }[]) {
  const signedTxns = await myAlgoConnect.signTxns(txnToBeSigned);
  return signedTxns;
}
export async function sendTxns(signedTxns: string[]) {
  const { txId } = await daemonClient
    .sendRawTransaction(parseSignedTxns(signedTxns))
    .do();
  await waitForConfirmation(daemonClient, txId, 3);
}

function parseSignedTxns(signedTxns: string[]): Uint8Array[] {
  return signedTxns.map((val) => new Uint8Array(Buffer.from(val, "base64")));
}
