

interface Column {
  id: "name" | "date" | "attributesCount" | "restrictions";
  label: string;
  minWidth?: number;
  align?: "right";
  format?: (value: number) => string;
}

export const columns: Column[] = [
  { id: "name", label: "Survey name", minWidth: 180 },
  {
    id: "attributesCount",
    label: "Attributes",
    minWidth: 120,
    align: "right",
    format: (value: number) => value.toLocaleString("en-US"),
  },
  {
    id: "restrictions",
    label: "Restrictions",
    minWidth: 120,
    align: "right",
    format: (value: number) => value.toLocaleString("en-US"),
  },
  { id: "date", label: "Last modified", minWidth: 150, align: "right" },
];
