import React, { FC } from "react";
import styles from "./settings__radio-group.module.css";
import { styled } from "@mui/material/styles";
import Radio, { RadioProps } from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";

const BpIcon = styled("span")(({ theme }) => ({
  borderRadius: "4px", // Changed from "50%" to "4px" for a more rectangular shape
  width: 20,
  height: 20,
  boxShadow:
    theme.palette.mode === "dark"
      ? "0 0 0 1px rgb(16 22 26 / 40%)"
      : "inset 0 0 0 1px rgba(16,22,26,.2), inset 0 -1px 0 rgba(16,22,26,.1)",
  backgroundColor: theme.palette.mode === "dark" ? "#394b59" : "#f5f8fa",
  backgroundImage:
    theme.palette.mode === "dark"
      ? "linear-gradient(180deg,hsla(0,0%,100%,.05),hsla(0,0%,100%,0))"
      : "linear-gradient(180deg,hsla(0,0%,100%,.8),hsla(0,0%,100%,0))",
  ".Mui-focusVisible &": {
    outline: "2px auto rgba(19,124,189,.6)",
    outlineOffset: 2,
  },
  "input:hover ~ &": {
    backgroundColor: theme.palette.mode === "dark" ? "#30404d" : "#ebf1f5",
  },
  "input:disabled ~ &": {
    boxShadow: "none",
    background:
      theme.palette.mode === "dark"
        ? "rgba(57,75,89,.5)"
        : "rgba(206,217,224,.5)",
  },
}));

const BpCheckedIcon = styled(BpIcon)({
  backgroundColor: "var(--blue)", // Solid fill color
  backgroundImage: "none", // Remove gradient for a solid fill
  "&::before": {
    display: "none", // Remove the inner circle
  },
  "input:hover ~ &": {
    backgroundColor: "var(--dark-blue-h)",
  },
});

// Inspired by blueprintjs
function BpRadio(props: RadioProps) {
  return (
    <Radio
      disableRipple
      color="default"
      checkedIcon={<BpCheckedIcon />}
      icon={<BpIcon />}
      {...props}
    />
  );
}

export interface SettingsRadioGroupProps {
  options: string[];
  defaultValue: string;
}

export const SettingsRadioGroup: FC<SettingsRadioGroupProps> = ({
  options,
  defaultValue,
}) => (
  <div className={styles.settings__radio_group}>
    <RadioGroup
      defaultValue={defaultValue}
      aria-labelledby="radio_button"
      name="radio_button"
    >
      {options.map((option) => (
        <FormControlLabel
          key={option}
          value={option}
          control={<BpRadio />}
          label={option}
          style={{ fontFamily: "Inter, sans-serif" }}
        />
      ))}
    </RadioGroup>
  </div>
);
