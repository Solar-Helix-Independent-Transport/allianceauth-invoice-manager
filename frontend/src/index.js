import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
import React from "react";
import { render } from "react-dom";
import InvHeader from "./components/InvHeader";
import InvMenu from "./components/InvMenu";
import { QueryClient, QueryClientProvider } from "react-query";
import InvUnpaid from "./components/InvUnpaid";
import InvVisible from "./components/InvVisible";

TimeAgo.addDefaultLocale(en);

const queryClient = new QueryClient();


const InvoicesView = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <InvHeader></InvHeader>
      <InvMenu></InvMenu>
      <InvUnpaid></InvUnpaid>
      <InvVisible></InvVisible>
    </QueryClientProvider>
  );
};

const appDiv = document.getElementById("root");
render(<InvoicesView />, appDiv);
