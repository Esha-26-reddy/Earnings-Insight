import { Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";

function AnswerCard({ answer, relevant }) {
  return (
    <section className="answer-section">
      <div className="answer-card">

        <div className="answer-header">
          <div className="answer-icon">
            <Sparkles size={18} />
          </div>

          <div>
            <h3>AI Answer</h3>

            <span>
              {relevant
                ? "Based on your uploaded document"
                : "Not related to the document"}
            </span>
          </div>
        </div>

        <div className="answer-content">
          <ReactMarkdown>
            {answer}
          </ReactMarkdown>
        </div>

      </div>
    </section>
  );
}

export default AnswerCard;