// components/ProtectedRoute.js
import { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, requiredUserType = null }) => {
  const [isValidating, setIsValidating] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState(null);

  // Fonction pour décoder le JWT
  const decodeToken = (token) => {
    try {
      if (!token) return null;
      const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      const payload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      return JSON.parse(payload);
    } catch (error) {
      console.error('Erreur lors du décodage du token:', error);
      return null;
    }
  };

  // Vérifier si un token est expiré
  const isTokenExpired = (token) => {
    if (!token) return true;
    const decoded = decodeToken(token);
    if (!decoded || !decoded.exp) return true;
    
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  };

  // Obtenir le type d'utilisateur depuis le localStorage
  const getUserTypeFromStorage = () => {
    try {
      const userData = localStorage.getItem('user');
      if (!userData) return null;
      
      const parsedData = JSON.parse(userData);
      
      
      // Retourner le rôle depuis les différentes propriétés possibles
      return parsedData.role || parsedData.userType || parsedData.user_type;
    } catch (error) {
      console.error('Erreur lors de la lecture du userData:', error);
      return null;
    }
  };

  // Rafraîchir le token
  const refreshToken = async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refreshToken');
      
      if (!refreshTokenValue) {
        throw new Error('Aucun refresh token disponible');
      }
      
      const response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshTokenValue }),
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Erreur de rafraîchissement:', response.status, errorData);
        
        if (response.status === 401 || response.status === 400) {
          localStorage.removeItem('refreshToken');
          throw new Error('Refresh token invalide');
        }
        throw new Error(`Échec du rafraîchissement: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.access) {
        localStorage.setItem('accessToken', data.access);
        return data.access;
      } else {
        throw new Error('Format de réponse invalide: aucun access token');
      }
    } catch (error) {
      console.error('Erreur lors du rafraîchissement du token:', error);
      throw error;
    }
  };

  useEffect(() => {
    const validateAuth = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        const refreshTokenValue = localStorage.getItem('refreshToken');
        
        
        // Cas 1: Aucun token trouvé
        if (!accessToken && !refreshTokenValue) {
          console.log('Aucun token disponible');
          setIsValidating(false);
          return;
        }
        
        let validAccessToken = accessToken;
        let currentUserType = getUserTypeFromStorage();
        
        
        
        // Vérifier si le token est expiré
        const isExpired = accessToken ? isTokenExpired(accessToken) : true;
        
        // Cas 2: Token d'accès expiré mais refresh token disponible
        if (isExpired && refreshTokenValue) {
          console.log('Token expiré, tentative de rafraîchissement');
          try {
            validAccessToken = await refreshToken();
            console.log('Token rafraîchi avec succès');
          } catch (error) {
            console.error('Impossible de rafraîchir le token:', error);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user'); // Nettoyer aussi les données utilisateur
            setIsValidating(false);
            return;
          }
        } 
        // Cas 3: Token valide mais pas de userType dans le storage
        else if (accessToken && !isExpired && !currentUserType) {
          console.log('Token valide mais userType manquant dans localStorage');
          // Vous pourriez faire une requête API ici pour récupérer les données utilisateur
        }
        
        // Stocker le type d'utilisateur
        setUserType(currentUserType);
        
        // Vérification du type d'utilisateur si requis
        if (requiredUserType && currentUserType !== requiredUserType) {
          console.warn(`Accès refusé: ${currentUserType} tentant d'accéder à une page ${requiredUserType}`);
          setIsValidating(false);
          return;
        }
        
        // Vérifier si on a un token valide
        if (validAccessToken && !isTokenExpired(validAccessToken)) {
          console.log('Authentification réussie');
          setIsAuthenticated(true);
        } else {
          console.log('Token invalide ou expiré après rafraîchissement');
        }
        
      } catch (error) {
        console.error('Erreur lors de la validation de l\'authentification:', error);
      } finally {
        setIsValidating(false);
      }
    };

    validateAuth();
  }, [requiredUserType]);

  // Pendant la validation, afficher un indicateur de chargement
  if (isValidating) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <div style={{ width: '40px', height: '40px', border: '4px solid #f3f3f3', 
                     borderTop: '4px solid #3498db', borderRadius: '50%', 
                     animation: 'spin 1s linear infinite' }}></div>
        <div>Vérification de l'authentification...</div>
        <style>
          {`
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          `}
        </style>
      </div>
    );
  }

  // Redirection vers la page de login appropriée si non authentifié
  if (!isAuthenticated) {
    // Déterminer le chemin de login
    let loginPath = '/login';
    const userData = localStorage.getItem('user');
    if (userData){
     localStorage.removeItem('user')
    }
    
    // Utiliser le userType détecté ou le requiredUserType
    const targetUserType = userType || requiredUserType;
    console.log('Redirection - userType:', userType, 'requiredUserType:', requiredUserType, 'target:', targetUserType);
    
    if (targetUserType === 'admin') {
      loginPath = '/admin/login';
      

    } else if (targetUserType === 'client') {
      loginPath = '/login';
    } else if (targetUserType === 'couturiere') {
      loginPath = '/login';
    }
    
    console.log(`Redirection vers: ${loginPath}`);
    
    // Nettoyer les données si l'accès est refusé
    if (userType && requiredUserType && userType !== requiredUserType) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
    }
    
    return <Navigate to={loginPath} replace />;
  }

  // Si authentifié, afficher le contenu protégé
  return children;
};

export default ProtectedRoute;