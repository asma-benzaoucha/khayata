import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import Popup from "../generalComponents/Popup";
import sorry from "../../assets/icons/sorry.png";
import ContentPopupSorry from "../talabiyatiComp/ContentPopupSorry";
import Popupimages from "../generalComponents/Popupimages"; // Import manquant
import "../../style/generalStyle/CommandCard.css";
export default function CommandCard({ 
  selectedImages = [],
  namecommand = "", 
  photobutton = ["", ""],
  date = ["", ""], 
  telephone = ["", ""], 
  prix = ["", ""], 
  nbpieces = ["", ""], 
  status = ["قيد التنفيذ", "#22C55E", ""],
  isCustom=false
}) { 
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 480);
  const [showPopup, setShowPopup] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 480);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const handleOpenPopup = () => {
    setIsPopupOpen(true);
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  return ( 
    <div className="CardContainer"> 
      <div className="sidedroit">
        <div className="line1"> 
          <div className="namecommand elemntcard"> 
            {namecommand}
            
           {isCustom &&(<div className="specialtext"> 
            مخصص
          </div> )}
          </div> 
          
          
          {/* Sur mobile: photo et status sur la même ligne */}
          {isMobile ? (
            <div className="photoStatusWrapper">
              <div className="photocommand elemntcard">
                <button className="photobutton" onClick={handleOpenPopup}>
                  {photobutton[0]}
                  <img src={photobutton[1]} alt="photocommand" className="imagefortalabiyati"/>
                </button>
                {isPopupOpen && (
                  <Popupimages
                  initialIndex={0} 
                    images={selectedImages}
                    onClose={handleClosePopup}
                  />
                )}
              </div>
              <div className="statusCommand"> 
                <button style={{backgroundColor: status[1]}} >
                  {status[0]}
                </button>
                {status[2] && (
                  <img 
                    className="iconRefuse" 
                    src={status[2]} 
                    alt="refuse"  
                    onClick={() => setShowPopup(true)}
                  /> 
                )}
                {showPopup && (
                  <Popup
                    title="نعتذر لك عزيزي العميل"
                    sousTitre="دعنا نوضح لك قواعد العمل وأسباب إلغاء الطلب"
                    iconPopup={sorry}
                    contenu={<ContentPopupSorry/>}
                    colorbackgroundTitleSousTitle="#F6EDD2"
                    buttonTexte="حسناً، فهمت"
                    onClose={() => setShowPopup(false)}
                    onConfirm={() => {
                      setShowPopup(false);
                      navigate('/mycommands');
                    }}
                  />
                )}
              </div> 
            </div>
          ) : (
            <>
              <div className="photocommand elemntcard">
                <button className="photobutton" onClick={handleOpenPopup}>
                  {photobutton[0]} 
                  <img src={photobutton[1]} alt="photocommand" />
                </button>
              </div>
              {isPopupOpen && (
                <Popupimages
                  images={selectedImages}
                  onClose={handleClosePopup}
                />
              )}
            </>
          )}
        </div> 

        <div className="line2"> 
          <div className="datecommand elemntcard">
            <img src={date[1]} alt="datecommand" />
            <span>{date[0]}</span>
          </div> 

          <div className="telephone elemntcard">
            <img src={telephone[1]} alt="telephone" />
            <span>{telephone[0]}</span>
          </div>


 {prix !== null && (
          <div className="prix elemntcard">
            <img src={prix[1]} alt="prix" /> 
            <span>{prix[0]}</span>
          </div>
)}
          <div className="nbpieces elemntcard">
            <img src={nbpieces[1]} alt="nbpieces" />
            <span>{nbpieces[0]}</span>
          </div>
        </div> 
      </div>

      {/* Status affiché seulement sur desktop/tablette */}
      {!isMobile && (
        <div className="sidegauche">
          <div className="statusCommand"> 
            <button style={{backgroundColor: status[1]}} >
              {status[0]}
            </button>
            {status[2] && (
              <img 
                className="iconRefuse" 
                src={status[2]} 
                alt="refuse"  
                onClick={() => setShowPopup(true)}
              />
            )}
            {showPopup && (
              <Popup
                title="نعتذر لك عزيزي العميل"
                sousTitre="دعنا نوضح لك قواعد العمل وأسباب إلغاء الطلب"
                iconPopup={sorry}
                contenu={<ContentPopupSorry/>}
                colorbackgroundTitleSousTitle="#F6EDD2"
                buttonTexte="حسناً ، فهمت"
                onClose={() => setShowPopup(false)}
                onConfirm={() => {
                  setShowPopup(false);
                  navigate('/mycommands');
                }}
              />
            )}
          </div> 
        </div>
      )}
    </div> 
  ); 
}