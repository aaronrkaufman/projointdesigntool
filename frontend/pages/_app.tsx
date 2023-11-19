import "../styles/globals.css";
import type { AppProps } from "next/app";
import { DocProvider } from "../context/document_context";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <DocProvider>
      <Component {...pageProps} />
    </DocProvider>
  );
}

export default MyApp;
