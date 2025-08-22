import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../../style/landingStyle/ProductSection.css";

// Icônes de flèche (inchangées)
const ArrowRight = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ArrowLeft = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

function ProductImageSlider({ images }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToPrevious = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? images.length - 1 : prevIndex - 1
    );
  };

  const goToNext = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === images.length - 1 ? 0 : prevIndex + 1
    );
  };

  return (
    <div className="image-slider-container">
      <div className="image-container">
        {images.length > 0 ? (
          <img src={images[currentIndex]} alt={`Product view ${currentIndex + 1}`} />
        ) : (
          <div className="no-image">لا توجد صورة</div>
        )}
        <span className="badge">الأكثر مبيعًا</span>

        {images.length > 1 && (
          <>
            <button className="nav-button prev-button" onClick={(e) => { e.stopPropagation(); goToPrevious(); }}>
              <ArrowRight />
            </button>
            <button className="nav-button next-button" onClick={(e) => { e.stopPropagation(); goToNext(); }}>
              <ArrowLeft />
            </button>

            <div className="image-indicators">
              {images.map((_, index) => (
                <span
                  key={index}
                  className={`indicator ${index === currentIndex ? "active" : ""}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    setCurrentIndex(index);
                  }}
                ></span>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default function ProductSection() {
  const [products, setProducts] = useState([]);
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
  
  // Fonction pour gérer la navigation selon le token
  const handleNavigation = (path) => {
    const refreshToken = localStorage.getItem('refreshToken');
    
    // Si pas de refresh token ou token expiré, aller au login
    if (!refreshToken || isTokenExpired(refreshToken)) {
      navigate("/loginClient");
    } else {
      // Refresh token valide, aller vers la page demandée
      navigate(path);
    }
  };

  const handleDiscoverMore = () => {
    handleNavigation("/shopping");
  };

  const handleCustomDesign = () => {
    handleNavigation("/special");
  };

  const handleBrowseAll = () => {
    handleNavigation("/shopping");
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/clientapi/top-selling-models/")
      .then((res) => res.json())
      .then((data) => {
        // Adapter le format des images
        const formatted = data.map((item, index) => ({
          id: index,
          title: item.name,
          price: item.price_per_piece_for_client + " دج",
          sizes: item.sizes || [],
          images: item.images.map((img) => img.image),
        }));
        setProducts(formatted);
      })
      .catch((err) => console.error("Erreur API:", err));
  }, []);

  return (
    <>
      <section className="product-section">
        <h2 className="section-title">تسوّق من مجموعتنا الحصرية</h2>
        <p className="section-subtitle">
          اكتشف جودة تصاميمنا أو اطلب تصميماً مخصصاً يناسب ذوقك
        </p>

        <div className="product-scroll-container">
          <div className="product-grid">
            {products.map((product) => (
              <div className="product-card" key={product.id}>
                <ProductImageSlider images={product.images} />
                <div className="product-info">
                  <div className="title-price">
                    <h3>{product.title}</h3>
                    <span className="price">{product.price}</span>
                  </div>
                  <p className="sizes">
                    <span>المقاسات:</span>
                    {product.sizes.length > 0 ? (
                      product.sizes.map((size, idx) => (
                        <span key={idx} className="size">{size}</span>
                      ))
                    ) : (
                      <span className="size">غير متوفر</span>
                    )}
                  </p>
                  <button className="buy-button" onClick={handleDiscoverMore}>
                    اكتشف المزيد
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="product-section">
        <h2 className="section-title">لم تَجِد ما تبحث عنه؟</h2>
        <p className="section-subtitle">
          اطلب تصميما مخصصا بالكامل يناسب ذوقك و مقاساتك الخاصة
        </p>
        <div className="notfound-buttons">
          <button className="notfound-btn filled" onClick={handleCustomDesign}>
            اطلب تصميم مخصص
          </button>
          <button className="notfound-btn outlined" onClick={handleBrowseAll}>
            تصفّح كامل العرض
          </button>
        </div>
      </section>
    </>
  );
}