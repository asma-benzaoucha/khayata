import '../../style/shoppingStyle/Navbarshop.css';
import React, { useState, useEffect } from 'react';
import logo from '../../assets/logobleu.png';
import home from '../../assets/icons/home.png';
import shop from '../../assets/icons/shop.png';
import commande from '../../assets/icons/commande.png';
import order from '../../assets/icons/special2.png';
import compte from '../../assets/icons/compte.png';
import { useNavigate } from "react-router-dom";

export default function Navbarshop({ defaultSection = "#shop" }) {
  const [activeSection, setActiveSection] = useState(window.location.hash || defaultSection);
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    const handleHashChange = () => {
      setActiveSection(window.location.hash);
    };

    // Récupérer le rôle de l'utilisateur au chargement du composant
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        setUserRole(user.role);
      } catch (error) {
        console.error("Erreur lors du parsing des données utilisateur:", error);
      }
    }

    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const navigate = useNavigate();
  
  const goToShop = () => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user.role === "dropshipper") {
          if (user.is_active === true) {
            navigate("/shoppingDropshipper");
          } else {
            navigate("/NotActiveDropshipper");
          }
        } else if (user.role === "client") {
          navigate("/shopping");
        } else {
          navigate("/");
        }
      } catch (error) {
        console.error("Erreur lors du parsing des données utilisateur:", error);
        navigate("/");
      }
    } else {
      navigate("/");
    }
  };

  const goToSpecial = () => {
    navigate("/special");
  };

  const goToCompte = () => {
    navigate("/compte");
  };

  const goToMycommands = () => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user.role === "dropshipper") {
          if (user.is_active === true) {
            navigate("/mycommandsdropshipper");
          } else {
            navigate("/NotActiveDropshipper");
          }
        } else if (user.role === "client") {
          navigate("/mycommands");
        } else {
          navigate("/");
        }
      } catch (error) {
        console.error("Erreur lors du parsing des données utilisateur:", error);
        navigate("/");
      }
    } else {
      navigate("/");
    }
  };

  const goTolandingPage = () => {
    navigate("/");
  };

  return (
    <>
      {/* Navbar Desktop et Tablette */}
      <div className="containershopping">
       <nav className={`navbarshop desktop-navbar ${userRole === "dropshipper" ? "dropshipper-navbar" : ""}`}>
          <div className="navbar-logo" onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
            <img src={logo} alt="قاف" className="logo-img" />
          </div>
          <div className="navbarshop-links">
            <a href="#home" className={activeSection === "#home" ? "active" : ""} onClick={goTolandingPage}>
              <img src={home} alt="الرئيسية" className="icon" />
              الرئيسية
            </a>
            
            <a href="#shop" className={activeSection === "#shop" ? "active" : ""} onClick={goToShop}>
              <img src={shop} alt="تسوق" className="icon" />
              تسوق
            </a>
            
            {/* Afficher "تصميم خاص" seulement si l'utilisateur n'est pas dropshipper */}
            {userRole !== "dropshipper" && (
              <a href="#custom" className={activeSection === "#custom" ? "active" : ""} onClick={goToSpecial}>
                <img src={order} alt="تصميم خاص" className="icon" />
                تصميم خاص
              </a>
            )}
            
            <a href="#orders" className={activeSection === "#orders" ? "active" : ""} onClick={goToMycommands}>
              <img src={commande} alt="طلبياتي" className="icon" />
              طلبياتي
            </a>

            <a href="#account" className={activeSection === "#account" ? "active" : ""} onClick={goToCompte}>
              <img src={compte} alt="حسابي" className="icon" />
              حسابي
            </a>
          </div>
        </nav>
      </div>
      
      {/* Mobile Navbar */}
      <nav className="mobile-navbar">
        <div className="mobile-topbar">
          <img src={logo} alt="قاف" className="logo-img" />
          <a href="#account" className="account-link" onClick={goToCompte}>
            <img src={compte} alt="حسابي" className="icon" /> 
          </a>
        </div>

        <div className="bottom-nav">
          <a href="#home" className={activeSection === "#home" ? "active" : ""} onClick={goTolandingPage}>
            <img src={home} alt="الرئيسية" className="icon" /><span>الرئيسية</span>
          </a>
          <a href="#shop" className={activeSection === "#shop" ? "active" : ""} onClick={goToShop}>
            <img src={shop} alt="تسوق" className="icon" /><span>تسوق</span>
          </a>
          
          {/* Afficher "تصميم خاص" seulement si l'utilisateur n'est pas dropshipper */}
          {userRole !== "dropshipper" && (
            <a href="#custom" className={activeSection === "#custom" ? "active" : ""} onClick={goToSpecial}>
              <img src={order} alt="تصميم خاص" className="icon" /><span>تصميم</span>
            </a>
          )}
          
          <a href="#orders" className={activeSection === "#orders" ? "active" : ""} onClick={goToMycommands}>
            <img src={commande} alt="طلبياتي" className="icon" /><span>طلبياتي</span>
          </a>
        </div>
      </nav>

      <style jsx>{`
        .dropshipper-navbar .navbarshop-links {
          max-width: calc(100vw - 100px) !important; /* Plus large que la version normale */
          width: auto !important;
          padding: 12px clamp(20px, 3vw, 50px) !important; /* Plus de padding */
        }
        
        @media (min-width: 1200px) {
          .dropshipper-navbar .navbarshop-links {
            gap: 180px !important; /* Plus d'espace entre les liens */
            padding: 12px 50px !important;
          }
        }
        
        @media (max-width: 1200px) and (min-width: 1149px) {
          .dropshipper-navbar .navbarshop-links {
            gap: 160px !important;
          }
        }
        
        @media (max-width: 1149px) and (min-width: 989px) {
          .dropshipper-navbar .navbarshop-links {
            gap: 140px !important;
          }
        }
        
        @media (max-width: 988px) and (min-width: 769px) {
          .dropshipper-navbar .navbarshop-links {
            gap: 100px !important;
          }
        }
      `}</style>
    </>
  );
}