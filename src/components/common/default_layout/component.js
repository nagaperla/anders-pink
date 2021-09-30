import React from "react";
import HeaderComponent  from "../header/component";

const DefaultLayoutComponent = (props) => {
  return (
    <div>
      <HeaderComponent/>
      <div className="my-5 pt-3">
        {props.children}
      </div>
    </div>
  )
};

export default DefaultLayoutComponent;
