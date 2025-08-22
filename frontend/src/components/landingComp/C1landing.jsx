import '../../style/landingStyle/C1landing.css';
import down from '../../assets/icons/down.png'
import pub from "../../assets/icons/publ.png";
import { useNavigate } from "react-router-dom";

export default function C1landing() {
  const navigate = useNavigate();
  
  // Fonction pour vérifier si un JWT est expiré
  const isTokenExpired = (token) => {
    if (!token) return true;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expirationTime = payload.exp * 1000; // Convertir en millisecondes
      const currentTime = Date.now();
      
      return expirationTime <= currentTime;
    } catch (error) {
      console.error('Erreur lors du décodage du token:', error);
      return true; // En cas d'erreur, considérer comme expiré
    }
  };
  
  const goToShoppingOrLogin = () => {
    const refreshToken = localStorage.getItem('refreshToken');
    
    // Si pas de refresh token ou token expiré, aller au login
    if (!refreshToken || isTokenExpired(refreshToken)) {
      navigate("/loginClient");
    } else {
      // Refresh token valide, aller directement au shopping
      navigate("/shopping");
    }
  };
  
  const goToSpecialOrLogin = () => {
    const refreshToken = localStorage.getItem('refreshToken');
    
    // Si pas de refresh token ou token expiré, aller au login
    if (!refreshToken || isTokenExpired(refreshToken)) {
      navigate("/loginClient");
    } else {
      // Refresh token valide, aller directement à la page spéciale
      navigate("/special");
    }
  };
  
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
      
      <div className='scroll-down-wrapper'>
        <img src={down} alt="إعلان" className='scroll-down-icon'/>
      </div>
    </section>
  );
}