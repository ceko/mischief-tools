import React from "react";
import { API } from "./api";

export const APIContext = React.createContext(
  new API(process.env.REACT_APP_API_ROOT!)
);
