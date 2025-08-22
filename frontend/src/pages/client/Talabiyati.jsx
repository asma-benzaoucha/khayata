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

function Talabiyati() {
  const [commandes, setCommandes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCommandes = async () => {
      try {
        // Récupérer le token JWT depuis le localStorage
        const token = localStorage.getItem('accessToken');
        
        if (!token) {
          throw new Error('Token d\'authentification manquant. Veuillez vous connecter.');
        }

        const response = await fetch('http://127.0.0.1:8000/clientapi/allorders', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });
        
        if (response.status === 401) {
          // Token invalide ou expiré
          localStorage.removeItem('access_token');
          throw new Error('Session expirée. Veuillez vous reconnecter.');
        }
        
        if (response.status === 403) {
          throw new Error('Vous n\'avez pas les permissions nécessaires.');
        }
        
        if (!response.ok) {
          throw new Error(`Erreur serveur: ${response.status}`);
        }
        
        const data = await response.json();
        const transformedData = transformApiData(data);
        setCommandes(transformedData);
      } catch (err) {
        setError(err.message);
        console.error("Erreur détaillée:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCommandes();
  }, []);

  const transformApiData = (apiData) => {
    const transformedCommandes = [];
    const API_BASE_URL = "http://127.0.0.1:8000";

    // Traiter les commandes personnalisées
    if (apiData.custom_orders && apiData.custom_orders.length > 0) {
      apiData.custom_orders.forEach(order => {
        transformedCommandes.push({
          id: order.id,
          namecommand: order.nameorder || "طلبية مخصصة",
          photobutton: ["عرض الصور", photo],
          date: [order.created_at.split('T')[0], date],
          telephone: [order.numTelephone, telephone],
          prix: [order.command_details && order.command_details[0]?.quantity 
                 ? `${parseInt(order.command_details[0].quantity) * 5000}دج` 
                 : "0دج", price],
          nbpieces: [order.command_details && order.command_details[0]?.quantity 
                    ? `${order.command_details[0].quantity} قطعة` 
                    : "0 قطعة", commande],
          status: getStatus(order.state),
          selectedImages: order.custom_images && order.custom_images.length > 0
                         ? order.custom_images.map(img => `${API_BASE_URL}${img.image}`) 
                         : [imageaffichage]
        });
      });
    }

    // Traiter les commandes standard
    if (apiData.standard_orders && apiData.standard_orders.length > 0) {
      apiData.standard_orders.forEach(order => {
        const pricePerPiece = parseFloat(order.fashion_model?.price_per_piece_for_client || 0);
        const quantity = order.standard_command_details && order.standard_command_details[0]?.quantity 
                         ? parseInt(order.standard_command_details[0].quantity) 
                         : 0;
        
        transformedCommandes.push({
          id: order.id,
          namecommand: order.fashion_model?.name || "طلبية قياسية",
          photobutton: ["عرض الصور", photo],
          date: [order.created_at.split('T')[0], date],
          telephone: [order.phone_number, telephone],
          prix: [`${pricePerPiece * quantity}دج`, price],
          nbpieces: [`${quantity} قطعة`, commande],
          status: getStatus(order.state),
          selectedImages: order.fashion_model?.images && order.fashion_model.images.length > 0
                         ? order.fashion_model.images.map(img => `${API_BASE_URL}${img.image}`) 
                         : [imageaffichage]
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
      case 'refused':
        return ["مرفوضة", "#EF4444", refuse];
      case 'pending':
        return ["قيد الانتظار", "#F59E0B", ""];
      default:
        return [state || "غير معروف", "#9CA3AF", ""];
    }
  };

  // Fonction pour se déconnecter
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
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
                  {error.includes('401') || error.includes('expirée') 
                    ? 'انتهت الجلسة. يرجى تسجيل الدخول مرة أخرى.' 
                    : error}
                </p>
                <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                  {(error.includes('401') || error.includes('expirée') || error.includes('manquant')) ? (
                    <button 
                      onClick={() => window.location.href = '/login'}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: '#3B82F6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                      }}
                    >
                      تسجيل الدخول
                    </button>
                  ) : (
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
                  )}
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
              />
            ))
          )}
        </div>
      </div>
    </>
  );
}

export default Talabiyati;