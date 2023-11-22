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

  function past_due(row) {
    if (row.paid) {
      return "info";
    }
    let value = row.due_date;
    let now = new Date();
    let comp = new Date(value);
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
            <div
              style={{ whiteSpace: "nowrap" }}
              className={`text-${past_due(props.getValue())}`}
            >
              {new Date(props.getValue()).toLocaleString()}{" "}
            </div>
          </>
        ),
      },
      {
        header: "Invoice Reference",
        accessorKey: "invoice_ref",
        cell: (props) => (
          <>
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
          rowClasses={past_due}
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
