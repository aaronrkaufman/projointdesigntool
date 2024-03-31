// "use client";

import styles from "../../styles/page.module.css";
import { Sidebar } from "../../components/sidebar";
import { DocumentContext } from "../../context/document_context";
import { useContext, useEffect, useState } from "react";
import Preview, { IPreview } from "../../components/preview/preview";

import { GetServerSideProps } from "next";
import { useAttributes } from "../../context/attributes_context";
import { getPreview } from "../../services/api";

interface IServerProps {
  params: {
    document: string;
  };
}

function PreviewPage({ params }: IServerProps) {
  const documentID = decodeURIComponent(params.document as string);
  // console.log(documentName);
  const { setCurrentDoc, setCurrentDocID } = useContext(DocumentContext);

  useEffect(() => {
    const localData = localStorage.getItem(`attributes-${documentID}`);
    const parsedData = localData ? JSON.parse(localData) : {};
    const documentName = parsedData?.name;
    setCurrentDoc(documentName);
  }, []);

  useEffect(() => {
    setCurrentDocID(documentID);
    // console.log("whatis happening", currentDoc)
  }, [documentID]);

  const { attributes, restrictions, instructions } = useAttributes();

  const [profiles, setProfiles] = useState<IPreview | null>(null);

  const [refresh, setRefresh] = useState<boolean>(true);

  const previewData = async () => {
    // const previews = await getPreview(attributes, restrictions);
    const previews = await getPreview(attributes);
    setProfiles({
      attributes: attributes.map((el) => el.name),
      previews: previews,
      instructions: instructions,
    });
    // console.log("previews:", previews);
  };

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
      <main className={styles.main}>
        <Sidebar active={documentID} />
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
