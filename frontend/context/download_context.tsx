// DownloadContext.js
import React, { createContext, useContext, useState } from "react";

const DownloadContext = createContext({
  downloadStatus: {
    isActive: false,
    progress: 0,
    filename: "",
    completed: false,
    error: false,
    downloadUrl: null,
  },
  setDownloadStatus: (status: any) => {},
});

export const useDownload = () => {
  const context = useContext(DownloadContext);
  if (!context) {
    throw new Error("useDownload must be used within an DownloadProvider");
  }
  return context;
};

export const DownloadProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [downloadStatus, setDownloadStatus] = useState({
    isActive: false,
    progress: 0,
    filename: "",
    completed: false,
    error: false,
    downloadUrl: null,
  });

  return (
    <DownloadContext.Provider value={{ downloadStatus, setDownloadStatus }}>
      {children}
    </DownloadContext.Provider>
  );
};
