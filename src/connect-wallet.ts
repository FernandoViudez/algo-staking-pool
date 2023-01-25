import MyAlgoConnect from "@randlabs/myalgo-connect";
import { saveCurrentAccount } from "./current-account";
import { hideConnectWalletBtn, showNftsBtn, showWithdraw } from "./ui";

export const myAlgoConnect = new MyAlgoConnect();

export async function onConnectWallet() {
  if (
    !(document.getElementById("app-addr") as HTMLInputElement).value ||
    !(document.getElementById("app-id") as HTMLInputElement).value ||
    !(document.getElementById("reward-asa-id") as HTMLInputElement).value
  ) {
    return alert("Please fill first three inputs");
  }
  const accountsSharedByUser = await myAlgoConnect.connect();
  saveCurrentAccount(accountsSharedByUser.pop().address);
  hideConnectWalletBtn();
  showNftsBtn();
  showWithdraw();
}
