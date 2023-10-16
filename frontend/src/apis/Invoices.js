import axios from "axios";
import cookies from "js-cookies";

axios.defaults.xsrfHeaderName = "X-CSRFToken";

export async function loadUnpaid() {
  const api = await axios.get(`/invoice/api/account/unpaid`);
  console.log(`get unpaid in api`);
  console.log(api);
  return api.data;
}

export async function loadAllVisible() {
  const api = await axios.get(`/invoice/api/account/visible`);
  console.log(`get visible from api`);
  console.log(api);
  return api.data;
}

export async function loadPaymentCorp() {
  const api = await axios.get(`/invoice/api/config/corp`);
  console.log(`get corp data in api`);
  console.log(api);
  return api.data;
}

export async function postPayInvoice(id) {
  console.log(`Sent payment for invoice`);
  const api = await axios.post(
    `/invoice/api//admin/paid/${id}`,
    { id: id },
    { headers: { "X-CSRFToken": cookies.getItem("csrftoken") } }
  );
  return api.data;
}
