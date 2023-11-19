"use client";

import { Header } from "../../components/header";
import styles from "../../styles/page.module.css";
import { Sidebar } from "../../components/sidebar";
import { SurveyContainer } from "../../components/survey/survey.container";
import { IDocument } from "../../components/documents/document";
import { DocProvider, DocumentContext } from "../../context/document_context";
import { useContext, useEffect } from "react";
import AttributeProvider from "../../context/attributes_context";
import { GetServerSideProps } from "next";
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

function DocumentPage({ params }: IServerProps) {
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

export const getServerSideProps: GetServerSideProps = async (context) => {
  const document = context.params?.document;

  // Check if 'document' is a string (or an array of strings if you allow that)
  if (typeof document !== "string") {
    // Handle the case where 'document' is not provided or is not a string
    return { notFound: true }; // Or redirect to another page
  }

  // You can perform server-side operations here, like fetching data based on the document name
  // ...

  // Then return the props
  return {
    props: {
      params: {
        document: document || "",
      },
    },
  };
};

export default DocumentPage;
