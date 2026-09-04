import { useEffect, useRef, useState } from "react";
import { Send, Mic, MicOff } from "lucide-react";

function QuestionBox({ onAnswer, disabled }) {
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState("");

  const recognitionRef = useRef(null);

  // -----------------------------
  // VOICE RECOGNITION SETUP
  // -----------------------------
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      return;
    }

    const recognition = new SpeechRecognition();

    // Voice settings
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";
    recognition.maxAlternatives = 1;

    // When microphone starts
    recognition.onstart = () => {
      setListening(true);
      setError("");
    };

    // When speech is converted to text
    recognition.onresult = (event) => {
      let transcript = "";

      // Read the latest result
      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        if (event.results[i].isFinal) {
          transcript += event.results[i][0].transcript;
        }
      }

      transcript = transcript.trim();

      if (!transcript) {
        return;
      }

      // Clean extra spaces
      transcript = transcript.replace(/\s+/g, " ");

      setQuestion((prev) => {
        const previousText = prev.trim();

        if (previousText) {
          return `${previousText} ${transcript}`;
        }

        return transcript;
      });
    };

    // Voice recognition errors
    recognition.onerror = (event) => {
      setListening(false);

      if (event.error === "not-allowed") {
        setError(
          "Microphone permission was denied. Please allow microphone access in Chrome."
        );
      } else if (event.error === "no-speech") {
        setError(
          "I didn't hear anything. Please try speaking again."
        );
      } else if (event.error === "audio-capture") {
        setError(
          "No microphone was detected. Please check your microphone."
        );
      } else if (event.error === "network") {
        setError(
          "Voice recognition could not connect. Please check your internet connection."
        );
      } else {
        setError(
          "Voice input failed. Please try again."
        );
      }
    };

    // Recognition finished
    recognition.onend = () => {
      setListening(false);
    };

    recognitionRef.current = recognition;

    // Cleanup
    return () => {
      recognition.stop();
    };
  }, []);

  // -----------------------------
  // START / STOP VOICE INPUT
  // -----------------------------
  const handleVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        "Voice input is not supported in this browser. Please use Google Chrome."
      );
      return;
    }

    if (!recognitionRef.current) {
      setError(
        "Voice recognition is not available. Please refresh the page and try again."
      );
      return;
    }

    // Stop listening
    if (listening) {
      recognitionRef.current.stop();
      setListening(false);
      return;
    }

    setError("");

    try {
      recognitionRef.current.start();
    } catch (err) {
      console.log("Speech recognition error:", err);
    }
  };

  // -----------------------------
  // ASK QUESTION
  // -----------------------------
  const handleAsk = async () => {
    const cleanedQuestion = question
      .trim()
      .replace(/\s+/g, " ");

    if (!cleanedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setAsking(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: cleanedQuestion,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail ||
            "Unable to answer the question."
        );
      }

      // Send answer to App.jsx
      onAnswer(data);

      // Clear question after successful answer
      setQuestion("");
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong. Please try again."
      );
    } finally {
      setAsking(false);
    }
  };

  // -----------------------------
  // ENTER KEY
  // -----------------------------
  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleAsk();
    }
  };

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <section className="question-section">

      <div className="question-header">
        <div>
          <h3>Ask about your document</h3>

          <p>
            Ask a question about the earnings report
            or transcript.
          </p>
        </div>
      </div>

      <div className="question-box">

        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="e.g. What was the company's revenue this quarter?"
          disabled={disabled || asking}
          rows={3}
        />

        <div className="question-actions">

          {/* VOICE BUTTON */}
          <button
            className={`voice-btn ${
              listening ? "listening" : ""
            }`}
            type="button"
            onClick={handleVoiceInput}
            disabled={disabled || asking}
            title={
              listening
                ? "Stop listening"
                : "Ask using your voice"
            }
          >
            {listening ? (
              <MicOff size={18} />
            ) : (
              <Mic size={18} />
            )}
          </button>

          {/* ASK BUTTON */}
          <button
            className="ask-btn"
            type="button"
            onClick={handleAsk}
            disabled={
              disabled ||
              asking ||
              !question.trim()
            }
          >
            {asking ? (
              "Thinking..."
            ) : (
              <>
                Ask Question
                <Send size={16} />
              </>
            )}
          </button>

        </div>
      </div>

      {/* LISTENING MESSAGE */}
      {listening && (
        <p className="voice-status">
          🎙️ Listening... Ask your question.
        </p>
      )}

      {/* ERROR MESSAGE */}
      {error && (
        <p className="question-error">
          {error}
        </p>
      )}

    </section>
  );
}

export default QuestionBox;