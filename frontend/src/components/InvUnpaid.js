import React from "react";
import { Button, Panel, Glyphicon, ButtonGroup } from "react-bootstrap";

import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { BaseTable } from "@pvyparts/allianceauth-components";
import { CopyToClipboard } from "react-copy-to-clipboard";

const InvUnpaid = () => {
  const { isLoading, isFetching, error, data } = useQuery("unpaid", () =>
    loadUnpaid()
  );

  function past_due(values) {
    let now = new Date();
    let comp = new Date(values);
    if (comp < now) {
      return "danger";
    } else {
      return "default";
    }
  }

  const columns = React.useMemo(
    () => [
      {
        header: "Character",
        accessorKey: "character.character_name",
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}> {props.getValue()} </div>
        ),
      },
      {
        header: "Due Date",
        accessorKey: "due_date",
        cell: (props) => (
          <>
            {props.row.original.paid ? (
              <div className="text-center">
                <span className="label label-success">Paid</span>
              </div>
            ) : (
              <div
                style={{ whiteSpace: "nowrap" }}
                className={`text-${past_due(props.getValue())}`}
              >
                {new Date(props.getValue()).toLocaleString()}{" "}
              </div>
            )}
          </>
        ),
      },
      {
        header: "Invoice Reference",
        accessorKey: "invoice_ref",
        cell: (props) => (
          <>
            {props.row.original.paid ? (
              <div className="text-center">
                <span className="label label-success">
                  Paid: {props.getValue()}
                </span>
              </div>
            ) : (
              <CopyToClipboard text={props.getValue()} className="text-center">
                <ButtonGroup bsClass="btn-group special">
                  <Button>{props.getValue()}</Button>
                  <Button bsClass="btn no-grow btn-warning">
                    <Glyphicon glyph="copy" />
                  </Button>
                </ButtonGroup>
              </CopyToClipboard>
            )}
          </>
        ),
      },
      {
        header: "Amount",
        accessorKey: "amount",
        cell: (props) => (
          <>
            {props.row.original.paid ? (
              <div className="text-center">
                {props.getValue().toLocaleString()}
              </div>
            ) : (
              <CopyToClipboard text={props.getValue()} className="text-center">
                <ButtonGroup bsClass="btn-group special">
                  <Button>{props.getValue().toLocaleString()}</Button>
                  <Button bsClass="btn no-grow btn-warning">
                    <Glyphicon glyph="copy" />
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
    <Panel>
      <Panel.Heading>Your Contributions</Panel.Heading>
      <Panel.Body>
        <BaseTable
          {...{
            isLoading,
            data,
            columns,
            error,
            isFetching,
          }}
        />
      </Panel.Body>
    </Panel>
  );
};

export default InvUnpaid;
