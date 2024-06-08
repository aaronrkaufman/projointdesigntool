import React, { FC, useEffect, useState } from "react";

import styles from "./preview__mcq.module.css";
import { SettingsRadioGroup } from "@/components/settings/__radio-group/settings__radio-group";
import { IProfile } from "../preview";

export interface PreviewMcqProps {
  refresh: boolean;
  options: IProfile[];
}

export const PreviewMcq: FC<PreviewMcqProps> = ({ refresh, options }) => {
  return (
    <div className={styles.preview__mcq}>
      <SettingsRadioGroup
        //   @ts-ignore
        key={refresh}
        options={options.map((option) => option.value)}
        defaultValue={""}
      />
    </div>
  );
};
