import React from "react";
import HeaderComponent  from "../header/component";
import BodyComponent  from "../body/component";

const DefaultLayoutComponent = (props) => {
  return (
    <div>
      <HeaderComponent/>
      <BodyComponent/>
    </div>
  )
};

export default DefaultLayoutComponent;
