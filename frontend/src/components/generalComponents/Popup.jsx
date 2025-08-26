import React, { useEffect } from "react";
import { IoClose } from "react-icons/io5";
import '../../style/generalStyle/Popup.css'

export default function Popup({
  title = "",
  iconPopup = null,
  sousTitre = "",
  contenu = null,
  buttonTexte = "Confirmer",
  onClose = () => {},
  onConfirm = () => {},
  showButton = true,
  colorbackgroundTitleSousTitle = "",
}) {
  
  useEffect(() => {
    // Empêcher le défilement du body quand le popup est ouvert
    document.body.classList.add('popup-open');
    
    return () => {
      document.body.classList.remove('popup-open');
    };
  }, []);

  const handleClose = (e) => {
    if (e.target === e.currentTarget || e.target.closest('.iconsortirpopup')) {
      onClose();
    }
  };

  return (
    <div className="blurbackground" onClick={handleClose}>
      <div className="containerpopup">
        <div 
          className="containerheaderpopup" 
          style={{backgroundColor: colorbackgroundTitleSousTitle}}
        >
          {/* Bouton de fermeture */}
          <div className="iconsortirpopup" onClick={onClose}>
            <IoClose size={24} />
          </div>

          {/* Icone (centrée) */}
          {iconPopup && (
            <div className="iconpopup">
              <img src={iconPopup} alt="icone popup" className="popup-icon" />
            </div>
          )}

          {/* Titre */}
          <div className="titrepopup">
            {title}
          </div>

          {/* Sous-titre */}
          {sousTitre && (
            <div className="soustitrepopup">
              {sousTitre}
            </div>
          )}
        </div>

        {/* Contenu */}
        <div className="contenupopup">
          {typeof contenu === "string" ? (
            <p className="contentpopup">{contenu}</p>
          ) : (
            contenu
          )}
        </div>

        {/* Bouton d'action */}
        {showButton && (
          <button
            className="bouttonpopup"
            onClick={onConfirm}
          >
            {buttonTexte}
          </button>
        )}
      </div>
    </div>
  );
}