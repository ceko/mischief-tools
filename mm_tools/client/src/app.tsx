import React from "react";
import logo from "./logo.svg";
import "./styles/app.scss";
import { Header } from "./components";
import { PriorityManagementPage } from "./pages";
import { APIContext } from "./context";

function App() {
  return (
    <div>
      <Header />
      <div className="page-wrap">
        <PriorityManagementPage />
      </div>
    </div>
  );
}

export default App;
