import { useState } from "react";
import {
  FileText,
  ChevronDown,
  ChevronRight,
} from "lucide-react";

function getSourceTitle(content) {
  const text = content.toLowerCase();

  if (
    text.includes("consolidated statements") ||
    text.includes("income statement") ||
    text.includes("balance sheet") ||
    text.includes("cash flow")
  ) {
    return "Financial Statements";
  }

  if (
    text.includes("earnings results") ||
    text.includes("financial results") ||
    text.includes("revenue") ||
    text.includes("operating income")
  ) {
    return "Financial Results";
  }

  if (
    text.includes("prepared remarks") ||
    text.includes("management") ||
    text.includes("chief executive officer") ||
    text.includes("ceo")
  ) {
    return "Management Commentary";
  }

  return "Document Excerpt";
}

function SourceCard({ sources }) {
  const [openSource, setOpenSource] = useState(0);

  const toggleSource = (index) => {
    setOpenSource(
      openSource === index ? null : index
    );
  };

  return (
    <section className="source-section">

      <div className="sources-heading">
        <div>
          <h3>Sources</h3>
          <span>
            {sources.length} relevant sources
          </span>
        </div>
      </div>

      <div className="sources-list">

        {sources.map((source, index) => {
          const title = getSourceTitle(
            source.content
          );

          const isOpen = openSource === index;

          return (
            <div
              className={`source-card ${
                isOpen ? "source-open" : ""
              }`}
              key={index}
            >

              <button
                className="source-header"
                onClick={() =>
                  toggleSource(index)
                }
              >

                <div className="source-left">

                  <div className="source-icon">
                    <FileText size={17} />
                  </div>

                  <div className="source-title">

                    <strong>
                      {title}
                    </strong>

                    <span>
                      Source {index + 1}
                    </span>

                  </div>

                </div>

                <div className="source-chevron">
                  {isOpen ? (
                    <ChevronDown size={18} />
                  ) : (
                    <ChevronRight size={18} />
                  )}
                </div>

              </button>


              {isOpen && (
                <div className="source-details">

                  <p>
                    {source.content}
                  </p>

                  <div className="source-file">
                    <FileText size={13} />
                    {source.source}
                  </div>

                </div>
              )}

            </div>
          );
        })}

      </div>

    </section>
  );
}

export default SourceCard;