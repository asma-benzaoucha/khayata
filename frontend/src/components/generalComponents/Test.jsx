import React, { useState } from "react";
import Popupimages from "./Popupimages";
import { Image, Settings } from "lucide-react";

// Exemple de données d'images
const sampleImages = [
  "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
  "https://images.unsplash.com/photo-1452570053594-1b985d6ea890",
  "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05",
  "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07",
  "https://images.unsplash.com/photo-1501785888041-af3ef285b470"
];

const Test = () => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [selectedImages, setSelectedImages] = useState(sampleImages);
  const [backgroundColor, setBackgroundColor] = useState("rgba(255, 255, 255, 0.8)");
  const [customImages, setCustomImages] = useState("");

  const handleOpenPopup = () => {
    setIsPopupOpen(true);
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  const handleApplyCustomImages = () => {
    if (customImages.trim()) {
      const imagesArray = customImages.split(',').map(url => url.trim());
      setSelectedImages(imagesArray);
    }
  };

  const handleResetImages = () => {
    setSelectedImages(sampleImages);
    setCustomImages("");
  };

  return (
    <div className="popup-tester">
      <header className="tester-header">
        <h1>Test du Composant PopupImages</h1>
        <p>Cliquez sur le bouton ci-dessous pour ouvrir la popup d'images</p>
      </header>

      <div className="tester-controls">
        <div className="control-group">
          <h3><Settings size={20} /> Paramètres</h3>
          
          <div className="input-group">
            <label>Couleur d'arrière-plan de l'en-tête:</label>
            <div className="color-options">
              {[
                "rgba(0, 0, 0, 0.8)",
                "rgba(25, 118, 210, 0.8)",
                "rgba(56, 142, 60, 0.8)",
                "rgba(245, 124, 0, 0.8)",
                "rgba(194, 24, 91, 0.8)"
              ].map(color => (
                <button
                  key={color}
                  className={`color-option ${backgroundColor === color ? 'active' : ''}`}
                  style={{ backgroundColor: color }}
                  onClick={() => setBackgroundColor(color)}
                />
              ))}
            </div>
          </div>

          <div className="input-group">
            <label>Images personnalisées (URLs séparées par des virgules):</label>
            <textarea
              value={customImages}
              onChange={(e) => setCustomImages(e.target.value)}
              placeholder="https://exemple.com/image1.jpg, https://exemple.com/image2.jpg"
              rows={3}
            />
            <div className="button-group">
              <button onClick={handleApplyCustomImages}>Appliquer</button>
              <button onClick={handleResetImages}>Réinitialiser</button>
            </div>
          </div>
        </div>
      </div>

      <div className="tester-preview">
        <div className="image-grid">
          {selectedImages.map((img, index) => (
            <div key={index} className="image-thumbnail">
              <img src={img} alt={`Preview ${index}`} />
              <span>Image {index + 1}</span>
            </div>
          ))}
        </div>

        <button className="open-popup-btn" onClick={handleOpenPopup}>
          <Image size={20} />
          Ouvrir la Popup d'Images
        </button>
      </div>

      {isPopupOpen && (
        <Popupimages
          images={selectedImages}
          colorbackgroundTitleSousTitle={backgroundColor}
          onClose={handleClosePopup}
        />
      )}

      <style jsx>{`
        .popup-tester {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .tester-header {
          text-align: center;
          margin-bottom: 30px;
          padding: 20px;
          background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
          color: white;
          border-radius: 12px;
        }
        
        .tester-header h1 {
          margin: 0 0 10px 0;
          font-size: 2.2rem;
        }
        
        .tester-header p {
          margin: 0;
          opacity: 0.9;
        }
        
        .tester-controls {
          background-color: #f8f9fa;
          padding: 20px;
          border-radius: 12px;
          margin-bottom: 30px;
        }
        
        .control-group h3 {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 0;
          color: #2c3e50;
        }
        
        .input-group {
          margin-bottom: 20px;
        }
        
        .input-group label {
          display: block;
          margin-bottom: 8px;
          font-weight: 500;
          color: #34495e;
        }
        
        .color-options {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
        }
        
        .color-option {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          border: 3px solid white;
          cursor: pointer;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .color-option:hover {
          transform: scale(1.1);
          box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .color-option.active {
          transform: scale(1.15);
          box-shadow: 0 0 0 3px #3498db;
        }
        
        textarea {
          width: 100%;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 6px;
          font-family: inherit;
          resize: vertical;
        }
        
        .button-group {
          display: flex;
          gap: 10px;
          margin-top: 10px;
        }
        
        .button-group button {
          padding: 10px 16px;
          border: none;
          border-radius: 6px;
          background-color: #3498db;
          color: white;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.2s;
        }
        
        .button-group button:hover {
          background-color: #2980b9;
        }
        
        .button-group button:last-child {
          background-color: #7f8c8d;
        }
        
        .button-group button:last-child:hover {
          background-color: #636e72;
        }
        
        .tester-preview {
          text-align: center;
        }
        
        .image-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
          gap: 15px;
          margin-bottom: 30px;
        }
        
        .image-thumbnail {
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 4px 8px rgba(0,0,0,0.1);
          transition: transform 0.2s;
        }
        
        .image-thumbnail:hover {
          transform: translateY(-5px);
        }
        
        .image-thumbnail img {
          width: 100%;
          height: 100px;
          object-fit: cover;
        }
        
        .image-thumbnail span {
          display: block;
          padding: 8px;
          background-color: #f1f2f6;
          font-size: 0.9rem;
        }
        
        .open-popup-btn {
          display: inline-flex;
          align-items: center;
          gap: 10px;
          padding: 14px 28px;
          background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
          color: white;
          border: none;
          border-radius: 50px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .open-popup-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 12px rgba(38, 117, 252, 0.3);
        }
        
        @media (max-width: 768px) {
          .image-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
          }
          
          .color-options {
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};

export default Test;