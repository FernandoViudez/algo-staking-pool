import { indexerClient } from "../src/client";
import { TRANTORIAN_COLLECTION_ADDRESS } from "./constants";
import { getCurrentAccount } from "./current-account";
import { hideNftsBtn, showNftsList } from "./ui";

export async function onShowAvailableNFTs() {
  const availableNFTs: string[] = await getListOfAvailableNFTs();
  buildOptions(availableNFTs);
  showNftsList();
  hideNftsBtn();
}

async function getListOfAvailableNFTs() {
  const currentAccount = getCurrentAccount();
  const holdingAssetsList = await indexerClient
    .lookupAccountAssets(currentAccount)
    .do();
  const trantorianCollectionAssetsList = await indexerClient
    .lookupAccountAssets(TRANTORIAN_COLLECTION_ADDRESS)
    .includeAll()
    .do();

  const newList = [];

  for (let holdingAsset of holdingAssetsList.assets) {
    const index = trantorianCollectionAssetsList.assets.findIndex(
      (item: any) => item["asset-id"] == holdingAsset["asset-id"]
    );
    if (index > -1) {
      newList.push(trantorianCollectionAssetsList.assets[index]["asset-id"]);
    }
  }

  return newList;
}

function buildOptions(list: string[]) {
  for (let asa of list) {
    const optionEl = document.createElement("option");
    optionEl.value = asa;
    optionEl.innerText = asa;
    document.getElementById("nfts-list").appendChild(optionEl);
  }
}
