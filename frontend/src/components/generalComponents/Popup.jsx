import React from "react";
import { IoClose } from "react-icons/io5"; // icône de fermeture par défaut
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
  colorbackgroundTitleSousTitle="",
}) {
  return (
    <div className="blurbackground">
      <div className="containerpopup">
        <div className="containerheaderpopup" style={{backgroundColor:colorbackgroundTitleSousTitle}}>
        {/* Bouton de fermeture */}
        <div className="iconsortirpopup absolute top-4 right-4 cursor-pointer text-gray-500 hover:text-black">
          <IoClose size={24} onClick={onClose} />
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
