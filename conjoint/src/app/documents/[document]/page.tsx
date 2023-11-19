"use client";

import { Header } from "@/components/header";
import styles from "../../profile/page.module.css";
import { Sidebar } from "@/components/sidebar";
import { SurveyContainer } from "@/components/survey/survey.container";
import { IDocument } from "@/components/documents/document";
import { DocProvider, DocumentContext } from "@/context/document_context";
import { useContext, useEffect } from "react";
import AttributeProvider from "@/context/attributes_context";
// Assuming you have a list of documents somewhere in your application
const documentsList: IDocument[] = [
  { name: "1", key: 1 },
  // ... other documents
];

interface IServerProps {
  params: {
    document: string;
  };
}

export default function DocumentPage({ params }: IServerProps) {
  const documentName = decodeURIComponent(params.document as string);
  // console.log(documentName);
  const { currentDoc, setCurrentDoc } = useContext(DocumentContext);

  useEffect(() => {
    setCurrentDoc(documentName);
    // console.log("whatis happening", currentDoc)
  }, [documentName]);

  // const documentData = await fetchDocumentData(documentName);

  // if (!documentData) {
  //   // Throw a 404 error if the document is not found
  //   throw new Response('Not Found', { status: 404 });
  // }
  return (
    <>
      <AttributeProvider>
        <Header></Header>

        <main className={styles.main}>
          <Sidebar active={documentName} />
          <SurveyContainer />
        </main>
      </AttributeProvider>
    </>
  );
}
