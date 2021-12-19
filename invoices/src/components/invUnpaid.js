import React from "react";
import { Button, Panel, Glyphicon, ButtonGroup } from "react-bootstrap";

import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { BaseTable, textColumnFilter} from "../components/BaseTable";
import { CopyToClipboard } from "react-copy-to-clipboard";

const InvUnpaid = () => {
  const { isLoading, error, data } = useQuery("unpaid", () => loadUnpaid());

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
        Header: "Due Date",
        accessor: "due_date",
        Cell: (props) => <> {new Date(props.value).toLocaleString()} </>,
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
    <Panel>
      <Panel.Heading>Your Contributions</Panel.Heading>
      <Panel.Body>
        <BaseTable {...{ isLoading, data, columns, error, getRowProps }} />
      </Panel.Body>
    </Panel>
  );
};

export default InvUnpaid;
