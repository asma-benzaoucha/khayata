import RegistrationSuccess from "./pages/user/registration-success-to-verified";
import RegistrationCouturiere from "./pages/user/registration-form-couturiere";
import ForgotPassword from "./pages/user/forgot-password";
import VerificationCode from "./pages/user/verificationCode";
import PasswordSuccess from "./pages/user/PasswordSuccess";
import ResetPassword from "./pages/user/ResetPassword";
import LoginPage from "./pages/user/LoginPage";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landingpage from './pages/client/Landingpage';
import ShoppingPage from './pages/client/ShoppingPage'
import FormAcheter from './pages/client/FormAcheterPage'
import ModelSpecialPage from "./pages/client/ModelSpecialPage";
import CompteclientPage from "./pages/client/CompteclientPage";
import Talabiyati from "./pages/client/Talabiyati";
import Popupimages from "./components/generalComponents/Popupimages";
import Test from "./components/generalComponents/test";
import LoginClient from "./pages/client/LoginClient";
import RegistrationClient from "./pages/client/RegistrationClient";
import LoginAdmin from "./pages/admin/LoginAdmin";
import Dashboard from "./pages/admin/Dashboard";
import ProtectedRoute from "./apimanagement/ProtectedRoute.jsx";
import TermsAndPolicy from "./pages/client/TermsAndPolicy";
import Sidebaradmin from "./components/AdminComponents/Sidebaradmin.jsx";


export default function App() {
  return (
    <Router>
      <Routes>
        {/* Routes publiques - accessibles sans authentification */}
        <Route path="/" element={<Landingpage />} />
        <Route path="/rules" element={<TermsAndPolicy/>} />
        
        
        {/* Routes d'authentification */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/loginClient" element={<LoginClient />} />
        <Route path="/registerclient" element={<RegistrationClient />} />
        <Route path="/signup" element={<RegistrationCouturiere />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verification" element={<VerificationCode />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/password-success" element={<PasswordSuccess />} />
        <Route path="/registration-success" element={<RegistrationSuccess />} />
        <Route path="/admin/login" element={<LoginAdmin />} />
        <Route path="/testing" element={<Sidebaradmin />} />
        
        
        {/* Routes protégées pour clients */}

        
        <Route path="/shopping" element={
          <ProtectedRoute requiredUserType="client">
            <ShoppingPage />
          </ProtectedRoute>
        } />

        <Route path="/special" element={
          <ProtectedRoute requiredUserType="client">
            <ModelSpecialPage />
          </ProtectedRoute>
        } />
        <Route path="/shopping/acheter" element={
          <ProtectedRoute requiredUserType="client">
            <FormAcheter />
          </ProtectedRoute>
        } />
        <Route path="/compte" element={
          <ProtectedRoute requiredUserType="client">
            <CompteclientPage />
          </ProtectedRoute>
        } />
        <Route path="/mycommands" element={
          <ProtectedRoute requiredUserType="client">
            <Talabiyati />
          </ProtectedRoute>
        } />
        
        {/* Routes protégées pour admin */}
        <Route path="/admin/dashboard" element={
          <ProtectedRoute requiredUserType="admin">
            <Dashboard />
          </ProtectedRoute>
        } />
        
        
        {/* Routes protégées pour couturières */}
        <Route path="/couturiere/dashboard" element={
          <ProtectedRoute requiredUserType="couturiere">
          </ProtectedRoute>
        } />
        
        {/* Routes protégées sans type spécifique (accessibles à tous les utilisateurs authentifiés) */}
        <Route path="/test" element={
          <ProtectedRoute>
            <Test />
          </ProtectedRoute>
        } />
        <Route path="/popup" element={
          <ProtectedRoute>
            <Popupimages />
          </ProtectedRoute>
        } />
        
      </Routes>




    </Router>
  );
}