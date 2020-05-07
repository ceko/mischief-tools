import React from "react";
import ReactDOM from "react-dom";
import App from "./app";

console.log(process.env.REACT_APP_API_ROOT);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
