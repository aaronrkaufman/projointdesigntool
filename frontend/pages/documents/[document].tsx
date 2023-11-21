// "use client";

import { Header } from "../../components/header";
import styles from "../../styles/page.module.css";
import { Sidebar } from "../../components/sidebar";
import { SurveyContainer } from "../../components/survey/survey.container";
import { IDocument } from "../../components/documents/document";
import { DocumentContext } from "../../context/document_context";
import { useContext, useEffect } from "react";

import { GetServerSideProps } from "next";

interface IServerProps {
  params: {
    document: string;
  };
}

function DocumentPage({ params }: IServerProps) {
  const documentName = decodeURIComponent(params.document as string);
  // console.log(documentName);
  const { setCurrentDoc } = useContext(DocumentContext);

  useEffect(() => {
    setCurrentDoc(documentName);
    // console.log("whatis happening", currentDoc)
  }, [documentName]);

  return (
    <>
      <Header></Header>

      <main className={styles.main}>
        <Sidebar active={documentName} />
        <SurveyContainer />
      </main>
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
