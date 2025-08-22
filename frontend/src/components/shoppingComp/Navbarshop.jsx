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

  useEffect(() => {
    const handleHashChange = () => {
      setActiveSection(window.location.hash);
    };

    window.addEventListener("hashchange", handleHashChange);

    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const navigate = useNavigate();
  const goToShop = () => {
    navigate("/shopping");
  };
   const goToSpecial = () => {
    navigate("/special");
  };
    const goToCompte = () => {
    navigate("/compte");
  };
    const goToMycommands = () => {
    navigate("/mycommands");
  };
 const goTolandingPage = () => {
    navigate("/");
  };
  

  
  return (
    <>
      {/* Navbar Desktop et Tablette */}
      <div className="containershopping">
      <nav className="navbarshop desktop-navbar">
        <div className="navbar-logo">
          <img src={logo} alt="قاف" className="logo-img" />
        </div>
        <div className="navbarshop-links">
          <a href="#home" className={activeSection === "#home" ? "active" : ""}  onClick={goTolandingPage}>
            <img src={home} alt="الرئيسية" className="icon" />
            الرئيسية
          </a>
          
          <a href="#shop" className={activeSection === "#shop" ? "active" : ""} onClick={goToShop}>
            <img src={shop} alt="تسوق" className="icon" />
             تسوق
          </a>
          <a href="#custom" className={activeSection === "#custom" ? "active" : ""} onClick={goToSpecial}>
            <img src={order} alt="تصميم خاص" className="icon" />
             تصميم خاص
          </a>
           <a href="#orders" className={activeSection === "#orders" ? "active" : ""}onClick={goToMycommands}>
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
          <a href="#home" className={activeSection === "#home" ? "active" : ""}>
            <img src={home} alt="الرئيسية" className="icon" /><span>الرئيسية</span>
          </a>
          <a href="#shop" className={activeSection === "#shop" ? "active" : ""}onClick={goToShop}>
            <img src={shop} alt="تسوق" className="icon"  /><span>تسوق</span>
          </a>
          <a href="#custom" className={activeSection === "#custom" ? "active" : ""}onClick={goToSpecial}>
            <img src={order} alt="تصميم خاص" className="icon" /><span>تصميم</span>
          </a>
          <a href="#orders" className={activeSection === "#orders" ? "active" : ""} onClick={goToMycommands}>
            <img src={commande} alt="طلبياتي" className="icon" /><span>طلبياتي</span>
          </a>
        </div>
      </nav>
    

    </>
  );
}