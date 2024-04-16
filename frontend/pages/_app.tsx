import "../styles/globals.css";
import type { AppProps } from "next/app";
import { DocProvider } from "../context/document_context";
import AttributeProvider from "../context/attributes_context";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <DocProvider>
      <AttributeProvider>
        <Component {...pageProps} />
      </AttributeProvider>
    </DocProvider>
  );
}

export default MyApp;
