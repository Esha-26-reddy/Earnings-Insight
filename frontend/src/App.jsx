import { useState } from "react";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import QuestionBox from "./components/QuestionBox";
import AnswerCard from "./components/AnswerCard";
import SourceCard from "./components/SourceCard";

function App() {
  const [uploadedDocument, setUploadedDocument] = useState(null);
  const [answerData, setAnswerData] = useState(null);

  const handleUploadSuccess = (data) => {
    setUploadedDocument(data);
    setAnswerData(null);
  };

  const handleAnswer = (data) => {
    setAnswerData(data);
  };

  return (
    <div className="app">

      <Header />

      <main className="main">

        {/* HERO */}

        <section className="hero">

          <div className="hero-badge">
            <span>✦</span>
            Document Intelligence
          </div>

          <h2>
            Understand earnings calls
            <br />
            <span>in seconds.</span>
          </h2>

          <p>
            Upload an earnings report or call transcript
            and ask questions using natural language.
          </p>

        </section>


        {/* FILE UPLOAD */}

        <FileUpload
          onUploadSuccess={handleUploadSuccess}
        />


        {/* QUESTION BOX */}

        {uploadedDocument && (
          <QuestionBox
            onAnswer={handleAnswer}
            disabled={!uploadedDocument}
          />
        )}


        {/* ANSWER */}

        {answerData && (
          <AnswerCard
            answer={answerData.answer}
            relevant={answerData.relevant}
          />
        )}


        {/* SOURCES */}

        {answerData &&
          answerData.sources &&
          answerData.sources.length > 0 && (
            <SourceCard
              sources={answerData.sources}
            />
          )}

      </main>

    </div>
  );
}

export default App;