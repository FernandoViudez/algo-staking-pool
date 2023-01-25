import { Algodv2, Indexer } from "algosdk";

const productionToken = {
  "x-api-key": "BtYg0Xyisl2oxmELrQeBz1h6pLEIhdYI7DsDSAgj",
};
const sandboxToken =
  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const productionHost = "https://testnet-algorand.api.purestake.io/ps2";
const sandboxHost = "http://127.0.0.1";

export const daemonClient = new Algodv2(sandboxToken, sandboxHost, 4001);

export const indexerClient = new Indexer("", sandboxHost, 8980);
