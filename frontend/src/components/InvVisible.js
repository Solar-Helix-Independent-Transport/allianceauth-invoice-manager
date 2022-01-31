import React from "react";
import { useQuery } from "react-query";
import { loadAllVisible } from "../apis/Invoices";
import { BaseTable, textColumnFilter, SelectColumnFilter } from "../components/BaseTable";
import { Button, Panel, Glyphicon, ButtonGroup } from "react-bootstrap";
import { CopyToClipboard } from "react-copy-to-clipboard";

const InvVisible = () => {
  const { isLoading, error, data } = useQuery(
    "visible",
    () => loadAllVisible()
  );

  function getRowProps(row) {
    let now = new Date();
    let comp = new Date(row.values.due_date);
    if (comp < now) {
      return {
        className: "danger",
      };
    }
  }

  const columns = React.useMemo(
    () => [
      {
        Header: "Character",
        accessor: "character.character_name",
        Filter: textColumnFilter,
        filter: "includes",
      },
      {
        Header: "Corporation",
        accessor: "character.corporation_name",
        Filter: SelectColumnFilter,
        filter: "includes",
        Cell: (props) => <div style={{whiteSpace: "nowrap"}}> {props.value} </div>,
      },
      {
        Header: "Alliance",
        accessor: "character.alliance_name",
        Filter: SelectColumnFilter,
        filter: "text",
        Cell: (props) => <div style={{whiteSpace: "nowrap"}}> {props.value} </div>,

      },
      {
        Header: "Due Date",
        accessor: "due_date",
        Cell: (props) => <div style={{whiteSpace: "nowrap"}}> {new Date(props.value).toLocaleString()} </div>,
      },
      {
        Header: "Invoice Reference",
        accessor: "invoice_ref",
        Filter: textColumnFilter,
        filter: "includes",
        Cell: (props) => (
          <>
            <CopyToClipboard text={props.value} className="text-center">
              <ButtonGroup bsClass="btn-group special">
                <Button >{props.value.toLocaleString()}</Button>
                <Button bsClass="btn no-grow btn-warning">
                  <Glyphicon glyph="copy" />
                </Button>
              </ButtonGroup>
            </CopyToClipboard>
          </>
        ),
      },
      {
        Header: "Amount",
        accessor: "amount",
        Cell: (props) => (
          <>
            <CopyToClipboard text={props.value} className="text-center">
              <ButtonGroup bsClass="btn-group special">
                <Button >{props.value.toLocaleString()}</Button>
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
        accessor: "note",
      },
      
    ],
    []
  );

  return (
    <>
    {!isLoading ? (
        <Panel>
            <Panel.Heading>
                Visible Contributions
            </Panel.Heading>
            <Panel.Body>
                <BaseTable {...{ isLoading, data, columns, error, getRowProps }} />
            </Panel.Body>
        </Panel>
      ) : (
        <></>
      )
    }
    </>
    );
  };
export default InvVisible;