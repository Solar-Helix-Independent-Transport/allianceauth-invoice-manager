import React from "react";
import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { Bars } from "@agney/react-loading";
import invPaymentDetail from "./invPaymnetDetail";
import { Col, Row } from "react-bootstrap";
import { Panel } from "react-bootstrap";

const InvMenu = () => {
  const { isLoading, error, data } = useQuery("unpaid", () => loadUnpaid());
  let amountDue = 0;
  !isLoading
    ? (amountDue = data.reduce((result, filter) => {
        return result + filter.amount;
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
          <Panel.Heading class="text-center">
            <h3 class="panel-title">Outstanding</h3>
          </Panel.Heading>
          <Panel.Body>
            <Col sm={12}>
              <h3 class="text-center">
                {isLoading ? (
                  <Bars
                    style={{ margin: "0px", height: "24px" }}
                    className="spinner-size"
                  />
                ) : (
                  <>Ƶ {amountDue.toLocaleString()}</>
                )}
              </h3>
              <br />
              {invPaymentDetail()}
            </Col>
          </Panel.Body>
        </Panel>
      </Col>
      <Col md={4}>
        <div class="panel panel-default">
          <div class="panel-heading text-center">
            <h3 class="panel-title">Key</h3>
          </div>
          <div class="panel-body">
            <table
              class="table table-hover text-center"
              style={{ width: "100%" }}
            >
              <tbody>
                <tr class="info">
                  <td>Paid</td>
                </tr>
                <tr class="">
                  <td>Outstanding</td>
                </tr>
                <tr class="danger">
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
