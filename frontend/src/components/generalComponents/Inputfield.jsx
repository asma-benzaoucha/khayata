import React, { useRef } from "react";
import "../../style/generalStyle/Inputfield.css";
import telecharger from "../../assets/icons/telecharger.png"

export default function InputField({
  caché = "",
  type = "text",
  placeholder = "",
  titre = "",
  down = false,
  downup = false,
  size = "default",
  value = "",
  onChange = () => {},
  onBlur,
  options = null,
  hasError = false,
  accept = "",
  multiple = false,
  uploadedFiles = [],
  onRemoveFile = () => {},
  inputRef = null
}) {
  const internalFileInputRef = useRef(null);
  const fileInputRef = inputRef || internalFileInputRef;

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    onChange(files);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    onChange(files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className={`input-field ${size === "oneline" ? "full-line" : "quarter-line"}`}>
      {titre && <label className="titre">{titre}</label>}

      <div className="input-wrapper">
        {options && Array.isArray(options) ? (
          <select
            className={`input-element ${options ? 'select-element' : ''} ${hasError ? 'error-border' : ''}`}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
            required
          >
            <option value="" disabled hidden>
              {placeholder}
            </option>
            {options.map((option, index) => (
              <option key={index} value={option.value || option}>
                {option.label || option}
              </option>
            ))}
          </select>
        ) : type === "file" ? (
          // NOUVEAU: Conteneur pour l'upload
          <div className="upload-container">
            {/* Zone d'upload */}
            <label 
              className="upload-zone"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <img src={telecharger} alt="upload" className="upload-icon" />
              <p className="upload-text">
                {multiple 
                  ? "اسحب وأفلت الملفات هنا أو انقر لاختيارها" 
                  : "اسحب وأفلت الملف هنا أو انقر لاختياره"
                }<br />
                {accept.includes("image") && accept.includes("pdf") 
                  ? "يُسمح بملفات PDF والصور" 
                  : accept.includes("image") 
                    ? "يُسمح بالصور فقط" 
                    : "يُسمح بملفات PDF فقط"
                }
              </p>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
                onBlur={onBlur}
                accept={accept || "image/*,application/pdf"}
                style={{ display: "none" }}
                multiple={multiple}
              />
            </label>

            {/* Aperçu des fichiers uploadés - MAINTENANT EN DESSOUS */}
            {uploadedFiles && uploadedFiles.length > 0 && (
              <div className="uploaded-files-container">
                <h4 className="files-title">الملفات المرفقة:</h4>
                <div className="files-list">
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="file-item">
                      <div className="file-info">
                        <span className="file-name">{file.name}</span>
                        <span className="file-size">({Math.round(file.size / 1024)} KB)</span>
                      </div>
                      <button 
                        type="button" 
                        className="remove-file-btn"
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          onRemoveFile(index);
                        }}
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <input
            type={type}
            placeholder={placeholder}
            className={`input-element ${hasError ? 'error-border' : ''}`}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
          />
        )}
      </div>
    </div>
  );
}