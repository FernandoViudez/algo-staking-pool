import { ABIContract, ABIMethod } from "algosdk";
import { abiJSON } from "./abi/staking.abi";

const contract = new ABIContract(abiJSON);

export function getMethodByName(name: string): ABIMethod {
  const m = contract.methods.find((mt: ABIMethod) => {
    return mt.name == name;
  });
  if (m === undefined) throw Error("Method undefined: " + name);
  return m;
}
