import React from "react";
import { Button, Card, ButtonGroup } from "react-bootstrap";

import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import BaseTable from "../components/Tables/BaseTable/BaseTable";
import { CopyToClipboard } from "react-copy-to-clipboard";

const InvUnpaid = () => {
  const { isLoading, isFetching, error, data } = useQuery("unpaid", () =>
    loadUnpaid()
  );

  const columns = React.useMemo(
    () => [
      {
        header: "Character",
        accessorKey: "character.character_name",
        cell: (cell) => (
          //className={`bg-${past_due(cell.row.original)}`}
          <div style={{ whiteSpace: "nowrap" }}> {cell.getValue()} </div>
        ),
      },
      {
        header: "Due Date",
        accessorKey: "due_date",
        cell: (props) => (
          <>
            <div style={{ whiteSpace: "nowrap" }}>
              {new Date(props.getValue()).toLocaleString()}{" "}
            </div>
          </>
        ),
      },
      {
        header: "Invoice Reference",
        accessorKey: "invoice_ref",
        cell: (props) => (
          <div className="float-end">
            {props.row.original.paid ? (
              <Button
                bsClass="btn btn-success btn-sm col-xs-12"
                disabled={true}
              >
                {props.getValue()}
              </Button>
            ) : (
              <CopyToClipboard text={props.getValue()} className="text-center">
                <ButtonGroup bsClass="btn-group special">
                  <Button>{props.getValue()}</Button>
                  <Button bsClass="btn no-grow btn-warning">
                    <i class="fa-solid fa-copy"></i>
                  </Button>
                </ButtonGroup>
              </CopyToClipboard>
            )}
          </div>
        ),
      },
      {
        header: "Amount",
        accessorKey: "amount",
        cell: (props) => (
          <>
            {props.row.original.paid ? (
              <Button
                bsClass="btn btn-success btn-sm col-xs-12"
                disabled={true}
              >
                {props.getValue().toLocaleString()}
              </Button>
            ) : (
              <CopyToClipboard text={props.getValue()} className="text-center">
                <ButtonGroup bsClass="btn-group special">
                  <Button>{props.getValue().toLocaleString()}</Button>
                  <Button bsClass="btn no-grow btn-warning">
                    <i class="fa-solid fa-copy"></i>
                  </Button>
                </ButtonGroup>
              </CopyToClipboard>
            )}
          </>
        ),
      },
      {
        header: "Details",
        accessorKey: "note",
        cell: (props) => (
          <div style={{ whiteSpace: "pre-line" }}>{props.getValue()}</div>
        ),
      },
    ],
    []
  );
  return (
    <div className="p-1">
      <Card>
        <Card.Header><Card.Title>Your Contributions</Card.Title></Card.Header>
        <Card.Body>
          <BaseTable
            {...{
              isLoading,
              data,
              columns,
              error,
              isFetching,
            }}
          />
        </Card.Body>
      </Card>
    </div>
  );
};

export default InvUnpaid;
