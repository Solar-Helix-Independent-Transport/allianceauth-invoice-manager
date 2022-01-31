import React from "react";
import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { Bars } from "@agney/react-loading";
import InvPaymentDetail from "./InvPaymnetDetail";
import { Col, Row } from "react-bootstrap";
import { Panel } from "react-bootstrap";

const InvMenu = () => {
  const { isLoading, error, data } = useQuery("unpaid", () => loadUnpaid());
  let amountDue = 0;
  !isLoading
    ? (amountDue = data.reduce((result, filter) => {
        if (!filter.paid){
          result = result + filter.amount
        }
        return result;
      }, 0))
    : error
    ? (amountDue = "Error")
    : (amountDue = 0);

  return (
    <Row>
      <Col md={8}>
        <Panel
          bsStyle={
            isLoading
              ? "info"
              : !error
              ? amountDue > 0
                ? "warning"
                : "success"
              : "danger"
          }
        >
          <Panel.Heading className="text-center">
            <h3 className="panel-title">Outstanding</h3>
          </Panel.Heading>
          <Panel.Body>
            <Col sm={12}>
              <h3 className="text-center">
                {isLoading ? (
                  <Bars
                    style={{ margin: "0px", height: "24px" }}
                    className="spinner-size"
                  />
                ) : (<>{
                  amountDue > 0 ? <>Ƶ {amountDue.toLocaleString()}</> : <>No Payment Required</>
                }</>
                )}
              </h3>
              <br />
              {InvPaymentDetail()}
            </Col>
          </Panel.Body>
        </Panel>
      </Col>
      <Col md={4}>
        <div className="panel panel-default">
          <div className="panel-heading text-center">
            <h3 className="panel-title">Key</h3>
          </div>
          <div className="panel-body">
            <table
              className="table table-hover text-center"
              style={{ width: "100%" }}
            >
              <tbody>
                <tr className="info">
                  <td>Paid</td>
                </tr>
                <tr className="">
                  <td>Outstanding</td>
                </tr>
                <tr className="danger">
                  <td>Overdue</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </Col>
    </Row>
  );
};

export default InvMenu;
