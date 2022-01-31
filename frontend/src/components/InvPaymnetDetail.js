import React from "react";
import { useQuery } from "react-query";
import { loadPaymentCorp } from "../apis/Invoices";

const InvPaymentDetail = () => {
  const { isLoading, error, data } = useQuery(["payment_corp"], () =>
    loadPaymentCorp()
  );

  return (
    <>
    <div className="col-sm-6">
        <p className="text-center"><small>All Payments are to be made to {isLoading | error ? (
            <> </>
            ):(
            <a href={"https://evewho.com/corporation/"+ data.corporation_id }>{data.corporation_name}</a>
            )
        }<br/>All payments made to other places will not be receipted!</small></p>
    </div>
    <div className="col-sm-6">
        <p className="text-center"><small>All Payments <b>MUST</b> include the Reference in the Reason Field<br/>Contact an Admin for assistance, if you made an error</small></p>
    </div>
    </>
  );
};

export default InvPaymentDetail;
