// components/ProtectedWrapper.jsx
import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { checkInitialAuth } from "../utils/auth"; 

function ProtectedWrapper({ children }) {
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    (async () => {
      const ok = await checkInitialAuth(location.pathname);
      if (!ok) {
        const publicRoutes = [
          "/login", "/signup", "/verification", "/forgot-password", 
          "/reset-password", "/registration-success", "/", 
          "/password-success", "/rules", "/rulesdropshipper",
          "/admin/login", "/SignupDropshipper", "/RegistrationSucess",
          "/RefuseDropshipperPage", "/registration-couturiere-refused",
          "/NotActiveDropshipper", "/NotActiveCouturiere"
        ];
        
        if (!publicRoutes.includes(location.pathname)) {
          navigate("/login");
        }
      }
      setLoading(false);
    })();
  }, [location.pathname, navigate]);

  if (loading) {
    return <div>Chargement...</div>; // Ou ton composant de loading
  }

  return children;
}

export default ProtectedWrapper;