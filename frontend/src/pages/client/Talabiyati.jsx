import { useState, useEffect } from "react";
import CommandCard from "../../components/generalComponents/Commandcard";
import { TbBoxOff } from "react-icons/tb";
import photo from '../../assets/icons/photo.png';
import imageaffichage from '../../assets/icons/two.png';
import date from '../../assets/icons/date.png';
import commande from '../../assets/icons/commande.png';
import price from '../../assets/icons/price.png';
import telephone from '../../assets/icons/whatsapp.png';
import refuse from '../../assets/icons/refuse.png';
import Navbarshop from "../../components/shoppingComp/Navbarshop";
import api from "../../apimanagement/api"; // Importez votre instance axios personnalisée

function Talabiyati() {
  const [commandes, setCommandes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCommandes = async () => {
      try {
        // Vérification préalable des tokens - si pas de refresh token, on ne fait même pas la requête
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          // Redirection immédiate vers le login
          window.location.href = '/loginClient';
          return;
        }
        
        // Utilisation de l'API personnalisée avec authentification
        const response = await api.withAuth(true, true).get('/clientapi/allorders');
        
        const data = response.data;
        const transformedData = transformApiData(data);
        setCommandes(transformedData);
      } catch (err) {
        console.error("Erreur détaillée:", err);
        
        // Si l'erreur concerne l'authentification, on laisse l'intercepteur gérer
        if (err.response?.status === 401 || err.message?.includes('Authentication') || err.message?.includes('refresh token')) {
          // Ces erreurs sont gérées par l'intercepteur, on ne fait rien
          return;
        } 
        
        // Pour les autres erreurs, on les affiche
        if (err.response?.status === 403) {
          setError('Vous n\'avez pas les permissions nécessaires.');
        } else {
          setError(`Erreur: ${err.message || 'Une erreur est survenue'}`);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCommandes();
  }, []);

  const transformApiData = (apiData) => {
    const transformedCommandes = [];
    const API_BASE_URL = "http://127.0.0.1:8000";

    // Traiter les commandes standard
  if (apiData.standard_orders && apiData.standard_orders.length > 0) {
    apiData.standard_orders.forEach(order => {
      // Calculer la quantité totale
      const totalQuantity = order.variants 
        ? order.variants.reduce((sum, variant) => sum + (variant.quantity || 0), 0)
        : 0;
      
      transformedCommandes.push({
        id: `standard_${order.id}`, // Ajouter un préfixe pour rendre la clé unique
        namecommand: order.model_name || "طلبية قياسية",
        photobutton: ["عرض الصور", photo],
        date: [order.created_at.split('T')[0], date],
        telephone: [order.phone_number, telephone],
        prix: [`${order.final_price || 0}دج`, price],
        nbpieces: [`${totalQuantity} قطعة`, commande],
        status: getStatus(order.state),
        selectedImages: order.images && order.images.length > 0
          ? order.images.map(img => `${API_BASE_URL}${img.image}`)
          : [imageaffichage],
        isCustom: false // Ajouter un flag pour identifier les commandes personnalisées
      });
    });
  }

  // Traiter les commandes personnalisées
  if (apiData.custom_orders && apiData.custom_orders.length > 0) {
    apiData.custom_orders.forEach(order => {
      // Calculer la quantité totale
      const totalQuantity = order.variants 
        ? order.variants.reduce((sum, variant) => sum + (variant.quantity || 0), 0)
        : 0;
      
      // Pour les commandes personnalisées, on utilise initial_price
      // Si initial_price est null, on passe null pour que CommandCard gère l'affichage
      const customPrice = order.initial_price === null ? null : `${order.initial_price}دج`;
      
      transformedCommandes.push({
        id: `custom_${order.id}`, // Ajouter un préfixe pour rendre la clé unique
        namecommand: order.nameorder || "طلبية مخصصة",
        photobutton: ["عرض الصور", photo],
        date: [order.created_at.split('T')[0], date],
        telephone: [order.numTelephone, telephone],
        prix: customPrice === null ? null : [customPrice, price],
        nbpieces: [`${totalQuantity} قطعة`, commande],
        status: getStatus(order.state),
        selectedImages: order.images && order.images.length > 0
          ? order.images.map(img => `${API_BASE_URL}${img.image}`)
          : [imageaffichage],
        isCustom: true // Ajouter un flag pour identifier les commandes personnalisées
      });
    });
  }

  return transformedCommandes;
};

  const getStatus = (state) => {
    switch(state) {
      case 'done':
        return ["مكتملة", "#22C55E", ""];
      case 'cancelled':
        return ["ملغية", "#EF4444", refuse];
      case 'pending':
        return ["قيد الانتظار", "#F59E0B", ""];
      default:
        return [state || "غير معروف", "#9CA3AF", ""];
    }
  };

  // Fonction pour se déconnecter
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    window.location.href = '/loginClient';
  };

  // Fonction pour rafraîchir la page
  const handleRetry = () => {
    window.location.reload();
  };

  if (loading) {
    return (
      <>
        <Navbarshop />
        <div className="containershop">
          <div className="shop-wrapper">
            <div className="cards-empty-container">
              <div style={{ textAlign: "center", color: "#9ca3af" }}>
                <p style={{ fontSize: "1.2rem", marginTop: "10px" }}>
                  جاري تحميل البيانات...
                </p>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbarshop />
        <div className="containershop">
          <div className="shop-wrapper">
            <div className="cards-empty-container">
              <div style={{ textAlign: "center", color: "#9ca3af" }}>
                <TbBoxOff size={80} />
                <p style={{ fontSize: "1.2rem", marginTop: "10px" }}>
                  {error}
                </p>
                <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                  <button 
                    onClick={handleRetry}
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#10B981',
                      color: 'white',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: 'pointer'
                    }}
                  >
                    إعادة المحاولة
                  </button>
                  <button 
                    onClick={handleLogout}
                    style={{
                      padding: '10px 20px',
                      backgroundColor: '#EF4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: 'pointer'
                    }}
                  >
                    تسجيل الخروج
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbarshop />
      <div className="containershop">
        <div className="shop-wrapper">
          {commandes.length === 0 ? (
            <div className="cards-empty-container">
              <div style={{ textAlign: "center", color: "#9ca3af" }}>
                <TbBoxOff size={80} />
                <p style={{ fontSize: "1.2rem", marginTop: "10px" }}>
                  لا توجد أي طلبية حالياً
                </p>
              </div>
            </div>
          ) : (
            commandes.map((cmd) => (
              <CommandCard
                key={cmd.id}
                namecommand={cmd.namecommand}
                photobutton={cmd.photobutton}
                date={cmd.date}
                telephone={cmd.telephone}
                prix={cmd.prix}
                nbpieces={cmd.nbpieces}
                status={cmd.status}
                selectedImages={cmd.selectedImages}
                isCustom={cmd.isCustom}
              />
            ))
          )}
        </div>
      </div>
    </>
  );
}

export default Talabiyati;