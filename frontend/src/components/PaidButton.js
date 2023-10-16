import React from "react";
import { postPayInvoice } from "../apis/Invoices";
import { Button } from "react-bootstrap";
import { useQueryClient } from "react-query";

const PaidButton = ({ pk }) => {
  const [active, setActive] = React.useState(false);
  const queryClient = useQueryClient();

  return (
    <>
      <Button
        bsClass={`btn btn-${active ? "success" : "info"}`}
        active={!active}
        onClick={async () => {
          setActive(true);
          postPayInvoice(pk);
          queryClient.invalidateQueries({ queryKey: "visible" });
        }}
      >
        {active ? `Paid` : `Mark as Paid`}
      </Button>
    </>
  );
};
export default PaidButton;
