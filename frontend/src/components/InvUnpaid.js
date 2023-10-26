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

  function getRowProps(row) {
    console.log(row.values);
    if (row.values.paid === true) {
      return {
        className: "info",
      };
    } else {
      let now = new Date();
      let comp = new Date(row.values.due_date);
      if (comp < now) {
        return {
          className: "danger",
        };
      }
    }
  }

  const columns = React.useMemo(
    () => [
      {
        header: "Character",
        accessorKey: "character.character_name",
      },
      {
        header: "Due Date",
        accessorKey: "due_date",
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>
            {" "}
            {new Date(props.getValue()).toLocaleString()}{" "}
          </div>
        ),
      },
      {
        header: "Invoice Reference",
        accessorKey: "invoice_ref",
        cell: (props) => (
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
        header: "Amount",
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
            getRowProps,
          }}
        />
      </Panel.Body>
    </Panel>
  );
};

export default InvUnpaid;
