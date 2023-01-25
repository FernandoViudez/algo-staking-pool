import {
  AtomicTransactionComposer,
  makeBasicAccountTransactionSigner,
  TransactionWithSigner,
} from "algosdk";
export const signer = makeBasicAccountTransactionSigner({
  addr: "",
  sk: new Uint8Array(),
});
export function encodeTxns(group: TransactionWithSigner[]) {
  const newGroup: { txn: string }[] = [];
  for (let tx of group) {
    newGroup.push({
      txn: Buffer.from(tx.txn.toByte()).toString("base64"),
    });
  }
  console.log(newGroup);
  return newGroup;
}
