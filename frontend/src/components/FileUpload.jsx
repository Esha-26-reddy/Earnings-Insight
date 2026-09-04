import { useRef, useState } from "react";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";

function FileUpload({ onUploadSuccess }) {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);
    setMessage("");
    setError("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select an earnings document first.");
      return;
    }

    setUploading(true);
    setMessage("");
    setError("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail || "Unable to process this document."
        );
      }

      setMessage("Document uploaded successfully.");

      if (onUploadSuccess) {
        onUploadSuccess(data);
      }
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while uploading the document."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <section className="upload-section">

      <div className="upload-card">

        <div className="upload-icon">
          <Upload size={24} />
        </div>

        <h3>Upload an earnings document</h3>

        <p className="upload-description">
          Upload an earnings report or earnings call transcript
          to start asking questions.
        </p>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt,.csv"
          onChange={handleFileChange}
          hidden
        />

        <button
          className="choose-file-btn"
          onClick={() => fileInputRef.current.click()}
        >
          <FileText size={18} />
          Choose File
        </button>

        <p className="file-types">
          Supported formats: PDF, TXT, CSV
        </p>

        {selectedFile && (
          <div className="selected-file">

            <FileText size={20} />

            <div className="selected-file-info">
              <strong>{selectedFile.name}</strong>
              <span>
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </span>
            </div>

          </div>
        )}

        {selectedFile && (
          <button
            className="upload-btn"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? "Processing document..." : "Upload & Analyze"}
          </button>
        )}

        {message && (
          <div className="success-message">
            <CheckCircle size={17} />
            {message}
          </div>
        )}

        {error && (
          <div className="error-message">
            <AlertCircle size={17} />
            {error}
          </div>
        )}

      </div>

    </section>
  );
}

export default FileUpload;