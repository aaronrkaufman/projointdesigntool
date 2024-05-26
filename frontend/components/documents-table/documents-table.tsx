import React, { FC } from "react";

import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Link from "next/link";
import styles from "./documents-table.module.css";
import { FileAdd, FileIcon } from "../ui/icons";
import { useRouter } from "next/router";
import { v4 as uuidv4 } from "uuid";
import { useAttributes } from "@/context/attributes_context";
import { columns } from "./__columns/documents-table__columns";
import { Button } from "../ui/button";
import { DocumentData, fetchDocuments } from "./documents-table.constants";

export interface DocumentsTableProps {}

export const DocumentsTable: FC<DocumentsTableProps> = ({}) => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const { storageChanged, setStorageChanged } = useAttributes();

  const [documents, setDocuments] = React.useState<DocumentData[]>([]);

  React.useEffect(() => {
    setDocuments(fetchDocuments());
  }, [storageChanged]);

  const router = useRouter();

  const handleAddDoc = () => {
    const uniqueId = uuidv4();
    const dataToSave = {
      attributes: [],
      lastEdited: new Date(), // Update last edited time
      name: "Untitled",
      restrictions: [],
    };
    localStorage.setItem(`attributes-${uniqueId}`, JSON.stringify(dataToSave));
    setStorageChanged((prev) => prev + 1);
    router.push(`/${encodeURIComponent(uniqueId)}`);
  };

  return (
    <section className={styles.table}>
      <div className={styles.tableContainer}>
        <div className={styles.top}>
          <div className={styles.docName}>
            <h2>Surveys</h2>
          </div>
          <Button
            text="New survey"
            icon={<FileAdd stroke="var(--white)" />}
            onClick={handleAddDoc}
          />
        </div>
        <Paper sx={{ width: "100%" }}>
          <TableContainer sx={{ maxHeight: 900 }}>
            <Table stickyHeader aria-label="sticky table">
              <TableHead>
                <TableRow>
                  {columns.map((column) => (
                    <TableCell
                      key={column.id}
                      align={column.align}
                      style={{ top: 0, minWidth: column.minWidth }}
                    >
                      <p>{column.label}</p>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {documents
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row) => {
                    return (
                      <Link
                        href={`/${encodeURIComponent(row.id)}`}
                        key={row.id}
                      >
                        <TableRow
                          hover
                          role="checkbox"
                          tabIndex={-1}
                          key={row.date}
                        >
                          {columns.map((column) => {
                            const value = row[column.id];
                            return (
                              <TableCell key={column.id} align={column.align}>
                                {column.id === "name" ? (
                                  <div className={styles.file}>
                                    <FileIcon stroke="var(--dark-blue-h)" />
                                    <p className={styles.table_docName}>
                                      {value}
                                    </p>
                                  </div>
                                ) : column.format &&
                                  typeof value === "number" ? (
                                  <p>{column.format(value)}</p>
                                ) : (
                                  <p>{value}</p>
                                )}
                              </TableCell>
                            );
                          })}
                        </TableRow>
                      </Link>
                    );
                  })}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[10, 25, 100]}
            component="div"
            count={documents.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </div>
    </section>
  );
};
