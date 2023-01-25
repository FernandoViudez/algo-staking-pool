const ACCOUNT_LS_KEY = "CURRENT_ACCOUNT_ADDRESS";

export function saveCurrentAccount(address: string) {
  localStorage.setItem(ACCOUNT_LS_KEY, address);
}

export function getCurrentAccount() {
  return localStorage.getItem(ACCOUNT_LS_KEY);
}
