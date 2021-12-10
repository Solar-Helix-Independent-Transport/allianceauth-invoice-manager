import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export async function loadUnpaid() {
  const api = await axios.get(`/invoice/api/account/unpaid`);
  console.log(`get unpaid in api`);
  return api.data;
}

export async function loadAllVisible() {
  const api = await axios.get(`/invoice/api/account/visible`);
  console.log(`get visible from api`);
  return api.data;
}

export async function loadPaymentCorp() {
  const api = await axios.get(`/invoice/api/config/corp`);
  console.log(`get corp data in api`);
  return api.data;
}

