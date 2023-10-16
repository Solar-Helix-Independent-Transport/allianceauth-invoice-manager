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

  const columns = React.useMemo(
    () => [
      {
        Header: "Character",
        accessorKey: "character.character_name",
      },
      {
        Header: "Due Date",
        accessorKey: "due_date",
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>
            {" "}
            {new Date(props.getValue()).toLocaleString()}{" "}
          </div>
        ),
      },
      {
        Header: "Invoice Reference",
        accessorKey: "invoice_ref",
        Cell: (props) => (
          <>
            <CopyToClipboard text={props.getValue()} className="text-center">
              <ButtonGroup bsClass="btn-group special">
                <Button disabled={props.row.values.paid}>
                  {props.getValue().toLocaleString()}
                </Button>
                <Button
                  disabled={props.row.getValue().paid}
                  bsClass="btn no-grow btn-warning"
                >
                  <Glyphicon glyph="copy" />
                </Button>
              </ButtonGroup>
            </CopyToClipboard>
          </>
        ),
      },
      {
        Header: "Amount",
        accessorKey: "amount",
        cell: (props) => (
          <>
            <CopyToClipboard text={props.getValue()} className="text-center">
              <ButtonGroup bsClass="btn-group special">
                <Button>{props.getValue().toLocaleString()}</Button>
                <Button bsClass="btn no-grow btn-warning">
                  <Glyphicon glyph="copy" />
                </Button>
              </ButtonGroup>
            </CopyToClipboard>
          </>
        ),
      },
      {
        Header: "Details",
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
