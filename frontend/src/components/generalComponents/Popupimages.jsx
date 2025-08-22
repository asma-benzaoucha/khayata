import React, { useState, useEffect } from "react";
import { X } from "lucide-react";
import "../../style/generalStyle/Popupimages.css";

// Définition des nouvelles icônes ArrowLeft et ArrowRight
const ArrowRight = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
    <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ArrowLeft = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
    <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const Popupimages = ({
  images = [],
  colorbackgroundTitleSousTitle = "rgba(255, 255, 255, 0.8)",
  onClose
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const [transitionDirection, setTransitionDirection] = useState('next');
  const [isZoomed, setIsZoomed] = useState(false);

  // Vérifier la taille de l'écran pour déterminer le mode d'affichage
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  // Navigation entre les images avec effet de zoom
  const goToPrevious = () => {
    if (images.length <= 1) return; // Empêche la navigation s'il n'y a qu'une image
    setTransitionDirection('prev');
    setIsZoomed(true);
    
    setTimeout(() => {
      setCurrentIndex((prevIndex) => 
        prevIndex === 0 ? images.length - 1 : prevIndex - 1
      );
      setIsZoomed(false);
    }, 150);
  };

  const goToNext = () => {
    if (images.length <= 1) return; // Empêche la navigation s'il n'y a qu'une image
    setTransitionDirection('next');
    setIsZoomed(true);
    
    setTimeout(() => {
      setCurrentIndex((prevIndex) => 
        prevIndex === images.length - 1 ? 0 : prevIndex + 1
      );
      setIsZoomed(false);
    }, 150);
  };

  // Navigation au clic sur un indicateur
  const goToImage = (index) => {
    if (images.length <= 1) return; // Empêche la navigation s'il n'y a qu'une image
    setTransitionDirection(index > currentIndex ? 'next' : 'prev');
    setIsZoomed(true);
    
    setTimeout(() => {
      setCurrentIndex(index);
      setIsZoomed(false);
    }, 150);
  };

  // Gestion du swipe sur mobile
  const [touchStart, setTouchStart] = useState(0);
  const [touchEnd, setTouchEnd] = useState(0);

  const handleTouchStart = (e) => {
    if (images.length <= 1) return; // Empêche le swipe s'il n'y a qu'une image
    setTouchStart(e.targetTouches[0].clientX);
  };

  const handleTouchMove = (e) => {
    if (images.length <= 1) return; // Empêche le swipe s'il n'y a qu'une image
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const handleTouchEnd = () => {
    if (images.length <= 1) return; // Empêche le swipe s'il n'y a qu'une image
    if (touchStart - touchEnd > 50) {
      // Swipe gauche
      goToNext();
    } else if (touchEnd - touchStart > 50) {
      // Swipe droit
      goToPrevious();
    }
  };

  if (images.length === 0) return null;

  return (
    <div className="popup-blur-background">
      <div className="popup-container">
        <div 
          className="popup-header"
          style={{ backgroundColor: colorbackgroundTitleSousTitle }}
        >
          <button className="close-button" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        
        <div className="popup-content-wrapper">
          {/* Icônes de navigation pour desktop - masquées si une seule image */}
          {!isMobile && images.length > 1 && (
            <>
              <button className="desktop-nav-button left-nav-button" onClick={goToPrevious}>
                <ArrowLeft />
              </button>
              
              <button className="desktop-nav-button right-nav-button" onClick={goToNext}>
                <ArrowRight />
              </button>
            </>
          )}
          
          <div className="popup-content">
            {/* Version Desktop - Affichage de l'image principale */}
            {!isMobile && (
              <div className="desktop-gallery">
                <div className="image-wrapper main-image">
                  <img 
                    src={images[currentIndex]} 
                    alt="Main" 
                    className={`${isZoomed ? 'zoom-out' : 'zoom-in'} slide-${transitionDirection}`}
                    key={currentIndex}
                  />
                </div>
              </div>
            )}
            
            {/* Version Mobile - Affichage d'une seule image */}
            {isMobile && (
              <div 
                className="mobile-gallery"
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={handleTouchEnd}
              >
                <div className="mobile-image-wrapper">
                  <img 
                    src={images[currentIndex]} 
                    alt="Mobile view" 
                    className={`${isZoomed ? 'zoom-out' : 'zoom-in'} slide-${transitionDirection}`}
                    key={currentIndex}
                  />
                </div>
                
                {/* Boutons de navigation mobile - masqués si une seule image */}
                {images.length > 1 && (
                  <>
                    <button className="nav-button prev-button" onClick={goToPrevious}>
                      <ArrowLeft />
                    </button>
                    
                    <button className="nav-button next-button" onClick={goToNext}>
                      <ArrowRight />
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
        
        {/* Indicateurs de navigation - masqués si une seule image */}
        {images.length > 1 && (
          <div className="navigation-indicators">
            {images.map((_, index) => (
              <button
                key={index}
                className={`indicator ${index === currentIndex ? 'active' : ''}`}
                onClick={() => goToImage(index)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Popupimages;