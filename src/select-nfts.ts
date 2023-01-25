import { showSubmitBtn } from "./ui";
const LS_SELECTED_OPTS_NAME = "SELECTED_OPTS";

export let selectedOpts: number[] = [];

export function onInputChange(event: any) {
  const optsEl: HTMLCollection = event.target.selectedOptions;
  for (let i = 0; i < optsEl.length; i++) {
    selectedOpts.push(Number((optsEl[i] as any).value));
  }
  saveSelectedOpts();
  showSubmitBtn();
}

function saveSelectedOpts() {
  localStorage.setItem(LS_SELECTED_OPTS_NAME, JSON.stringify(selectedOpts));
}

export function getSelectedOpts(): number[] {
  return JSON.parse(localStorage.getItem(LS_SELECTED_OPTS_NAME));
}
