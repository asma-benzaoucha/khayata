import '../../style/landingStyle/C1landing.css';
import down from '../../assets/icons/down.png';
import pub from "../../assets/icons/publ.png";
import { useNavigate } from "react-router-dom";
import { handleNavigationWithAuth } from "../../apimanagement/authUtils";

export default function C1landing() {
  const navigate = useNavigate();

  const handleProtectedNavigation = async (path) => {
    try {
      await handleNavigationWithAuth(navigate, path, false);
    } catch (error) {
      console.error('Navigation error:', error);
    }
  };
  
  const goToShoppingOrLogin = () => {
    handleProtectedNavigation("/shopping");
  }
  
  const goToSpecialOrLogin = () => {
    handleProtectedNavigation("/special");
  }

  // Fonction pour faire défiler la page vers le bas
  const scrollDown = () => {
    window.scrollBy({
      top: 500, // Défiler de 600px vers le bas
      behavior: 'smooth' // Animation fluide
    });
  }
  
  return (
    <section className="landing-section" id="home">
      <div className="landing-content">
        <h1 className="landing-title">متجر التصاميم الفريدة</h1>
        <p className="landing-subtitle">
          اختر من مجموعة حصرية من التصاميم الجاهزة أو اطلب تصميماً مخصصاً يناسب ذوقك.
        </p>
        <div className="landing-buttons">
          <button className="shop-button" onClick={goToShoppingOrLogin}>تسوق الآن</button>
          <button className="custom-button" onClick={goToSpecialOrLogin}>تصميم خاص</button>
        </div>
      </div>
   
      <a href="#pub" className="pub-icon">
        <div className="pub-circle">
          <img src={pub} alt="إعلان" className="pubimage" />
        </div>
      </a>
      
      {/* Ajout de onClick pour le défilement */}
      <div className='scroll-down-wrapper' onClick={scrollDown}>
        <img src={down} alt="تمرير لأسفل" className='scroll-down-icon'/>
      </div>
    </section>
  );
}