import { claimRewards } from "./claim-rewards";
import { onConnectWallet } from "./connect-wallet";
import { onInputChange } from "./select-nfts";
import { onShowAvailableNFTs } from "./show-available-nfts";
import { submitStake } from "./submit-stake";
import { withdrawStake } from "./withdraw-stake";

window.onload = () => {
  const connectWallet = document.getElementById("connect-wallet");
  const stakeBtn = document.getElementById("show-nfts");
  const nftsSelectInput = document.getElementById("nfts-list");
  const submitBtn = document.getElementById("submit");
  const rewardsBtn = document.getElementById("withdraw-rewards");
  const withdrawStakeBtn = document.getElementById("withdraw-stake");
  connectWallet.addEventListener("click", onConnectWallet);
  stakeBtn.addEventListener("click", onShowAvailableNFTs);
  nftsSelectInput.addEventListener("change", onInputChange);
  submitBtn.addEventListener("click", submitStake);
  rewardsBtn.addEventListener("click", claimRewards);
  withdrawStakeBtn.addEventListener("click", withdrawStake);
};
