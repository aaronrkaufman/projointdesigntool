import { Header } from "@/components/header";
import styles from "../../profile/page.module.css";
import { Sidebar } from "@/components/sidebar";
import { SurveyContainer } from "@/components/survey/survey.container";
import { IDocument } from "@/components/documents/document";
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
  const documentName = params.document as string;
  console.log(documentName)

  // const documentData = await fetchDocumentData(documentName);

  // if (!documentData) {
  //   // Throw a 404 error if the document is not found
  //   throw new Response('Not Found', { status: 404 });
  // }
  return (
    <>
      <Header></Header>
      <main className={styles.main}>
        <Sidebar active={1} />
        <SurveyContainer />
      </main>
    </>
  );
}
