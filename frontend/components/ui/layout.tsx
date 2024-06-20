import React from "react";
import styles from "./ui.module.css";

import { LinearProgress } from "@mui/material";
import { Sidebar } from "../sidebar/sidebar";

const Layout = ({
  children,
  active,
  loading,
}: {
  children: React.ReactNode;
  active: string;
  loading: boolean;
}) => {
  return (
    <div className={styles.main}>
      <Sidebar active={active} />
      {loading ? <LinearProgress /> : children}
    </div>
  );
};

export default Layout;
