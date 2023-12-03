// "use client";

import { Header } from "../../../components/header";
import styles from "../../../styles/page.module.css";
import { Sidebar } from "../../../components/sidebar";
import { SurveyContainer } from "../../../components/survey/survey.container";
import { IDocument } from "../../../components/documents/document";
import { DocumentContext } from "../../../context/document_context";
import { useContext, useEffect, useState } from "react";
import Preview, { IPreview } from "../../../components/preview/preview";

import { GetServerSideProps } from "next";
import { useAttributes } from "../../../context/attributes_context";
import { getPreview } from "../../../services/api";

interface IServerProps {
  params: {
    document: string;
  };
}

function PreviewPage({ params }: IServerProps) {
  const documentName = decodeURIComponent(params.document as string);
  // console.log(documentName);
  const { setCurrentDoc } = useContext(DocumentContext);

  const { attributes } = useAttributes();

  const [profiles, setProfiles] = useState<IPreview | null>(null);

  const [refresh, setRefresh] = useState<boolean>(true);

  const previewData = async () => {
    const previews = await getPreview(attributes);
    setProfiles({
      attributes: attributes.map((el) => el.name),
      previews: previews,
    });
    console.log(previews);
  };

  useEffect(() => {
    setCurrentDoc(documentName);
    // console.log("whatis happening", currentDoc)
  }, [documentName]);

  useEffect(() => {
    previewData();
  }, [attributes]);

  useEffect(() => {
    if (refresh) {
      previewData();
      setRefresh(false);
    }
  }, [refresh]);

  return (
    <>
      <Header></Header>

      <main className={styles.main}>
        <Sidebar active={documentName} />
        {/* <SurveyContainer /> */}
        {profiles ? <Preview {...profiles} setRefresh={setRefresh} /> : ""}
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

export default PreviewPage;
