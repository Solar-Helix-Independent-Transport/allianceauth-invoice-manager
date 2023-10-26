import React from "react";
import { useQuery } from "react-query";
import { loadAllVisible } from "../apis/Invoices";
import { BaseTable } from "@pvyparts/allianceauth-components";
import { Button, Panel, Glyphicon, ButtonGroup } from "react-bootstrap";
import { CopyToClipboard } from "react-copy-to-clipboard";
import PaidButton from "./PaidButton";

const InvVisible = () => {
  const { isLoading, isFetching, data } = useQuery("visible", () =>
    loadAllVisible()
  );

  const columns = React.useMemo(
    () => [
      {
        header: "Character",
        accessorKey: "character.character_name",
      },
      {
        header: "Corporation",
        accessorKey: "character.corporation_name",
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}> {props.getValue()} </div>
        ),
      },
      {
        header: "Alliance",
        accessorKey: "character.alliance_name",
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}> {props.getValue()} </div>
        ),
      },
      {
        header: "Due Date",
        accessorKey: "due_date",
        enableColumnFilter: false,
        cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>
            {new Date(props.getValue()).toLocaleString()}
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
        header: "Amount",
        accessorKey: "amount",
        cell: (props) => (
          <>
            <CopyToClipboard text={props.getValue()} className="text-center">
              <ButtonGroup bsClass="btn-group special">
                <Button>{props.getValue()}</Button>
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
      {
        header: "Actions",
        accessorKey: "action",
        enableColumnFilter: false,
        enableSorting: false,
        cell: (props) =>
          props.getValue() ? <PaidButton pk={props.row.original.pk} /> : <></>,
      },
    ],
    []
  );
  let initialState = {};
  if (data) {
    let hideActions = data.reduce((p, c) => p | c.action, false);
    if (!hideActions) {
      initialState = { columnVisibility: { action: false } };
    }
  }
  return (
    <>
      {!isLoading ? (
        <Panel>
          <Panel.Heading>Visible Contributions</Panel.Heading>
          <Panel.Body>
            <BaseTable
              {...{
                isLoading,
                data,
                columns,
                initialState,
                isFetching,
              }}
            />
          </Panel.Body>
        </Panel>
      ) : (
        <></>
      )}
    </>
  );
};
export default InvVisible;
