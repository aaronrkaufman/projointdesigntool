import React, { FC, useEffect, useState } from "react";

import styles from "./preview__mcq.module.css";
import { SettingsRadioGroup } from "@/components/settings/__radio-group/settings__radio-group";

export interface PreviewMcqProps {
  refresh: boolean;
}

export const PreviewMcq: FC<PreviewMcqProps> = ({ refresh }) => {
  return (
    <div className={styles.preview__mcq}>
      <SettingsRadioGroup
        //   @ts-ignore
        key={refresh}
        options={["Profile 1", "Profile 2"]}
        defaultValue={""}
      />
    </div>
  );
};
