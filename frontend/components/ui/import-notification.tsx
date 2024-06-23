import { useDownload } from "@/context/download_context";
import Box from "@mui/material/Box";
import styles from "./notification.module.css";
import { useEffect } from "react";
import { XIcon } from "./icons";

const ImportNotification = () => {
  const { downloadStatus, setDownloadStatus } = useDownload();

  if (!downloadStatus.isActive || !downloadStatus.import) return null;

  const handleClose = () => {
    setDownloadStatus((prev: any) => ({
      ...prev,
      downloadUrl: null,
      isActive: false,
      import: false,
      export: false,
      completed: false,
    }));
  };

  return (
    <Box className={styles.notification}>
      {downloadStatus.completed && (
        <>
          <div className={styles.downloadComplete}>
            <h4>Imported the file successfully! </h4>
            <div className={styles.close}>
              <XIcon onClick={handleClose} />
            </div>
          </div>
        </>
      )}
      {downloadStatus.error && <p>Error in download. Try again.</p>}
    </Box>
  );
};

export default ImportNotification;
