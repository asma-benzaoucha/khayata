import React, { useState } from "react";
import "../../style/shoppingStyle/ProductCard.css";
import { useNavigate } from 'react-router-dom';
import Popupimages from "../generalComponents/Popupimages"; // Assurez-vous que le chemin est correct

// Icônes de flèche personnalisées
const ArrowRight = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ArrowLeft = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export default function ProductCard({ product }) {
  const navigate = useNavigate();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showPopup, setShowPopup] = useState(false); // État pour contrôler l'affichage du popup
  
  const goToform = () => {
    navigate("/shopping/acheter", {
      state: {
        product: {
          ...product,
          currentImage: product.images[currentImageIndex],
          code: product.code,//ici procuct.code et product.variants sont deja recu à partir de ...product
          variants: product.variants
        }
      }
    });
  };

  // Fonction pour ouvrir le popup
  const openImagePopup = () => {
    setShowPopup(true);
  };

  // Fonction pour fermer le popup
  const closeImagePopup = () => {
    setShowPopup(false);
  };

  // Préparer les images - compatibilité ascendante
  const images = product.images || [product.image];
  
  // Vérifier si le produit a plusieurs images
  const hasMultipleImages = images.length > 1;

  // Aller à l'image suivante
  const nextImage = (e) => {
    e.stopPropagation();
    setCurrentImageIndex((prevIndex) => 
      prevIndex === images.length - 1 ? 0 : prevIndex + 1
    );
  };

  // Aller à l'image précédente
  const prevImage = (e) => {
    e.stopPropagation();
    setCurrentImageIndex((prevIndex) => 
      prevIndex === 0 ? images.length - 1 : prevIndex - 1
    );
  };

  return (
    <>
      <div className="shopping-product-card">
        <div className="shopping-product-img-container" onClick={openImagePopup}>
          <img 
            src={images[currentImageIndex]} 
            alt={product.title} 
            className="shopping-product-image" 
          />
          
          {/* Afficher les boutons de navigation seulement s'il y a plusieurs images */}
          {hasMultipleImages && (
            <>
              <button className="shopping-nav-btn shopping-prev-btn" onClick={prevImage}>
                <ArrowLeft />
              </button>
              <button className="shopping-nav-btn shopping-next-btn" onClick={nextImage}>
                <ArrowRight />
              </button>
              
              {/* Indicateurs de position (points) */}
              <div className="shopping-image-indicators">
                {images.map((_, index) => (
                  <span 
                    key={index} 
                    className={`shopping-indicator ${index === currentImageIndex ? 'shopping-indicator-active' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      setCurrentImageIndex(index);
                    }}
                  ></span>
                ))}
              </div>
            </>
          )}
        </div>
        
        <div className="shopping-product-header">
          <h3 className="shopping-product-title">{product.title}</h3>
          <p className="shopping-product-price">{product.price + " دج"}</p>
        </div>

        <p className="shopping-product-sizes">
          <span>المقاسات:</span>
          {product.sizes.map((size, idx) => (
            <span key={idx} className="shopping-size-item">{size}</span>
          ))}
        </p>

        <button className="shopping-buy-btn" onClick={goToform}>احصل عليه</button>
      </div>

      {/* Afficher le popup lorsque showPopup est true */}
      {showPopup && (
        <Popupimages
          images={images}
          initialIndex={currentImageIndex}
          onClose={closeImagePopup}
        />
      )}
    </>
  );
}