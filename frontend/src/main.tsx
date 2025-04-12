import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
import React from "react";
import ReactDOM from "react-dom/client";
import InvHeader from "./components/InvHeader";
import InvMenu from "./components/InvMenu";
import { QueryClient, QueryClientProvider } from "react-query";
import InvUnpaid from "./components/InvUnpaid";
import InvVisible from "./components/InvVisible";
import "./index.css";

TimeAgo.addDefaultLocale(en);

const queryClient = new QueryClient();

const InvoicesView = () => {
  console.log("blah")
  return (
    <QueryClientProvider client={queryClient}>
      <InvHeader></InvHeader>
      <InvMenu></InvMenu>
      <InvUnpaid></InvUnpaid>
      <InvVisible></InvVisible>
    </QueryClientProvider>
  );
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <InvoicesView />
  </React.StrictMode>,
);
