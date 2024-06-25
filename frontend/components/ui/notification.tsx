import { useDownload } from "@/context/download_context";
import Box from "@mui/material/Box";
import styles from "./notification.module.css";
import { useEffect } from "react";
import { XIcon } from "./icons";

const DownloadNotification = () => {
  const { downloadStatus, cleanDownloadStatus } = useDownload();

  useEffect(() => {
    return () => {
      if (downloadStatus.downloadUrl) {
        window.URL.revokeObjectURL(downloadStatus.downloadUrl);
      }
    };
  }, [downloadStatus.downloadUrl]);

  if (!downloadStatus.export) return null;
  if (!downloadStatus.isActive) return null;

  const handleDownloadClick = () => {
    if (!downloadStatus.downloadUrl) return;

    const link = document.createElement("a");
    link.href = downloadStatus.downloadUrl;
    link.setAttribute("download", downloadStatus.filename);
    document.body.appendChild(link);
    link.click();

    setTimeout(() => {
      cleanDownloadStatus();
    }, 2000);

    link.remove();
  };

  return (
    <Box className={styles.notification}>
      {!downloadStatus.completed && !downloadStatus.error && (
        <h4>Downloading: {downloadStatus.filename}</h4>
      )}
      {downloadStatus.completed && (
        <>
          <div className={styles.downloadComplete}>
            <h4>Download complete! </h4>
            <div className={styles.close}>
              <XIcon onClick={cleanDownloadStatus} />
            </div>
          </div>
          <p>
            Click{" "}
            <a className={styles.link} href="#" onClick={handleDownloadClick}>
              here
            </a>{" "}
            if the file didn&#39;t start downloading.
          </p>
        </>
      )}
      {downloadStatus.error && (
        <div className={styles.downloadComplete}>
          <h4>Error in download {downloadStatus.errorMessage}. Try again.</h4>
          <div className={styles.close}>
            <XIcon onClick={cleanDownloadStatus} />
          </div>
        </div>
      )}
    </Box>
  );
};

export default DownloadNotification;
