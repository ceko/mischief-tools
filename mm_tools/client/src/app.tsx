import React from "react";
import "./styles/app.scss";
import { Header } from "./components";
import { PriorityManagementPage } from "./pages";

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
