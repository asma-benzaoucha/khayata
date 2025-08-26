import { useState } from "react";
import Sidebaradmin from "../../components/AdminComponents/Sidebaradmin";
import machinecouture from "../../assets/machinecouture.png";
import revenir from "../../assets/avancerjaune.png";
import avancer from "../../assets/revenirjaune.png";
import "../../style/AdminStyle/Dashboard.css";
import Courbe from "@/components/AdminComponents/Courbe";

// Données factices
const couturieres = [
  { id: 1, name: "عائشة سالم" },
  { id: 2, name: "فاطمة الزهراء" },
  { id: 3, name: "خديجة محمد" },
];

const affiliate = [
  { id: 1, name: "افيلي جمال" },
];

const bestmodels = [
  { id: 1, name: "عباءة محتشمة", code: "123" },
  { id: 2, name: "جلباب تقليدي", code: "456" },
];




function Dashboard() {
  // États pour suivre l'index courant de chaque section
  const [currentCouturiereIndex, setCurrentCouturiereIndex] = useState(0);
  const [currentAffiliateIndex, setCurrentAffiliateIndex] = useState(0);
  const [currentModelIndex, setCurrentModelIndex] = useState(0);

  // Fonctions pour naviguer vers l'élément précédent
  const prevCouturiere = () => {
    setCurrentCouturiereIndex(prevIndex => 
      prevIndex === 0 ? couturieres.length - 1 : prevIndex - 1
    );
  };

  const prevAffiliate = () => {
    setCurrentAffiliateIndex(prevIndex => 
      prevIndex === 0 ? affiliate.length - 1 : prevIndex - 1
    );
  };

  const prevModel = () => {
    setCurrentModelIndex(prevIndex => 
      prevIndex === 0 ? bestmodels.length - 1 : prevIndex - 1
    );
  };

  // Fonctions pour naviguer vers l'élément suivant
  const nextCouturiere = () => {
    setCurrentCouturiereIndex(prevIndex => 
      prevIndex === couturieres.length - 1 ? 0 : prevIndex + 1
    );
  };

  const nextAffiliate = () => {
    setCurrentAffiliateIndex(prevIndex => 
      prevIndex === affiliate.length - 1 ? 0 : prevIndex + 1
    );
  };

  const nextModel = () => {
    setCurrentModelIndex(prevIndex => 
      prevIndex === bestmodels.length - 1 ? 0 : prevIndex + 1
    );
  };

  return (
    <div className="Containeradmindashboard">
      <Sidebaradmin />

      <div className="contentadmindashboard">
        {/* Titre + bouton */}
        <div className="dashboard-header">
          <h2>لوحة التحكم</h2>
        </div>
        <p className="soustitredashboard">احصائيات عامة حول مداخيل المتجر و نشاط العملاء</p>

        {/* Cartes machines */}
        <div className="Cardselements">
             
         
          {/* Couturière - Affiche les flèches seulement s'il y a plusieurs éléments */}
          <div className="machine-card">
            <img src={machinecouture} alt="machine" className="machine-img" />
            <div className="machine-content">
              <p className="title">الخياطة الأكثر مهارة</p>
              <div className={`containerarrow-elements ${couturieres.length === 1 ? 'single-item-center' : ''}`}>
                {couturieres.length > 1 && (
                  <img 
                    src={revenir} 
                    alt="prev" 
                    className="arrow" 
                    onClick={prevCouturiere}
                  />
                )}
                
                <div className="value-container">
                  <h3 className="value">{couturieres[currentCouturiereIndex].name}</h3>
                </div>
                
                {couturieres.length > 1 && (
                  <img 
                    src={avancer} 
                    alt="next" 
                    className="arrow" 
                    onClick={nextCouturiere}
                  />
                )}
              </div>
            </div>
          </div>

          {/* Affiliate - N'affiche pas les flèches car un seul élément */}
          <div className="machine-card">
            <img src={machinecouture} alt="machine" className="machine-img" />
            <div className="machine-content">
              <p className="title">المروج الأكثر نشاطا</p>
              <div className={`containerarrow-elements ${affiliate.length === 1 ? 'single-item-center' : ''}`}>
                {affiliate.length > 1 && (
                  <img 
                    src={revenir} 
                    alt="prev" 
                    className="arrow" 
                    onClick={prevAffiliate}
                  />
                )}
                
                <div className="value-container">
                  <h3 className="value">{affiliate[currentAffiliateIndex].name}</h3>
                </div>
                
                {affiliate.length > 1 && (
                  <img 
                    src={avancer} 
                    alt="next" 
                    className="arrow" 
                    onClick={nextAffiliate}
                  />
                )}
              </div>
            </div>
          </div>
          
          {/* Meilleur modèle - Affiche les flèches seulement s'il y a plusieurs éléments */}
          <div className="machine-card">
            <img src={machinecouture} alt="machine" className="machine-img" />
            <div className="machine-content">
              <p className="title">النموذج الأكثر مبيعاً</p>
              <div className={`containerarrow-elements ${bestmodels.length === 1 ? 'single-item-center' : ''}`}>
                {bestmodels.length > 1 && (
                  <img 
                    src={revenir} 
                    alt="prev" 
                    className="arrow" 
                    onClick={prevModel}
                  />
                )}
                
                <div className="value-container">
                  <h3 className="value">{bestmodels[currentModelIndex].name}</h3>
                  <div className="code"> {bestmodels[currentModelIndex].code}</div>
                </div>
                
                {bestmodels.length > 1 && (
                  <img 
                    src={avancer} 
                    alt="next" 
                    className="arrow" 
                    onClick={nextModel}
                  />
                )}
              </div>
            </div>
          </div>
         
        </div>

        {/* Section graphe */}
        <div className="courbesection">
          <Courbe/>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;