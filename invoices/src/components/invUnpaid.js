import React from "react";
import { Panel } from "react-bootstrap";
import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { BaseTable, SelectColumnFilter } from "../components/BaseTable";

const InvUnpaid = () => {
  const { isLoading, error, data } = useQuery(
    "unpaid",
    () => loadUnpaid()
  );


  const columns = React.useMemo(
    () => [
      {
        Header: "Character",
        accessor: "character.character_name",
        Filter: SelectColumnFilter,
        filter: "includes",
      },
      {
        Header: "Due Date",
        accessor: "due_date",
        Cell: (props) => <div> {new Date(props.value).toLocaleString()} </div>,
      },
      {
        Header: "Invoice Reference",
        accessor: "invoice_ref",
        Filter: SelectColumnFilter,
        filter: "includes",
      },
      {
        Header: "Amount",
        accessor: "amount",
        Cell: (props) => <div> {props.value.toLocaleString()} </div>,
      },
      {
        Header: "Details",
        accessor: "note",
      },
    ],
    []
  );

  return (
    <Panel>
        <Panel.Heading>
            Your Contributions
        </Panel.Heading>
        <Panel.Body>
            <BaseTable {...{ isLoading, data, columns, error }} />
        </Panel.Body>
    </Panel>
  );
};

export default InvUnpaid;
