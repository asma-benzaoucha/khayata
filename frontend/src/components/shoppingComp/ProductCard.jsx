import React, { useState } from "react";
import "../../style/shoppingStyle/ProductCard.css";
import { useNavigate } from 'react-router-dom';

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
  
  const goToform = () => {
    navigate("/shopping/acheter");
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
    <div className="product-card">
      <div className="product-img-wrapper">
        <img 
          src={images[currentImageIndex]} 
          alt={product.title} 
          className="product-img" 
        />
        
        {/* Afficher les boutons de navigation seulement s'il y a plusieurs images */}
        {hasMultipleImages && (
          <>
            <button className="nav-btn prev-btn" onClick={prevImage}>
              <ArrowLeft />
            </button>
            <button className="nav-btn next-btn" onClick={nextImage}>
              <ArrowRight />
            </button>
            
            {/* Indicateurs de position (points) */}
            <div className="image-indicators">
              {images.map((_, index) => (
                <span 
                  key={index} 
                  className={`indicator ${index === currentImageIndex ? 'active' : ''}`}
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
      
      <div className="product-header">
        <h3 className="product-title">{product.title}</h3>
        <p className="product-price">{product.price}</p>
      </div>

      <p className="mysizes">
        <span>المقاسات:</span>
        {product.sizes.map((size, idx) => (
          <span key={idx} className="size">{size}</span>
        ))}
      </p>

  <button className="buy-btn" onClick={goToform}>احصل عليه</button>

    
    </div>
  );
}