import React from "react";
import { Col } from "react-bootstrap";
import { Panel } from "react-bootstrap";

const InvHeader = () => {

  return (
    <Panel>
      <Panel.Body>
        <Col xs={12} className="flex">
          <div className="child">
            <h1 className="text-center" style={{ margin: 0 }}>Alliance Contributions</h1>
          </div>
          
        </Col>
      </Panel.Body>
    </Panel>
  );
};

export default InvHeader;
