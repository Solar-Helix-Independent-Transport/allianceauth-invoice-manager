import React from "react";
import { useQuery } from "react-query";
import { loadUnpaid } from "../apis/Invoices";
import { Bars } from "@agney/react-loading";
import InvPaymentDetail from "./InvPaymnetDetail";
import { Col, Row } from "react-bootstrap";
import { Card } from "react-bootstrap";

const InvMenu = () => {
  const { isLoading, error, data } = useQuery("unpaid", () => loadUnpaid());
  let amountDue = 0;
  !isLoading
    ? (amountDue = data.reduce((result, filter) => {
        if (!filter.paid) {
          result = result + filter.amount;
        }
        return result;
      }, 0))
    : error
    ? (amountDue = "Error")
    : (amountDue = 0);

  return (
    <Row className="flex-row align-content-stretch">
      <div className="w-75 ps-3 pb-1 pe-1">
        <Card
          className={`
            ${
              isLoading
                ? "border-info"
                : !error
                ? amountDue > 0
                  ? "border-warning"
                  : "border-success"
                : "border-danger"
            }`}
        >
          <Card.Header
            className={`text-center 
            ${
              isLoading
                ? "border-info"
                : !error
                ? amountDue > 0
                  ? "border-warning bg-warning text-dark"
                  : "border-success bg-success"
                : "border-danger"
            }`}
          >
            <Card.Title>Outstanding</Card.Title>
          </Card.Header>
          <Card.Body>
            <Col sm={12}>
              <h3 className="text-center">
                {isLoading ? (
                  <Bars
                    style={{ margin: "0px", height: "24px" }}
                    className="spinner-size"
                  />
                ) : (
                  <>
                    {amountDue > 0 ? (
                      <>Ƶ {amountDue.toLocaleString()}</>
                    ) : (
                      <>No Payment Required</>
                    )}
                  </>
                )}
              </h3>
              <br />
              <InvPaymentDetail />
            </Col>
          </Card.Body>
        </Card>
      </div>
      <div className="w-25 pe-3 pb-1 ps-1">
        <Card className="h-100">
          <Card.Header className="text-center">
            <Card.Title>Key</Card.Title>
          </Card.Header>
          <Card.Body>
            <table className="table text-center mb-0">
              <tbody>
                <tr>
                  <td className="bg-info bg-opacity-25">Paid</td>
                </tr>
                <tr>
                  <td className="">Outstanding</td>
                </tr>
                <tr>
                  <td className="bg-danger bg-opacity-25">Overdue</td>
                </tr>
              </tbody>
            </table>
          </Card.Body>
        </Card>
      </div>
    </Row>
  );
};

export default InvMenu;
